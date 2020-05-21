from enum import Enum
from lexicon.tests.tests import (
    SoundFromThai4, ToneFromThaiAndSound, EnglishFromThai6)


# The 6 steps in a Learning
from lexicon.tests.typing_test import TypingTestFromEnglish


class IdentificationStep(Enum):
    NONE = 0
    STEP_1 = 1  # get audio
    STEP_2 = 2  # get tone
    STEP_3 = 3  # get meaning
    STEP_4 = 4  # type
    INTERMISSION = 5
    FIGHT = 6


class SpellIdentification(object):
    """
    First, the player has to identify the spell - the first 4 tests
    Then, using sentences, the player lowers the HP of the Spell
    Finally, the player can catch the Spell, or dismiss it
    """
    def __init__(self, al, spell):
        self.al = al
        self.spell = spell
        self.word = spell.word
        self.step = IdentificationStep.STEP_1

        self.test_1 = SoundFromThai4(al, correct=self.word, learning=self)
        self.test_2 = None
        self.test_3 = None
        self.test_4 = None
        # self.test_5 = TappingTestSentence(al, correct_word=word, learning=self)
        # test_5 is a sentence if possible, a Thai from English 6 otherwise
        # self.test_5 = pick_sentence_test(al, word, learning=self)
        # if not self.test_5:
        #     self.test_5 = ThaiFromEnglish6(al, correct=word, learning=self)

        self.al.active_test = self.test_1

    def test_finished(self, failed=False):
        """this is triggered by the test when it ends"""
        if failed:
            self.step = IdentificationStep.PRESENTATION
            self.al.active_test = None
        else:
            self.goes_to_next_step()
            if self.step == IdentificationStep.STEP_2:
                self.test_2 = ToneFromThaiAndSound(self.al, correct=self.word, learning=self)
                self.al.active_test = self.test_2
            if self.step == IdentificationStep.STEP_3:
                self.test_3 = EnglishFromThai6(self.al, correct=self.word, learning=self)
                self.al.active_test = self.test_3
            if self.step == IdentificationStep.STEP_4:
                self.test_4 = TypingTestFromEnglish(self.al, correct=self.word, learning=self)
                self.al.active_test = self.test_4

    def draw(self):
        """
        The drawing of the tests is taken care of by the tests during the test phases.
        """
        self.draw_brain()

    def draw_brain(self):
        x = self.al.ui.width - 230
        y = 100
        if self.step == IdentificationStep.STEP_1:
            self.al.ui.screen.blit(self.al.ui.images["brain_0"], [x, y])
        elif self.step == IdentificationStep.STEP_2:
            self.al.ui.screen.blit(self.al.ui.images["brain_2"], [x, y])
        elif self.step == IdentificationStep.STEP_3:
            self.al.ui.screen.blit(self.al.ui.images["brain_4"], [x, y])
        elif self.step == IdentificationStep.STEP_4:
            self.al.ui.screen.blit(self.al.ui.images["brain_6"], [x, y])

    def interact(self, al):
        # if self.step == IdentificationStep.NONE:
        #     if al.ui.space:
        #         al.ui.space = False
        #         al.active_test = self.test_1
        #         self.step = IdentificationStep.STEP_1
        #     elif al.active_presentation:
        #         al.active_presentation.interact()
        # if self.step == LearningStep.CONGRATULATION:
        #     if al.ui.space:
        #         self.step = LearningStep.END
        #         al.ui.space = False
        #         al.active_test = None
        #         al.active_learning = None
        #         al.active_presentation = None
        #         if self.npc.defeat_dialog:
        #             al.active_npc = self.npc
        #             al.active_npc.switch_to_dialog(al.active_npc.defeat_dialog)
        #     elif al.active_presentation:
        #         al.active_presentation.interact()
        if self.al.ui.escape:
            al.active_learning = None
            self.al.ui.escape = False

    def goes_to_next_step(self):
        a = self.step.value
        b = int(self.step.value) + 1
        c = IdentificationStep(int(self.step.value) + 1)
        self.step = IdentificationStep(int(self.step.value) + 1)
