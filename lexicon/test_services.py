import random

from lexicon.tests.grid_test import GridTest
from lexicon.tests.tests import EnglishFromSound4, EnglishFromSound6, ThaiFromSound6, ThaiFromSound4, EnglishFromThai6, \
    EnglishFromThai4


def pick_sentence(al, chosen_word, learning=False, test_success_callback=None):
    """
    Returns TappingTestSentence or None if no sentence
    """
    from lexicon.tests.tapping_test_sentence import TappingTestSentence
    can_be_selected_sentences = []
    for sentence in chosen_word.sentences:
        sentence_can_be_learnt = True
        for word in sentence.words:
            if word.total_xp < 5:
                sentence_can_be_learnt = False
        if sentence_can_be_learnt:
            can_be_selected_sentences.append(sentence)
    if len(can_be_selected_sentences) > 0:
        sentence = random.choice(can_be_selected_sentences)
        test = TappingTestSentence(al, correct_word=chosen_word, sentence=sentence, learning=learning, test_success_callback=test_success_callback)
    else:
        test = None
    return test


def pick_a_test_for_word(al, chosen_word):
    # test = None
    # can_be_tested_on_sentence = True
    # while test is None:
    #     r = random.randint(0, 20)  # can be 0, ..., n-1   (15)
    #     from lexicon.tests.tests import ThaiFromEnglish6, ThaiFromEnglish4
    #     if r == 0:
    #         test = ThaiFromEnglish4(al, correct_word=chosen_word)
    #     elif r == 1:
    #         test = ThaiFromEnglish6(al, correct_word=chosen_word)
    #     elif r == 2:
    #         test = EnglishFromSound4(al, correct_word=chosen_word)
    #     elif r == 3:
    #         test = EnglishFromSound6(al, correct_word=chosen_word)
    #     elif r == 4:
    #         test = ThaiFromSound4(al, correct_word=chosen_word)
    #     elif r == 5:
    #         test = ThaiFromSound6(al, correct_word=chosen_word)
    #     elif r == 6:
    #         test = EnglishFromThai4(al, correct_word=chosen_word)
    #     elif r == 7:
    #         test = EnglishFromThai6(al, correct_word=chosen_word)
    #     else:
    #         if can_be_tested_on_sentence:
    #             test = pick_sentence(al, chosen_word)
    #             if not test:
    #                 can_be_tested_on_sentence = False
    # al.active_test = test
    al.active_test = GridTest(al, correct_word=chosen_word, sentence=chosen_word.sentences[0])


def pick_a_test_for_thai_word(al, chosen_word, test_success_callback=None) -> None:
    """
    Here, the learner saw the word in thai already,
    so we don't want to ask the Thai word from English, for example
    """
    # test = None
    # can_be_tested_on_sentence = True
    # while test is None:
    #     r = random.randint(0, 20)  # can be 0, ..., n-1
    #     if r == 0:
    #         test = EnglishFromSound4(al, correct_word=chosen_word, test_success_callback=test_success_callback)
    #     elif r == 1:
    #         test = EnglishFromSound6(al, correct_word=chosen_word, test_success_callback=test_success_callback)
    #     elif r == 2:
    #         test = EnglishFromThai4(al, correct_word=chosen_word, test_success_callback=test_success_callback)
    #     elif r == 3:
    #         test = EnglishFromThai6(al, correct_word=chosen_word, test_success_callback=test_success_callback)
    #     else:
    #         if can_be_tested_on_sentence:
    #             test = pick_sentence(al, chosen_word, test_success_callback=test_success_callback)
    #             if not test:
    #                 can_be_tested_on_sentence = False
    # al.active_test = test
    al.active_test = GridTest(al, correct_word=chosen_word, sentence=chosen_word.sentences[0])


def pick_a_test_for_english_word(al, chosen_word, test_success_callback=None):
    """
    Here, the learner saw the word in english already,
    so we don't want to ask the English word from Thai, for example
    """
    test = None
    can_be_tested_on_sentence = True
    while test is None:
        r = random.randint(0, 20)  # can be 0, ..., n-1
        from lexicon.tests.tests import ThaiFromEnglish6, ThaiFromEnglish4
        if r == 0:
            test = ThaiFromEnglish4(al, correct_word=chosen_word, test_success_callback=test_success_callback)
        elif r == 1:
            test = ThaiFromEnglish6(al, correct_word=chosen_word, test_success_callback=test_success_callback)
        elif r == 2:
            test = ThaiFromSound4(al, correct_word=chosen_word, test_success_callback=test_success_callback)
        elif r == 3:
            test = ThaiFromSound6(al, correct_word=chosen_word, test_success_callback=test_success_callback)
        else:
            if can_be_tested_on_sentence:
                test = pick_sentence(al, chosen_word, test_success_callback=test_success_callback)
                if not test:
                    can_be_tested_on_sentence = False
    al.active_test = test
