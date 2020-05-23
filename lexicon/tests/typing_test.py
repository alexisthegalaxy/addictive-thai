from lexicon.items import Word
from lexicon.tests.tests import ThaiFromEnglish
from ui.keyboard import Keyboard


class TypingTestFromEnglish(ThaiFromEnglish):
    def __init__(
        self, al: "All", correct: Word, learning=None, test_success_callback=None, test_failure_callback=None,
    ):
        super().__init__(al, correct, learning, test_success_callback, test_failure_callback)
        self.number_of_distr: int = 5
        self.keyboard = Keyboard(ui=al.ui)
        self.answer = ""

    def draw(self):
        ui = self.al.ui
        screen = ui.screen
        fonts = ui.fonts

        # Draw the background
        self.draw_background()

        # Draw "What's the Thai word for"
        explanatory_string = "What's the Thai word for:"
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        screen.blit(fonts.sarabun32.render(explanatory_string, True, (0, 0, 0)), (x, y))

        # Draw prompt
        x = ui.percent_width(0.15)
        y = ui.percent_height(0.18)
        screen.blit(
            fonts.sarabun32.render(self.correct.english, True, (0, 0, 0)), (x, y)
        )

        # Draw answer
        x = ui.percent_width(0.2)
        y = ui.percent_height(0.3)
        screen.blit(
            fonts.sarabun48.render(self.answer, True, (0, 0, 0)), (x, y)
        )

        if self.al.ui.is_shift():
            screen.blit(ui.images["shift_keyboard"], [self.keyboard.x, self.keyboard.y])
        else:
            screen.blit(ui.images["default_keyboard"], [self.keyboard.x, self.keyboard.y])

    def add_letter(self, value):
        self.answer += value

    def validate_answer(self):
        if self.answer == self.correct.thai:
            print('success')
            self.al.active_test = None
            self.al.active_spell_identification = None
            self.al.active_npc.gets_caught()
        else:
            print('failure!', self.answer, self.correct.thai)

    def interact(self, al):
        if al.ui.enter:
            al.ui.enter = False
            self.validate_answer()
        self.keyboard.interact(self, al)

