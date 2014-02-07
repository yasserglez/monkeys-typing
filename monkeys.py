import copy


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
    # WARNING: This assumes that the files in 'corpus_files' fit in main memory 
    # one at a time -- which makes sense for the assignment.
    freq_tab = _init_freq_tab(order)
    for corpus_file in corpus_files:
        with open(corpus_file, 'r') as fd:
            text = fd.read()
            for i in xrange(len(text) - order + 1):
                chars = text[i:i + order]
                tab_ref = freq_tab
                for k, char in enumerate(chars):
                    index = char2index(char)
                    if k == order - 1:
                        tab_ref[index] += 1
                    else:
                        tab_ref = tab_ref[index]
    return freq_tab


def write_freq_tab(order, freq_tab, output_file):
    pass


def read_freq_tab(input_file):
    pass


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


# Initialize a freq. table with all counts set to 'value'.
def _init_freq_tab(order, value=0):
    prev_tab = [value] * NUM_CHARS
    for n in xrange(1, order):
        tab = [prev_tab]
        tab += [copy.deepcopy(prev_tab) for i in xrange(NUM_CHARS - 1)] 
        prev_tab = tab
    return prev_tab
