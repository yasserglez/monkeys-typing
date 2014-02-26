from monkeys import compute_freq_tab, write_freq_tab

freq_tab_2nd_order = compute_freq_tab(2, 'books/agnes_grey.txt')
write_freq_tab(freq_tab_2nd_order, 'agnes_grey_2nd_order.json')

freq_tab_3rd_order = compute_freq_tab(3, 'books/agnes_grey.txt')
write_freq_tab(freq_tab_3rd_order, 'agnes_grey_3rd_order.json')
