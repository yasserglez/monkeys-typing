from bisect import bisect_left
from collections import deque
from copy import deepcopy
from itertools import islice, izip, product
from json import dump, load
from random import randint
from re import split


# Build a map of input chars to typewriter chars.
LETTERS = {l:l for l in 'abcdefghijklmnopqrstuvwxyz'}
DIGITS = {d:'#' for d in '0123456789'}
PUNCTUATION = {p:p for p in ' ,.;:?!()-\'"'}
INPUT_CHAR_MAP = dict(LETTERS.items() + DIGITS.items() + 
                      PUNCTUATION.items())

# Build maps of typewriter chars to integers and vice versa.
INDEX_MAP = ''.join(sorted(set(INPUT_CHAR_MAP.values() + ['@'])))
CHAR_MAP = {c:i for i, c in enumerate(INDEX_MAP)}

# Number of typewriter chars (40 in the assignment).
NUM_CHARS = len(INDEX_MAP)

# Map any input char into the NUM_CHARS typewriter chars (if a char
# is not found in INPUT_CHAR_MAP it is mapped to @).
map_input_char = lambda c: INPUT_CHAR_MAP.get(c.lower(), '@')

# Assign consecutive integers to every typewriter char (ASCII order).
char2index = lambda c: CHAR_MAP[c]

# The inverse of char2index.
index2char = lambda i: INDEX_MAP[i]


# Compute a freq table of the given order from plain text files.
def freq_tab_creation(order, *corpus_files):
    freq_tab = _freq_tab_init(order)
    for corpus_file in corpus_files:
        fd = open(corpus_file, 'r')
        text = fd.read()
        shifted_seqs = [islice(text, i, None) for i in xrange(order)]
        for input_ngram in izip(*shifted_seqs):
            typewriter_ngram = map(map_input_char, input_ngram)
            _freq_tab_inc(freq_tab, map(char2index, typewriter_ngram))
        fd.close()
    return freq_tab


# Reduce the resolution of the typewriter -- i.e. reduce the freqs 
# in the table by the ratio given in factor. freq_tab is modified!
def freq_tab_resolution(freq_tab, factor):
    order = _freq_tab_order(freq_tab)
    for ngram_index in product(xrange(NUM_CHARS), repeat=order):
        ngram_freq = _freq_tab_get(freq_tab, ngram_index)
        if ngram_freq > 0:
            ngram_freq = int(factor * ngram_freq)
            _freq_tab_set(freq_tab, ngram_index, ngram_freq)


# Export all the n-grams with non-zero freqs to a JSON file.
def freq_tab_write(freq_tab, output_file):
    order = _freq_tab_order(freq_tab)
    nonzero_ngrams = {}
    for ngram_index in product(xrange(NUM_CHARS), repeat=order):
        ngram_freq = _freq_tab_get(freq_tab, ngram_index)
        if ngram_freq > 0:
            ngram = ''.join(map(index2char, ngram_index))
            nonzero_ngrams[ngram] = ngram_freq
    fd = open(output_file, 'w')
    dump(nonzero_ngrams, fd)
    fd.close()


# Build the freq table from the n-gram freqs in a JSON file.
def freq_tab_read(input_file):
    fd = open(input_file, 'r')
    nonzero_ngrams = load(fd)
    fd.close()
    order = len(nonzero_ngrams.iterkeys().next())
    freq_tab = _freq_tab_init(order)
    for ngram, ngram_freq in nonzero_ngrams.iteritems():
        _freq_tab_set(freq_tab, map(char2index, ngram), ngram_freq)
    return freq_tab


# Given an n-gram prefix with (n-1) chars, compute the most probable
# char seq without repeated chars following the given freq table.  
def freq_tab_most_probable_path(freq_tab, ngram_prefix):
    path = ngram_prefix
    ngram_prefix = deque()
    for char in path:
        ngram_prefix.append(char2index(char))
    while len(path) < NUM_CHARS:
        tab_ref = freq_tab
        for i in ngram_prefix:
            tab_ref = tab_ref[i]
        # Find the char with the highest freq (not already included).
        char_freq, char_index = 0, None
        for i in xrange(NUM_CHARS):
            if tab_ref[i] > char_freq and index2char(i) not in path:
                char_freq = tab_ref[i]
                char_index = i
        if char_freq > 0:
            # Append the char and update the prefix.
            path += index2char(char_index)
            ngram_prefix.append(char_index)
            ngram_prefix.popleft()
        else:
            # Stop. All remaining chars have zero freqs.
            break
    return path


