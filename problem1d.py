from monkeys import (compute_freq_tab, freq_tab_resolution,
                     simulate_freq_tab, relative_word_yield)

corpus = (
    ('books/legend_of_sleepy_hollow.txt', 69164),
    ('books/agnes_grey.txt', 384300),
    ('books/jane_eyre.txt', 1051336)
)

for book_path, book_chars in corpus:
    for order in (1, 2, 3):
        orig_freq_tab = compute_freq_tab(order, book_path)
        for factor in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
            freq_tab = freq_tab_resolution(orig_freq_tab, factor)
            rates = []
            for i in xrange(30):
                simulate_freq_tab(freq_tab, book_chars, 'tmp.txt')
                rate = relative_word_yield('tmp.txt', book_path)
                rates.append(rate)
            avg_rate = sum(rates) / float(len(rates))
            print ','.join([book_path, order, factor, avg_rate])
