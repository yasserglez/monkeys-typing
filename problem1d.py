from monkeys import (compute_freq_tab, reduce_freq_tab_resolution, 
                     simulate_freq_tab, relative_word_yield, 
                     unique_word_yield)

book_path, book_chars = 'books/agnes_grey.txt', 384300

for order in (1, 2, 3):
    orig_freq_tab = compute_freq_tab(order, book_path)
    for factor in (0.1 * k for k in xrange(11)):
        freq_tab = reduce_freq_tab_resolution(orig_freq_tab, factor)
        simulate_freq_tab(freq_tab, 10 * book_chars, 'tmp.txt')
        relative = relative_word_yield('tmp.txt', book_path)
        unique = unique_word_yield('tmp.txt', book_path)
        print '%s,%s,%s,%s' % (order, factor, relative, unique)
