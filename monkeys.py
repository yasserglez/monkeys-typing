
from bisect import bisect_left
from copy import deepcopy
from collections import deque
from itertools import islice, izip, product
from json import dump, load
from random import randint
from re import split


# Build a map of input chars to typewriter chars.
LETTERS = {l: l for l in 'abcdefghijklmnopqrstuvwxyz'}
DIGITS = {d: '#' for d in '0123456789'}
PUNCTUATION = {p: p for p in ' ,.;:?!()-\'"'}
INPUT_CHAR_MAP = dict(LETTERS.items() + DIGITS.items() + PUNCTUATION.items())

# Build maps of typewriter chars to integers and vice versa.
INDEX_MAP = ''.join(sorted(set(INPUT_CHAR_MAP.values() + ['@'])))
CHAR_MAP = {c: i for i, c in enumerate(INDEX_MAP)}

# Number of typewriter chars (40 in the assignment).
NUM_CHARS = len(INDEX_MAP)

# Use INPUT_CHAR_MAP to map any input char into the NUM_CHARS typewriter chars
# (if a char is not found in INPUT_CHAR_MAP it is mapped to @).
translate_input_char = lambda c: INPUT_CHAR_MAP.get(c.lower(), '@')

# Assign consecutive integers to every typewriter char (ASCII order).
char_to_index = lambda c: CHAR_MAP[c]

# The inverse of char_to_index.
index_to_char = lambda i: INDEX_MAP[i]


# This assumes that the files in corpus_files fit in main memory 
# one at a time -- which makes sense for the assignment.
def freq_tab_creation(order, *corpus_files):
    freq_tab = _freq_tab_init(order)
    if order > 0:
        for corpus_file in corpus_files:
            fd = open(corpus_file, 'r')
            text = fd.read()
            input_ngram_seqs = [islice(text, i, None) for i in xrange(order)]
            for input_ngram in izip(*input_ngram_seqs):
                typewriter_ngram = map(translate_input_char, input_ngram)
                _freq_tab_inc(freq_tab, map(char_to_index, typewriter_ngram))
            fd.close()
    return freq_tab


# Reduce the resolution of the typewriter -- i.e. reduce the freqs in the 
# table by the ratio given in factor. The original freq table is modified!
def freq_tab_resolution(freq_tab, factor):
    order = _freq_tab_order(freq_tab)
    for ngram_index in product(xrange(NUM_CHARS), repeat=order):
        ngram_freq = _freq_tab_get(freq_tab, ngram_index)
        if ngram_freq > 0:
            ngram_freq = int(factor * ngram_freq)
            _freq_tab_set(freq_tab, ngram_index, ngram_freq)


# Export all the ngrams with non-zero freqs to a JSON file.
def freq_tab_write(freq_tab, output_file):
    nonzero_ngrams = {}
    order = _freq_tab_order(freq_tab)
    for ngram_index in product(xrange(NUM_CHARS), repeat=order):
        ngram_freq = _freq_tab_get(freq_tab, ngram_index)
        if ngram_freq > 0:
            ngram = ''.join(map(index_to_char, ngram_index))
            nonzero_ngrams[ngram] = ngram_freq
    fd = open(output_file, 'w')
    dump(nonzero_ngrams, fd)
    fd.close()


# Read the freq table from the ngram freqs in a JSON file.
def freq_tab_read(input_file):
    fd = open(input_file, 'r')
    nonzero_ngrams = load(fd)
    fd.close()
    order = len(nonzero_ngrams.iterkeys().next())
    freq_tab = _freq_tab_init(order)
    for ngram, ngram_freq in nonzero_ngrams.iteritems():
        _freq_tab_set(freq_tab, map(char_to_index, ngram), ngram_freq)
    return freq_tab


def freq_tab_most_probable_path(freq_tab, ngram_prefix, max_chars):
    pass


# Sample num_chars chars from the freq table and save them to output_file.
# Set freq_tab to None for the straightforward monkey problem.
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
                # The first (order - 1) chars are sampled uniformly.
                char_index = randint(0, NUM_CHARS - 1)
                ngram_prefix.append(char_index)
            else:
                # Sample according to the freq table.
                char_index = _freq_tab_sample(freq_tab, ngram_prefix)
                ngram_prefix.append(char_index)
                ngram_prefix.popleft()
        fd.write(index_to_char(char_index))
    fd.close()


def relative_word_yield(simulated_file, corpus_file):
    word_yield = 0
    corpus_words = _get_words(corpus_file)
    for word in _get_words(simulated_file):
        if word in corpus_words:
            word_yield += 1
    relative_word_yield = word_yield / float(len(corpus_words))
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


# Get the freq of an n-gram given the (ordered) indexes of its chars.
def _freq_tab_get(freq_tab, ngram_index):
    tab_ref = freq_tab
    for n, i in enumerate(ngram_index):
        if n == len(ngram_index) - 1:
            return tab_ref[i]
        else:
            tab_ref = tab_ref[i]


# Update the freq of an n-gram given the (ordered) indexes of its chars.
def _freq_tab_set(freq_tab, ngram_index, ngram_freq):
    tab_ref = freq_tab
    for n, i in enumerate(ngram_index):
        if n == len(ngram_index) - 1:
            tab_ref[i] = ngram_freq
        else:
            tab_ref = tab_ref[i]


# Increment by 1 the freq of an n-gram given the (ordered) indexes of its chars.
def _freq_tab_inc(freq_tab, ngram_index):
    tab_ref = freq_tab
    for n, i in enumerate(ngram_index):
        if n == len(ngram_index) - 1:
            tab_ref[i] += 1
        else:
            tab_ref = tab_ref[i]


# Sample a char from the freq table given the (order - 1) chars in the n-gram prefix.
def _freq_tab_sample(freq_tab, ngram_prefix):
    # Compute the cumulative values of the freq distribution.
    cumul_sum, cumul_freqs = 0, []
    tab_ref = freq_tab
    for i in ngram_prefix:
        tab_ref = tab_ref[i]
    for i in xrange(NUM_CHARS):
        cumul_sum += tab_ref[i]
        cumul_freqs.append(cumul_sum)
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
    translated_text = ''.join((translate_input_char(char) for char in fd.read()))
    fd.close()
    words = split('[' + split_chars + ']+', translated_text.strip(split_chars))
    return set(words)
