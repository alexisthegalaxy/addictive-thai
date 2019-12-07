from enum import Enum
from typing import Union

from lexicon.items import Word, Letter
from lexicon.presentation import LetterPresentation, WordPresentation
from lexicon.test_services import pick_sentence_test
from lexicon.tests.tests import ThaiFromEnglish4, ThaiFromEnglish6, ThaiLetterFromEnglish4
from sounds.play_sound import play_transformed_thai_word


# The 6 steps in a Learning
class LearningStep(Enum):
    NONE = 0
    PRESENTATION = 1
    TEST1 = 2  # THAIFROMENGLISH4
    TEST2 = 3  # Get the tone right
    TEST3 = 4  # THAIFROMENGLISH6
    TEST4 = 5  # TYPING
    TEST5 = 6  # Sentence / THAIFROMENGLISH6
    CONGRATULATION = 7
    END = 8


class Learning(object):
    def draw(self):
        """
        The showing is taken care of by the tests during the test phases.
        We only need to show the phases of PRESENTATION and CONGRATULATION
        """
        if self.step == LearningStep.PRESENTATION:
            if self.al.active_presentation:
                self.al.active_presentation.draw()
        if self.step == LearningStep.CONGRATULATION:
            if self.al.active_presentation:
                self.al.active_presentation.draw()
        self.draw_brain()

    def draw_brain(self):
        x = self.al.ui.width - 230
        y = 100
        if self.step == LearningStep.PRESENTATION:
            self.al.ui.screen.blit(self.al.ui.images["brain_0"], [x, y])
        elif self.step == LearningStep.TEST1:
            self.al.ui.screen.blit(self.al.ui.images["brain_1"], [x, y])
        elif self.step == LearningStep.TEST2:
            self.al.ui.screen.blit(self.al.ui.images["brain_2"], [x, y])
        elif self.step == LearningStep.TEST3:
            self.al.ui.screen.blit(self.al.ui.images["brain_3"], [x, y])
        elif self.step == LearningStep.TEST4:
            self.al.ui.screen.blit(self.al.ui.images["brain_4"], [x, y])
        elif self.step == LearningStep.TEST5:
            self.al.ui.screen.blit(self.al.ui.images["brain_5"], [x, y])
        elif self.step == LearningStep.CONGRATULATION:
            self.al.ui.screen.blit(self.al.ui.images["brain_6"], [x, y])

    def interact(self, al):
        if self.step == LearningStep.PRESENTATION:
            if al.ui.space:
                al.ui.space = False
                al.active_test = self.test_1
                self.step = LearningStep.TEST1
            elif al.active_presentation:
                al.active_presentation.interact()
        if self.step == LearningStep.CONGRATULATION:
            if al.ui.space:
                self.step = LearningStep.END
                al.ui.space = False
                al.active_test = None
                al.active_learning = None
                al.active_presentation = None
                if self.npc.defeat_dialog:
                    al.active_npc = self.npc
                    al.active_npc.switch_to_dialog(al.active_npc.defeat_dialog)
            elif al.active_presentation:
                al.active_presentation.interact()
        if self.al.ui.escape:
            al.active_learning = None
            self.al.ui.escape = False

    def goes_to_next_step(self):
        self.step = LearningStep(int(self.step.value) + 1)

    def goes_to_first_step(self):
        self.step = LearningStep.PRESENTATION

    def test_finished(self, failed=False):
        """this is triggered by the test when it ends"""
        if failed:
            self.step = LearningStep.PRESENTATION
            self.al.active_test = None
        else:
            self.goes_to_next_step()
            if self.step == LearningStep.TEST2:
                self.al.active_test = self.test_2
            if self.step == LearningStep.TEST3:
                self.al.active_test = self.test_3
            if self.step == LearningStep.TEST4:
                self.al.active_test = self.test_4
            if self.step == LearningStep.TEST5:
                self.al.active_test = self.test_5


class WordLearning(Learning):
    def __init__(self, word: Union[Word, Letter], al, npc):
        self.al = al
        self.word = word
        self.npc = npc
        self.step = LearningStep.NONE

        self.al.active_presentation = WordPresentation(al, word, from_learning=True)
        self.test_1 = ThaiFromEnglish4(al, correct_word=word, learning=self)
        self.test_2 = ThaiFromEnglish4(al, correct_word=word, learning=self)  # TODO
        self.test_3 = ThaiFromEnglish6(al, correct_word=word, learning=self)
        self.test_4 = ThaiFromEnglish4(al, correct_word=word, learning=self)  # TODO
        # self.test_5 = TappingTestSentence(al, correct_word=word, learning=self)
        # test_5 is a sentence if possible, a Thai from English 6 otherwise
        self.test_5 = pick_sentence_test(al, word, learning=self)
        if not self.test_5:
            self.test_5 = ThaiFromEnglish6(al, correct_word=word, learning=self)

        play_transformed_thai_word(self.word.thai)


class LetterLearning(Learning):
    def __init__(self, letter: Letter, al, npc):
        self.al = al
        self.letter = letter
        self.npc = npc
        self.step = LearningStep.NONE

        self.al.active_presentation = LetterPresentation(al, letter, from_learning=True)
        self.test_1 = ThaiLetterFromEnglish4(al, correct=letter, learning=self)
        self.test_2 = ThaiLetterFromEnglish4(al, correct=letter, learning=self)
        self.test_3 = ThaiLetterFromEnglish4(al, correct=letter, learning=self)
        self.test_4 = ThaiLetterFromEnglish4(al, correct=letter, learning=self)
        self.test_5 = ThaiLetterFromEnglish4(al, correct=letter, learning=self)
        # self.test_2 = EnglishLetterFromThai4(al, learning=self)
        # self.test_3 = EnglishLetterFromThai16(al, learning=self)
        # self.test_4 = ThaiLetterFromEnglish16(al, correct=letter, learning=self)
        # self.test_5 = ThaiLetterFromSound(al, letter, learning=self)
        # if not self.test_5:
        #     self.test_5 = ThaiLetterFromEnglish6(al, correct=letter, learning=self)
        play_transformed_thai_word(self.letter.thai)
