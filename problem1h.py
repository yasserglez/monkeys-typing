from itertools import combinations

from monkeys import compute_freq_tab, cng_profile, cng_dissimilarity

corpus = (
    'books/christmas_carol.txt', 
    'books/tale_of_2_cities.txt',
    'books/wuthering_heights.txt',
    'books/agnes_grey.txt',
    'books/jane_eyre.txt',
    'books/tarzan_of_the_apes.txt', 
    'books/warlord_of_mars.txt',
    'books/the_people_that_time_forgot.txt',
    'books/the_land_that_time_forgot.txt',
    'books/king_solomons_mines.txt',
    'books/fanny_hill.txt',
    'books/alices_adventures_in_wonderland.txt', 
    'books/through_the_looking_glass.txt',
    'books/legend_of_sleepy_hollow.txt',
    'books/the_adventures_of_sherlock_holmes.txt', 
    'books/the_lost_world.txt', 
    'books/the_hound_of_the_baskervilles.txt', 
    'books/tales_of_terror_and_mystery.txt',
    'books/adventures_of_huckleberry_finn.txt', 
    'books/the_adventures_of_tom_sawyer.txt',
    'books/a_connecticut_yankee_in_king_arthur_s_court.txt',
    'books/the_prince.txt',
    'books/war_of_the_worlds.txt', 
    'books/the_time_machine.txt',
    'books/metamorphosis.txt', 
    'books/the_trial.txt',
    'books/the_jungle_book.txt'
)

# Build the book's profile database.
profiles = []
for book_path in corpus:
    freq_tab = compute_freq_tab(3, book_path)
    profiles.append(cng_profile(freq_tab, 500))

# Compute the pairwise dissimilarities.
for book_data_i, book_data_j in combinations(enumerate(corpus), 2):
    i, book_path_i = book_data_i
    j, book_path_j = book_data_j
    profile_i, profile_j = profiles[i], profiles[j]
    dissim = cng_dissimilarity(profile_i, profile_j)
    print '%s,%s,%s' % (i + 1, j + 1, dissim)
