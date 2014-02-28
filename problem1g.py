from monkeys import compute_freq_tab, cng_profile, cng_dissimilarity

training_corpus = {
    'C. Dickens': ('books/tale_of_2_cities.txt', ),
    'E. R. Burroughs': (
        'books/warlord_of_mars.txt', 
        'books/the_people_that_time_forgot.txt', 
        'books/the_land_that_time_forgot.txt'),
    'L. Carroll': ('books/through_the_looking_glass.txt', ),
    'Sir A. C. Doyle': (
        'books/the_lost_world.txt', 
        'books/the_hound_of_the_baskervilles.txt', 
        'books/tales_of_terror_and_mystery.txt'),
    'M. Twain': (
         'books/the_adventures_of_tom_sawyer.txt', 
         'books/a_connecticut_yankee_in_king_arthur_s_court.txt'),
    'H. G. Wells': ('books/the_time_machine.txt', ),
    'F. Kafka': ('books/the_trial.txt', )
}

testing_corpus = {
    'C. Dickens': 'books/christmas_carol.txt',
    'E. R. Burroughs': 'books/tarzan_of_the_apes.txt',
    'L. Carroll': 'books/alices_adventures_in_wonderland.txt',
    'Sir A. C. Doyle': 'books/the_adventures_of_sherlock_holmes.txt',
    'M. Twain': 'books/adventures_of_huckleberry_finn.txt',
    'H. G. Wells': 'books/war_of_the_worlds.txt',
    'F. Kafka': 'books/metamorphosis.txt'
}

for profile_len in (10, 100, 500):
    # Build the author's profiles database.
    profiles = {}
    for author, book_paths in training_corpus.iteritems():
        freq_tab = compute_freq_tab(3, *book_paths)
        profiles[author] = cng_profile(freq_tab, profile_len)
    # Predict the authors of the books in the test corpus.
    for author, book_path in testing_corpus.iteritems():
        freq_tab = compute_freq_tab(3, book_path)
        profile = cng_profile(freq_tab, profile_len)
        # Assign the closest profile from the database.
        pred_author, min_dissim = None, None
        for cand_author, cand_profile in profiles.iteritems():
            dissim = cng_dissimilarity(profile, cand_profile)
            if pred_author is None or dissim < min_dissim:
                pred_author, min_dissim = cand_author, dissim
        print '%s,%s,%s' % (profile_len, author, pred_author)

