import pygame
from enum import Enum

from all import All
from lexicon.test_services import pick_sentence
from lexicon.tests import ThaiFromEnglish4, ThaiFromEnglish6, TappingTestSentence
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
    def __init__(self, word, al, npc):
        self.al = al
        self.word = word
        self.step = LearningStep.NONE
        self.test_1 = ThaiFromEnglish4(al, correct_word=word, learning=self)
        self.test_2 = ThaiFromEnglish4(al, correct_word=word, learning=self)  # TODO
        self.test_3 = ThaiFromEnglish6(al, correct_word=word, learning=self)
        self.test_4 = ThaiFromEnglish4(al, correct_word=word, learning=self)  # TODO
        # self.test_5 = TappingTestSentence(al, correct_word=word, learning=self)
        # test_5 is a sentence if possible, a Thai from English 6 otherwise
        self.test_5 = pick_sentence(al, word, learning=self)
        if not self.test_5:
            self.test_5 = ThaiFromEnglish6(al, correct_word=word, learning=self)
        self.npc = npc
        play_transformed_thai_word(self.word.thai)

    def draw_presentation_screen(self):
        ui = self.al.ui
        x = ui.percent_width(0.1)
        y = ui.percent_height(0.1)
        height = ui.percent_height(0.8)
        width = ui.percent_width(0.8)

        screen = ui.screen
        pygame.draw.rect(screen, (150, 150, 150), (x, y, width, height))
        pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)

        # Draw Thai word
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        screen.blit(
            self.al.ui.fonts.garuda64.render(self.word.thai, True, (0, 0, 0)), (x, y)
        )

        # Draw English
        x = ui.percent_width(0.15)
        y = ui.percent_height(0.28)
        screen.blit(
            self.al.ui.fonts.garuda64.render(self.word.english, True, (0, 0, 0)), (x, y)
        )

    def draw(self):
        """
        The showing is taken care of by the tests during the test phases.
        We only need to show the phases of PRESENTATION and CONGRATULATION
        """
        if self.step == LearningStep.PRESENTATION:
            self.draw_presentation_screen()
        if self.step == LearningStep.CONGRATULATION:
            self.draw_presentation_screen()

    def interact(self, al: All):
        if self.step == LearningStep.PRESENTATION:
            if al.ui.space:
                al.ui.space = False
                al.active_test = self.test_1
                self.step = LearningStep.TEST1
        if self.step == LearningStep.CONGRATULATION:
            if al.ui.space:
                self.step = LearningStep.END
                al.ui.space = False
                al.active_test = None
                al.active_learning = None
                if self.npc.dialog_1:
                    al.active_npc = self.npc
                    al.active_npc.switch_to_dialog(al.active_npc.dialog_1)

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
