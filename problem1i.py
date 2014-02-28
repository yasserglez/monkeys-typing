from itertools import combinations
from monkeys import compute_freq_tab, cng_profile, cng_dissimilarity

corpus = {
    'C. Dickens': (
        'books/christmas_carol.txt', 
        'books/tale_of_2_cities.txt'),
    'E. Bronte': ('books/wuthering_heights.txt', ),
    'A. Bronte': ('books/agnes_grey.txt', ),
    'C. Bronte': ('books/jane_eyre.txt', ),
    'E. R. Burroughs': (
        'books/tarzan_of_the_apes.txt', 
        'books/warlord_of_mars.txt',
        'books/the_people_that_time_forgot.txt',
        'books/the_land_that_time_forgot.txt', ),
    'H. R. Haggard': ('books/king_solomons_mines.txt', ),
    'J. Cleland': ('books/fanny_hill.txt', ),
    'L. Carroll': (
        'books/alices_adventures_in_wonderland.txt', 
        'books/through_the_looking_glass.txt'),
    'W. Irving': ('books/legend_of_sleepy_hollow.txt', ),
    'Sir A. C. Doyle': (
        'books/the_adventures_of_sherlock_holmes.txt', 
        'books/the_lost_world.txt', 
        'books/the_hound_of_the_baskervilles.txt', 
        'books/tales_of_terror_and_mystery.txt'),
    'M. Twain': (
        'books/adventures_of_huckleberry_finn.txt', 
        'books/the_adventures_of_tom_sawyer.txt',
        'books/a_connecticut_yankee_in_king_arthur_s_court.txt'),
    'N. Machiavelli': ('books/the_prince.txt', ),
    'H. G. Wells': (
        'books/war_of_the_worlds.txt', 
        'books/the_time_machine.txt'),
    'F. Kafka': (
        'books/metamorphosis.txt', 
        'books/the_trial.txt'),
    'R. Kipling': ('books/the_jungle_book.txt', )
}

# Build the author's profile database.
profiles = {}
for author, book_paths in corpus.iteritems():
    freq_tab = compute_freq_tab(3, *book_paths)
    profiles[author] = cng_profile(freq_tab, 500)

# Compute the pairwise dissimilarities.
for author1, author2 in combinations(profiles.iterkeys(), 2):
    profile1, profile2 = profiles[author1], profiles[author2]
    dissim = cng_dissimilarity(profile1, profile2)
    print '%s,%s,%s' % (author1, author2, dissim)
