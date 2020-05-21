from lexicon.items import Word
from lexicon.tests.tests import ThaiFromEnglish


class Key(object):
    def __init__(self, keyboard, x, y, default_letter, shift_letter, event_key_name, width=48, height=46):
        self.x = x + keyboard.x
        self.y = y + keyboard.y
        self.default_letter = default_letter
        self.shift_letter = shift_letter
        self.event_key_name = event_key_name
        self.width = width
        self.height = height

    def contains(self, point):
        x, y = point
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height


class Keyboard(object):
    def __init__(self, ui):
        self.x = ui.percent_width(0.22)
        self.y = ui.percent_height(0.52)
        self.row_1 = ["ๅ", "/", "_", "ภ", "ถ", "◌ุ", "◌ึ", "ค", "ต", "จ", "ข", "ช"]
        self.row_2 = ["ๆ", "ไ", "ำ", "พ", "ะ", "◌ั", "◌ี", "ร", "น", "ย", "บ", "ล"]
        self.row_3 = ["ฟ", "ห", "ก", "ด", "เ", "◌้", "◌่", "า", "ส", "ว", "ง", "ฃ"]
        self.row_4 = ["-", "ผ", "ป", "แ", "อ", "◌ิ", "◌ื", "ท", "ม", "ใ", "ฝ"]

        self.shift_row_1 = ["+", "๑", "๒", "๓", "๔", "◌ู", "฿", "๕", "๖", "๗", "๘", "๙"]
        self.shift_row_2 = ["๐", "\"", "ฎ", "ฑ", "ธ", "◌ํ", "◌๊", "ณ", "ฯ", "ญ", "ฐ", ","]
        self.shift_row_3 = ["ฤ", "ฆ", "ฏ", "โ", "ฌ", "◌็", "◌๋", "ษ", "ศ", "ซ", ".", "ฅ"]
        self.shift_row_4 = ["%", "(", ")", "ฉ", "ฮ", "◌ฺ", "◌์", "?", "ฒ", "ฬ", "ฦ"]

        self.keys = [
            # row 1
            Key(self, x=1, y=2, default_letter="ๅ", shift_letter=None, event_key_name="one"),
            Key(self, x=51, y=2, default_letter="/", shift_letter="￿+", event_key_name="two"),
            Key(self, x=101, y=2, default_letter="_", shift_letter="￿๑", event_key_name="three"),
            Key(self, x=152, y=2, default_letter="ภ", shift_letter="๒", event_key_name="four"),
            Key(self, x=202, y=2, default_letter="ถ", shift_letter="๓", event_key_name="five"),
            Key(self, x=253, y=2, default_letter="ุ", shift_letter="๔", event_key_name="six"),
            Key(self, x=303, y=2, default_letter="ึ", shift_letter="ู", event_key_name="seven"),
            Key(self, x=354, y=2, default_letter="ค", shift_letter="฿", event_key_name="eight"),
            Key(self, x=404, y=2, default_letter="ต", shift_letter="๖", event_key_name="nine"),
            Key(self, x=455, y=2, default_letter="จ", shift_letter="๗", event_key_name="zero"),
            Key(self, x=505, y=2, default_letter="ข", shift_letter="๘", event_key_name="minus"),
            Key(self, x=556, y=2, default_letter="ช", shift_letter="๙", event_key_name="plus"),
            Key(self, x=606, y=2, width=73, default_letter=None, shift_letter=None, event_key_name="backspace"),
            # row 2
            Key(self, x=26, y=52, default_letter="ๆ", shift_letter="๐", event_key_name="q"),
            Key(self, x=76, y=52, default_letter="ไ", shift_letter="\"", event_key_name="w"),
            Key(self, x=127, y=52, default_letter="ำ", shift_letter="ฎ", event_key_name="e"),
            Key(self, x=177, y=52, default_letter="พ", shift_letter="ฑ", event_key_name="r"),
            Key(self, x=228, y=52, default_letter="ะ", shift_letter="ธ", event_key_name="t"),
            Key(self, x=278, y=52, default_letter="ั", shift_letter="ํ", event_key_name="y"),
            Key(self, x=329, y=52, default_letter="ี", shift_letter="๊", event_key_name="u"),
            Key(self, x=380, y=52, default_letter="ร", shift_letter="ณ", event_key_name="i"),
            Key(self, x=430, y=52, default_letter="น", shift_letter="ฯ", event_key_name="o"),
            Key(self, x=480, y=52, default_letter="ย", shift_letter="ญ", event_key_name="p"),
            Key(self, x=530, y=52, default_letter="บ", shift_letter="ฐ", event_key_name="left_bracket"),
            Key(self, x=581, y=52, default_letter="ล", shift_letter=",", event_key_name="right_bracket"),
            # row 3
            Key(self, x=39, y=103, default_letter="ฟ", shift_letter="ฤ", event_key_name="a"),
            Key(self, x=89, y=103, default_letter="ห", shift_letter="ฆ", event_key_name="s"),
            Key(self, x=140, y=103, default_letter="ก", shift_letter="ฏ", event_key_name="d"),
            Key(self, x=190, y=103, default_letter="ด", shift_letter="โ", event_key_name="f"),
            Key(self, x=241, y=103, default_letter="เ", shift_letter="ฌ", event_key_name="g"),
            Key(self, x=291, y=103, default_letter="้", shift_letter="็", event_key_name="h"),
            Key(self, x=341, y=103, default_letter="่", shift_letter="๋", event_key_name="j"),
            Key(self, x=392, y=103, default_letter="า", shift_letter="ษ", event_key_name="k"),
            Key(self, x=442, y=103, default_letter="ส", shift_letter="ศ", event_key_name="l"),
            Key(self, x=493, y=103, default_letter="ว", shift_letter="ซ", event_key_name="semicolon"),
            Key(self, x=543, y=103, default_letter="ง", shift_letter=".", event_key_name="quote"),
            Key(self, x=594, y=103, default_letter="ฃ", shift_letter="ฅ", event_key_name="backslash"),
            # row 4
            Key(self, x=1, y=153, width=60, default_letter=None, shift_letter=None, event_key_name="right_shift"),
            Key(self, x=64, y=153, default_letter="ผ", shift_letter="(", event_key_name="z"),
            Key(self, x=114, y=153, default_letter="ป", shift_letter=")", event_key_name="x"),
            Key(self, x=165, y=153, default_letter="แ", shift_letter="ฉ", event_key_name="c"),
            Key(self, x=215, y=153, default_letter="อ", shift_letter="ฮ", event_key_name="v"),
            Key(self, x=266, y=153, default_letter="ิ", shift_letter="ฺ", event_key_name="b"),
            Key(self, x=316, y=153, default_letter="ื", shift_letter="์", event_key_name="n"),
            Key(self, x=367, y=153, default_letter="ท", shift_letter="?", event_key_name="m"),
            Key(self, x=417, y=153, default_letter="ม", shift_letter="ฒ", event_key_name="comma"),
            Key(self, x=468, y=153, default_letter="ใ", shift_letter="ฬ", event_key_name="period"),
            Key(self, x=519, y=153, default_letter="ฝ", shift_letter="ฦ", event_key_name="slash"),
            Key(self, x=569, y=153, width=110, default_letter=None, shift_letter=None, event_key_name="left_shift"),
        ]

    def interact(self, test, al):
        if al.ui.click:
            for key in self.keys:
                if key.contains(al.ui.click):
                    if key.event_key_name == "backspace":
                        test.answer = test.answer[:-1]
                    if key.event_key_name == "enter":
                        test.validate_answer()
                    if key.event_key_name == "right_shift":
                        al.ui.right_shift = not al.ui.right_shift
                    if key.event_key_name == "left_shift":
                        al.ui.left_shift = not al.ui.left_shift
                    if al.ui.is_shift():
                        if key.shift_letter:
                            test.answer += key.shift_letter
                    else:
                        if key.default_letter:
                            test.answer += key.default_letter
                    break
            al.ui.click = None
        else:
            for key in self.keys:
                if getattr(al.ui, key.event_key_name):
                    if key.event_key_name == "backspace":
                        test.answer = test.answer[:-1]
                    if key.event_key_name == "enter":
                        test.validate_answer()
                    if al.ui.is_shift():
                        if key.shift_letter:
                            test.answer += key.shift_letter
                    else:
                        if key.default_letter:
                            test.answer += key.default_letter
                    if key.event_key_name not in ["right_shift", "left_shift"]:
                        setattr(al.ui, key.event_key_name, False)


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

