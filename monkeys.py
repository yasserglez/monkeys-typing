
from copy import deepcopy
from itertools import islice, izip, product
from json import dump, load


LETTERS = {l: l for l in 'abcdefghijklmnopqrstuvwxyz'}
DIGITS = {d: '#' for d in '0123456789'}
PUNCT_MARKS = {p: p for p in ' ,.;:?!()-\'"'}
INPUT_CHAR_MAP = dict(LETTERS.items() + DIGITS.items() + PUNCT_MARKS.items())
del LETTERS, DIGITS, PUNCT_MARKS

INDEX_MAP = ''.join(sorted(set(INPUT_CHAR_MAP.values() + ['@'])))
CHAR_MAP = {c: i for i, c in enumerate(INDEX_MAP)}
NUM_CHARS = len(INDEX_MAP)

# char2index uses INPUT_CHAR_MAP to map any input char into the typewriter chars
# (if a char is not found in INPUT_CHAR_MAP it is mapped to @), and then uses
# CHAR_MAP to obtain the corresponding integer (see index2char).
char2index = lambda c: CHAR_MAP[INPUT_CHAR_MAP.get(c.lower(), '@')]

# index2char assigns consecutive integers to every typewriter char (ASCII order).
index2char = lambda i: INDEX_MAP[i]


def compute_freq_tab(order, *corpus_files):
    # This assumes that the files in 'corpus_files' fit in main memory 
    # one at a time -- which makes sense for the assignment.
    freq_tab = _freq_tab_init(order)
    for corpus_file in corpus_files:
        with open(corpus_file, 'r') as fd:
            text = fd.read()
            for ngram in izip(*[islice(text, i, None) for i in xrange(order)]):
                _freq_tab_inc(freq_tab, map(char2index, ngram))
    return freq_tab


def write_freq_tab(freq_tab, output_file):
    # Export the ngrams with non-zero freqs. to a JSON file.
    nonzero_ngrams = {}
    order = _freq_tab_order(freq_tab)
    for ngram_index in product(xrange(NUM_CHARS), repeat=order):
        ngram_freq = _freq_tab_get(freq_tab, ngram_index)
        if ngram_freq > 0:
            ngram = ''.join(map(index2char, ngram_index))
            nonzero_ngrams[ngram] = ngram_freq
    with open(output_file, 'w') as fd:
        dump(nonzero_ngrams, fd)


def read_freq_tab(input_file):
    # Build the freq. table from the ngram freqs. in a JSON file.
    with open(input_file, 'r') as fd:
        nonzero_ngrams = load(fd)
    order = len(nonzero_ngrams.iterkeys().next())
    freq_tab = _freq_tab_init(order)
    for ngram, ngram_freq in nonzero_ngrams.iteritems():
        _freq_tab_set(freq_tab, map(char2index, ngram), ngram_freq)
    return freq_tab


def most_probable_digraph(freq_tab, initial_char):
    pass


def simulate(order, freq_tab, resolution, num_chars, output_file):
    pass


def relative_word_yield(sim_file, corpus_file):
    pass


def create_profile(order, freq_tab, profile_len):
    pass


def profile_dissimilarity(profile1, profile2):
    pass



def _freq_tab_init(order, value=0):
    freq_tab = [value] * NUM_CHARS
    for n in xrange(1, order):
        tmp = [freq_tab]
        tmp += [deepcopy(freq_tab) for i in xrange(NUM_CHARS - 1)] 
        freq_tab = tmp
    return freq_tab


def _freq_tab_order(freq_tab):
    order = 0
    tab_ref = freq_tab
    while isinstance(tab_ref, list):
        tab_ref = tab_ref[0]
        order += 1
    return order     


def _freq_tab_get(freq_tab, ngram_index):
    tab_ref = freq_tab
    for n, i in enumerate(ngram_index):
        if n == len(ngram_index) - 1:
            return tab_ref[i]
        else:
            tab_ref = tab_ref[i]


def _freq_tab_set(freq_tab, ngram_index, value):
    tab_ref = freq_tab
    for n, i in enumerate(ngram_index):
        if n == len(ngram_index) - 1:
            tab_ref[i] = value
        else:
            tab_ref = tab_ref[i]


def _freq_tab_inc(freq_tab, ngram_index):
    tab_ref = freq_tab
    for n, i in enumerate(ngram_index):
        if n == len(ngram_index) - 1:
            tab_ref[i] += 1
        else:
            tab_ref = tab_ref[i]
