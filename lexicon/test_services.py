import random

from lexicon.tests import EnglishFromSound4, EnglishFromSound6


def pick_sentence(al, chosen_word, learning=False):
    from lexicon.tests import TappingTestSentence
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
        test = TappingTestSentence(al, correct_word=chosen_word, sentence=sentence, learning=learning)
    else:
        test = None
    return test


def pick_a_test_for_word(al, chosen_word):
    test = None
    can_be_tested_on_sentence = True
    while test is None:
        r = random.randint(0, 100)  # can be 0, ..., n-1
        from lexicon.tests import ThaiFromEnglish6, ThaiFromEnglish4
        if r == 0:
            test = ThaiFromEnglish4(al, correct_word=chosen_word)
        elif r == 1:
            test = ThaiFromEnglish6(al, correct_word=chosen_word)
        elif r == 2:
            test = EnglishFromSound4(al, correct_word=chosen_word)
        elif r == 3:
            test = EnglishFromSound6(al, correct_word=chosen_word)
        else:
            test = EnglishFromSound6(al, correct_word=chosen_word)
            # if can_be_tested_on_sentence:
            #     test = pick_sentence(al, chosen_word)
            #     if not test:
            #         can_be_tested_on_sentence = False
    al.active_test = test
