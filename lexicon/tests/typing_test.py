import random
from typing import List

from lexicon.items import Word
from lexicon.tests.tests import ThaiFromEnglish, TestAnswerBox


class Keyboard(object):
    def __init__(self):
        self.row_1 = ["ๅ", "/", "_", "ภ", "ถ", "◌ุ", "◌ึ", "ค", "ต", "จ", "ข", "ช"]

        self.row_2 = ["ๆ", "ไ", "ำ", "พ", "ะ", "◌ั", "◌ี", "ร", "น", "ย", "บ", "ล"]

        self.row_3 = ["ฟ", "ห", "ก", "ด", "เ", "◌้", "◌่", "า", "ส", "ว", "ง", "ฃ"]
        self.row_4 = ["-", "ผ", "ป", "แ", "อ", "◌ิ", "◌ื", "ท", "ม", "ใ", "ฝ"]

        self.shift_row_1 = ["+", "๑", "๒", "๓", "๔", "◌ู", "฿", "๕", "๖", "๗", "๘", "๙"]

        self.shift_row_2 = ["๐", "\"", "ฎ", "ฑ", "ธ", "◌ํ", "◌๊", "ณ", "ฯ", "ญ", "ฐ", ","]
        self.shift_row_3 = ["ฤ", "ฆ", "ฏ", "โ", "ฌ", "◌็", "◌๋", "ษ", "ศ", "ซ", ".", "ฅ"]

        self.shift_row_4 = ["%", "(", ")", "ฉ", "ฮ", "◌ฺ", "◌์", "?", "ฒ", "ฬ", "ฦ"]


class TypingTestFromEnglish(ThaiFromEnglish):
    def __init__(
        self, al: "All", correct: Word, learning=None, test_success_callback=None, test_failure_callback=None,
    ):
        super().__init__(al, correct, learning, test_success_callback, test_failure_callback)
        self.number_of_distr: int = 5

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct] + self.distractors
        random.shuffle(self.choices)

        y = 0.30
        y_space = 0.025
        y_length = 0.175
        self.boxes = [
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(y),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(y_length),
                string=self.choices[0].thai,
                index=0,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(y),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(y_length),
                string=self.choices[1].thai,
                index=1,
            ),
        ]
        y += y_space + y_length
        self.boxes += [
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(y),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(y_length),
                string=self.choices[2].thai,
                index=2,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(y),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(y_length),
                string=self.choices[3].thai,
                index=3,
            ),
        ]
        y += y_space + y_length
        self.boxes += [
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(y),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(y_length),
                string=self.choices[4].thai,
                index=4,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(y),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(y_length),
                string=self.choices[5].thai,
                index=5,
            ),
        ]

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
        screen.blit(fonts.garuda32.render(explanatory_string, True, (0, 0, 0)), (x, y))

        # Draw prompt
        x = ui.percent_width(0.15)
        y = ui.percent_height(0.18)
        screen.blit(
            fonts.garuda32.render(self.correct.english, True, (0, 0, 0)), (x, y)
        )

        # Draw all the options
        for i, box in enumerate(self.boxes):
            box.draw(screen, fonts, selected=self.selected_option_index == i)

    def interact(self, al):
        super().interact(al)
        if al.ui.hover:
            for box in self.boxes:
                if box.contains(al.ui.hover):
                    al.ui.hover = None
                    for other_box in self.boxes:
                        other_box.selected = False
                    box.selected = True
                    self.selected_option_index = box.index
                    break
        if al.ui.click:
            for box in self.boxes:
                if box.contains(al.ui.click):
                    al.ui.click = None
                    self.learner_select_option()
                    break
