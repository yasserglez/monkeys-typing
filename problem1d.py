from monkeys import (compute_freq_tab, reduce_freq_tab_resolution, 
                     simulate_freq_tab, relative_word_yield)

book_path, book_chars = 'books/agnes_grey.txt', 384300

for order in (1, 2, 3):
    orig_freq_tab = compute_freq_tab(order, book_path)
    for rate in (0.1 * k for k in xrange(11)):
        freq_tab = reduce_freq_tab_resolution(orig_freq_tab, rate)
        simulate_freq_tab(freq_tab, 10 * book_chars, 'tmp.txt')
        word_yield = relative_word_yield('tmp.txt', book_path)
        print '%s,%s,%s' % (order, rate, word_yield)
