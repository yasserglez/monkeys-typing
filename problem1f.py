from monkeys import compute_freq_tab, most_probable_freq_tab_path

corpus = (
    'books/christmas_carol.txt',
    'books/wuthering_heights.txt',
    'books/agnes_grey.txt',
    'books/jane_eyre.txt',
    'books/tarzan_of_the_apes.txt',
    'books/king_solomons_mines.txt',
    'books/fanny_hill.txt',
    'books/alices_adventures_in_wonderland.txt',
    'books/legend_of_sleepy_hollow.txt',
    'books/the_adventures_of_sherlock_holmes.txt',
    'books/adventures_of_huckleberry_finn.txt',
    'books/the_prince.txt',
    'books/war_of_the_worlds.txt',
    'books/metamorphosis.txt',
    'books/the_jungle_book.txt',
)

for book_path in corpus:
    freq_tab = compute_freq_tab(2, book_path)
    path_2nd_order = most_probable_freq_tab_path(freq_tab, 't')
    freq_tab = compute_freq_tab(3, book_path)
    path_3rd_order = most_probable_freq_tab_path(freq_tab, 'th')
    print book_path, path_2nd_order, path_3rd_order