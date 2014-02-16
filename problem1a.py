from monkeys import simulate_freq_tab, relative_word_yield

selected_books = (
    ('christmas_carol.txt', 168925),
    ('wuthering_heights.txt', 662869),
    ('agnes_grey.txt', 384300),
    ('jane_eyre.txt', 1051336),
    ('tarzan_of_the_apes.txt', 492783),
    ('king_solomons_mines.txt', 454437),
    ('fanny_hill.txt', 474725),
    ('alices_adventures_in_wonderland.txt', 148580),
    ('legend_of_sleepy_hollow.txt', 69164),
    ('the_adventures_of_sherlock_holmes.txt', 575574),
    ('adventures_of_huckleberry_finn.txt', 578345),
    ('the_prince.txt', 286854),
    ('war_of_the_worlds.txt', 346458),
    ('metamorphosis.txt', 122139),
    ('the_jungle_book.txt', 279771)
)

for book_file, book_chars in selected_books:
    rates = []
    for i in xrange(30):
        simulate_freq_tab(None, book_chars, 'tmp.txt')
        rate = relative_word_yield('tmp.txt', 'books/' + book_file)
        rates.append(rate)
    print book_file, sum(rates) / float(len(rates))