# Sample num_chars chars from the given freq table and save them to 
# output_file. freq_tab must be set to None for the straightforward
# monkey problem (order 0).
def freq_tab_simulation(freq_tab, num_chars, output_file):
    order = _freq_tab_order(freq_tab)
    ngram_prefix = deque()
    fd = open(output_file, 'w')
    for i in xrange(num_chars):
        if order == 0:
            # The straightforward monkey problem (sampled uniformly).
            char_index = randint(0, NUM_CHARS - 1)
        else:
            if len(ngram_prefix) < order - 1:
                # The first (order-1) chars are sampled uniformly.
                char_index = randint(0, NUM_CHARS - 1)
                ngram_prefix.append(char_index)
            else:
                # Sample according to the freq table.
                char_index = _freq_tab_sample(freq_tab, ngram_prefix)
                ngram_prefix.append(char_index)
                ngram_prefix.popleft()
        fd.write(index2char(char_index))
    fd.close()


# Number of words from the corpus file that appear in the simulated 
# file divided by the total number of words in the corpus file.
def relative_word_yield(simulated_file, corpus_file):
    word_yield = 0.0
    corpus_words = _get_words(corpus_file)
    for word in _get_words(simulated_file):
        if word in corpus_words:
            word_yield += 1
    relative_word_yield = word_yield / len(corpus_words)
    return relative_word_yield


def profile_creation(freq_tab, profile_len):
    pass


def profile_dissimilarity(profile1, profile2):
    pass


# Initialize a freq table with all counts set to a given value.
def _freq_tab_init(order, value=0):
    freq_tab = [value] * NUM_CHARS if order > 0 else None
    for n in xrange(1, order):
        tmp = [freq_tab]
        tmp += [deepcopy(freq_tab) for i in xrange(NUM_CHARS - 1)] 
        freq_tab = tmp
    return freq_tab


# Return the order of the freq table.
def _freq_tab_order(freq_tab):
    order = 0
    tab_ref = freq_tab
    while isinstance(tab_ref, list):
        tab_ref = tab_ref[0]
        order += 1
    return order     


# Get the freq of an n-gram given the indexes of its chars.
def _freq_tab_get(freq_tab, ngram_index):
    tab_ref = freq_tab
    for n, i in enumerate(ngram_index):
        if n == len(ngram_index) - 1:
            return tab_ref[i]
        else:
            tab_ref = tab_ref[i]


# Update the freq of an n-gram given the indexes of its chars.
def _freq_tab_set(freq_tab, ngram_index, ngram_freq):
    tab_ref = freq_tab
    for n, i in enumerate(ngram_index):
        if n == len(ngram_index) - 1:
            tab_ref[i] = ngram_freq
        else:
            tab_ref = tab_ref[i]


# Add 1 to the freq of an n-gram given the indexes of its chars.
def _freq_tab_inc(freq_tab, ngram_index):
    tab_ref = freq_tab
    for n, i in enumerate(ngram_index):
        if n == len(ngram_index) - 1:
            tab_ref[i] += 1
        else:
            tab_ref = tab_ref[i]


# Sample a char from the freq table given the (order-1) chars of 
# the n-gram prefix.
def _freq_tab_sample(freq_tab, ngram_prefix):
    # Compute the cumulative values of the freq dist.
    cumul_sum, cumul_freqs = 0, []
    tab_ref = freq_tab
    for i in ngram_prefix:
        tab_ref = tab_ref[i]
    for i in xrange(NUM_CHARS):
        cumul_sum += tab_ref[i]
        cumul_freqs.append(cumul_sum)
    # Sample an integer in [0,cumul_sum] and find its position in the
    # ordered list cumul_freqs. The position will be the char index.
    char_index = (randint(0, NUM_CHARS - 1) if cumul_sum == 0 else
                  bisect_left(cumul_freqs, randint(0, cumul_sum)))
    return char_index


# Return a set with the words in the file.
def _get_words(text_file):
    split_chars = '@'
    for char in PUNCTUATION.iterkeys():
        # The dash needs to be escaped in the regex.
        split_chars += '\-' if char == '-' else char
    fd = open(text_file, 'r')
    typewriter_text = ''.join((map_input_char(c) for c in fd.read()))
    fd.close()
    split_re = '[' + split_chars + ']+'
    words = split(split_re, typewriter_text.strip(split_chars))
    return set(words)
