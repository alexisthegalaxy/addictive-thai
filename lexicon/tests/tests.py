import random
import pygame
from enum import Enum
from typing import List

from lexicon.items import Word
from models import get_random_word_id
from sounds.play_sound import play_thai_word, play_transformed_thai_word


class Option(object):
    def __init__(self, item, correct, index=0):
        self.index = index
        self.item = item  # can be a Word or a Sentence
        self.correct = correct

    def __str__(self):
        return f"{self.index} - {self.item}"


class TestType(Enum):
    TAPPING = 1
    THAIFROMEN4 = 2
    THAIFROMEN6 = 3
    ENFROMTHAI = 4


def get_correct_option(options: List[Option]):
    for option in options:
        if option.correct:
            return option
    print("ERROR: no correct option in options!")


def draw_box(screen, fonts, x, y, width, height, string, selected=False, font_size=32, bg=(220, 220, 220)):
    # 1 - Draw background
    border_color = (0, 220, 0) if selected else (0, 0, 0)
    pygame.draw.rect(screen, border_color, [x - 5, y - 5, width + 10, height + 10])
    pygame.draw.rect(screen, bg, (x, y, width, height))

    # 2 - Draw the word inside
    if font_size == 24:
        font = fonts.garuda24
    elif font_size == 28:
        font = fonts.garuda28
    else:
        font = fonts.garuda32
    rendered_text = font.render(string, True, (0, 0, 0))
    screen.blit(rendered_text, (x + 10, y + int(height / 2.2) - 20))


class TestAnswerBox(object):
    def __init__(self, x, y, width, height, string, index):
        self.x = x
        self.y = y
        self.selected = False
        self.width = width
        self.height = height
        self.string = string
        self.index = index

    def draw(self, screen, fonts, selected):
        draw_box(
            screen,
            fonts,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            string=self.string,
            selected=selected or self.selected,
        )

    def contains(self, point):
        (x, y) = point
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height


class Test(object):
    def __init__(self, al: "All", learning=None, test_success_callback=None):
        self.al = al
        self.learning = learning
        self.selected_option_index = 0
        self.test_success_callback = test_success_callback

    def draw(self):
        pass

    def interact(self, al):
        pass

    def draw_background(self):
        ui = self.al.ui
        x = ui.percent_width(0.1)
        y = ui.percent_height(0.1)
        height = ui.percent_height(0.8)
        width = ui.percent_width(0.8)

        screen = ui.screen
        pygame.draw.rect(screen, (150, 150, 150), (x, y, width, height))
        pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)

    def succeeds(self):
        # 2 - Play sound
        try:
            play_transformed_thai_word(self.correct_word.thai)
        except pygame.error:
            play_thai_word("right")

        # 3 - End test
        self.al.active_test = None

        # 4 - If part of a learning, pass the baton to the next test
        if self.learning:
            self.learning.test_finished()

        # 5 - test_success_callback
        if self.test_success_callback:
            self.test_success_callback()

    def fails(self):
        # 1 - Hurts the player.
        self.al.learner.hurt(1)

        # 2 - Play sound.
        play_thai_word("wrong")

        # 3 - If part of a learning, pass the baton to the next test
        if self.learning:
            self.learning.test_finished(failed=True)


class ThaiFromEnglish(Test):
    def __init__(
        self, al: "All", correct_word: Word, learning=None, test_success_callback=None
    ):
        super().__init__(al, learning, test_success_callback)
        self.correct_word: Word = correct_word
        self.number_of_distr: int = 3

    def select_distractors(self):
        known_words = Word.get_known_words()
        distractors = []
        if len(known_words) > self.number_of_distr:
            while len(distractors) < self.number_of_distr:
                distractor = random.choices(known_words)[0]
                if (
                    distractor not in distractors
                    and distractor.thai != self.correct_word.thai
                ):
                    distractors.append(distractor)
        else:  # We don't know enough words!
            while len(distractors) < self.number_of_distr:
                # TODO Alexis there is no more al.words
                distractor = get_random_word_id()
                if (
                    distractor not in distractors
                    and distractor.thai != self.correct_word.thai
                ):
                    distractors.append(distractor)
        return distractors

    def interact(self, al):
        if al.ui.up:
            self.selected_option_index -= 2
            if self.selected_option_index < 0:
                self.selected_option_index += self.number_of_distr + 1
            al.ui.up = False
        if al.ui.down:
            self.selected_option_index += 2
            if self.selected_option_index >= (self.number_of_distr + 1):
                self.selected_option_index -= self.number_of_distr + 1
            al.ui.down = False
        if al.ui.left or al.ui.right:
            self.selected_option_index += (
                1 if self.selected_option_index % 2 == 0 else -1
            )
            al.ui.left = False
            al.ui.right = False
        if al.ui.space:
            al.ui.space = False
            self.learner_select_option()

    def learner_select_option(self):
        option = self.selected_option_index
        if self.choices[option] == self.correct_word:
            self.succeeds()
        else:
            self.fails()


class ThaiFromEnglish4(ThaiFromEnglish):
    def __init__(
        self, al: "All", correct_word: Word, learning=None, test_success_callback=None
    ):
        super().__init__(al, correct_word, learning, test_success_callback)
        self.number_of_distr: int = 3

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
        random.shuffle(self.choices)

        self.boxes = [
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(0.35),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[0].thai,
                index=0,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(0.35),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[1].thai,
                index=1,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(0.625),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[2].thai,
                index=2,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(0.625),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[3].thai,
                index=3,
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
            fonts.garuda32.render(self.correct_word.english, True, (0, 0, 0)), (x, y)
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


class ThaiFromEnglish6(ThaiFromEnglish):
    def __init__(
        self, al: "All", correct_word: Word, learning=None, test_success_callback=None
    ):
        super().__init__(al, correct_word, learning, test_success_callback)
        self.number_of_distr: int = 5

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
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
            fonts.garuda32.render(self.correct_word.english, True, (0, 0, 0)), (x, y)
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


class EnglishFromThai4(ThaiFromEnglish):
    def __init__(
        self, al: "All", correct_word: Word, learning=None, test_success_callback=None
    ):
        super().__init__(al, correct_word, learning, test_success_callback)
        self.number_of_distr: int = 3

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
        random.shuffle(self.choices)

        self.boxes = [
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(0.35),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[0].english,
                index=0,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(0.35),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[1].english,
                index=1,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(0.625),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[2].english,
                index=2,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(0.625),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[3].english,
                index=3,
            ),
        ]

    def draw(self):
        ui = self.al.ui

        screen = ui.screen
        fonts = ui.fonts
        # Draw the background
        self.draw_background()

        explanatory_string = "What's the English word for:"
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        screen.blit(fonts.garuda32.render(explanatory_string, True, (0, 0, 0)), (x, y))

        # Draw prompt
        x = ui.percent_width(0.15)
        y = ui.percent_height(0.18)
        screen.blit(
            fonts.garuda32.render(self.correct_word.thai, True, (0, 0, 0)), (x, y)
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


class EnglishFromThai6(ThaiFromEnglish):
    def __init__(
        self, al: "All", correct_word: Word, learning=None, test_success_callback=None
    ):
        super().__init__(al, correct_word, learning, test_success_callback)
        self.number_of_distr: int = 5

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
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
                string=self.choices[0].english,
                index=0,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(y),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(y_length),
                string=self.choices[1].english,
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
                string=self.choices[2].english,
                index=2,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(y),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(y_length),
                string=self.choices[3].english,
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
                string=self.choices[4].english,
                index=4,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(y),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(y_length),
                string=self.choices[5].english,
                index=5,
            ),
        ]

    def draw(self):
        ui = self.al.ui

        screen = ui.screen
        fonts = ui.fonts
        self.draw_background()

        explanatory_string = "What's the English word for:"
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        screen.blit(fonts.garuda32.render(explanatory_string, True, (0, 0, 0)), (x, y))

        # Draw prompt
        x = ui.percent_width(0.15)
        y = ui.percent_height(0.18)
        screen.blit(
            fonts.garuda32.render(self.correct_word.thai, True, (0, 0, 0)), (x, y)
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


class FromSound(Test):
    def __init__(
        self, al: "All", correct_word: Word, learning=None, test_success_callback=None
    ):
        super().__init__(al, learning, test_success_callback)
        self.correct_word: Word = correct_word
        self.number_of_distr: int = 3
        self.selector_on_sound = False
        play_transformed_thai_word(self.correct_word.thai)

    def select_distractors(self):
        known_words = Word.get_known_words()
        distractors = []
        if len(known_words) > self.number_of_distr:
            while len(distractors) < self.number_of_distr:
                distractor = random.choices(known_words)[0]
                if (
                    distractor not in distractors
                    and distractor.thai != self.correct_word.thai
                ):
                    distractors.append(distractor)
        else:  # We don't know enough words!
            while len(distractors) < self.number_of_distr:
                distractor = get_random_word_id()
                if (
                    distractor not in distractors
                    and distractor.thai != self.correct_word.thai
                ):
                    distractors.append(distractor)
        return distractors

    def interact(self, al):
        if al.ui.up:
            al.ui.up = False
            if self.selector_on_sound:
                self.selector_on_sound = False
                self.selected_option_index = self.number_of_distr - 1
            else:
                self.selected_option_index -= 2
                if self.selected_option_index < 0:
                    self.selector_on_sound = True
        if al.ui.down:
            al.ui.down = False
            if self.selector_on_sound:
                self.selector_on_sound = False
                self.selected_option_index = 0
            else:
                self.selected_option_index += 2
                if self.selected_option_index >= (self.number_of_distr + 1):
                    self.selector_on_sound = True
        if al.ui.left or al.ui.right:
            self.selected_option_index += (
                1 if self.selected_option_index % 2 == 0 else -1
            )
            al.ui.left = False
            al.ui.right = False
        if al.ui.space:
            al.ui.space = False
            if self.selector_on_sound:
                play_transformed_thai_word(self.correct_word.thai)
            else:
                self.learner_select_option()

    def learner_select_option(self):
        option = self.selected_option_index
        if self.choices[option] == self.correct_word:
            self.succeeds()
        else:
            self.fails()


class EnglishFromSound(FromSound):
    def __init__(
        self, al: "All", correct_word: Word, learning=None, test_success_callback=None
    ):
        super().__init__(al, learning, correct_word, test_success_callback)


class EnglishFromSound4(EnglishFromSound):
    def __init__(
        self, al: "All", correct_word: Word, learning=None, test_success_callback=None
    ):
        super().__init__(al, learning, correct_word, test_success_callback)
        self.number_of_distr: int = 3

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
        random.shuffle(self.choices)

        self.boxes = [
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(0.35),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[0].english,
                index=0,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(0.35),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[1].english,
                index=1,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(0.625),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[2].english,
                index=2,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(0.625),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[3].english,
                index=3,
            ),
        ]

    def draw(self):
        ui = self.al.ui

        screen = ui.screen
        fonts = ui.fonts
        # Draw the background
        self.draw_background()

        # Draw "What's the English word for"
        explanatory_string = "What's the English word for:"
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        screen.blit(fonts.garuda32.render(explanatory_string, True, (0, 0, 0)), (x, y))

        # Draw prompt
        x = ui.percent_width(0.60)
        y = ui.percent_height(0.10)
        image_name = "sound_icon_green" if self.selector_on_sound else "sound_icon"
        ui.screen.blit(ui.images[image_name], [x, y])

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


class EnglishFromSound6(EnglishFromSound):
    def __init__(
        self, al: "All", correct_word: Word, learning=None, test_success_callback=None
    ):
        super().__init__(al, learning, correct_word, test_success_callback)
        self.number_of_distr: int = 5

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
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
                string=self.choices[0].english,
                index=0,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(y),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(y_length),
                string=self.choices[1].english,
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
                string=self.choices[2].english,
                index=2,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(y),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(y_length),
                string=self.choices[3].english,
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
                string=self.choices[4].english,
                index=4,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(y),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(y_length),
                string=self.choices[5].english,
                index=5,
            ),
        ]

    def draw(self):
        ui = self.al.ui

        screen = ui.screen
        fonts = ui.fonts
        # Draw the background
        self.draw_background()

        # Draw "What's the English word for"
        explanatory_string = "What's the English word for:"
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        screen.blit(fonts.garuda32.render(explanatory_string, True, (0, 0, 0)), (x, y))

        # Draw prompt
        x = ui.percent_width(0.60)
        y = ui.percent_height(0.10)
        image_name = "sound_icon_green" if self.selector_on_sound else "sound_icon"
        ui.screen.blit(ui.images[image_name], [x, y])

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


class ThaiFromSound4(EnglishFromSound):
    def __init__(
        self,
        al: "All",
        correct_word: Word,
        learning: "Learning" = None,
        test_success_callback=None,
    ):
        super().__init__(al, learning, correct_word, test_success_callback)
        self.number_of_distr: int = 3

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
        random.shuffle(self.choices)

        self.boxes = [
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(0.35),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[0].thai,
                index=0,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(0.35),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[1].thai,
                index=1,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(0.625),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[2].thai,
                index=2,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.53),
                y=al.ui.percent_height(0.625),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.225),
                string=self.choices[3].thai,
                index=3,
            ),
        ]

    def draw(self):
        ui = self.al.ui

        screen = ui.screen
        fonts = ui.fonts
        # Draw the background
        self.draw_background()

        # Draw "What's the English word for"
        explanatory_string = "What's the English word for:"
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        screen.blit(fonts.garuda32.render(explanatory_string, True, (0, 0, 0)), (x, y))

        # Draw prompt
        x = ui.percent_width(0.60)
        y = ui.percent_height(0.10)
        image_name = "sound_icon_green" if self.selector_on_sound else "sound_icon"
        ui.screen.blit(ui.images[image_name], [x, y])

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


class ThaiFromSound6(EnglishFromSound):
    def __init__(
        self,
        al: "All",
        correct_word: Word,
        learning: "Learning" = None,
        test_success_callback=None,
    ):
        super().__init__(al, learning, correct_word, test_success_callback)
        self.number_of_distr: int = 5

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
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

        # Draw "What's the English word for"
        explanatory_string = "What's the English word for:"
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        screen.blit(fonts.garuda32.render(explanatory_string, True, (0, 0, 0)), (x, y))

        # Draw prompt
        x = ui.percent_width(0.60)
        y = ui.percent_height(0.10)
        image_name = "sound_icon_green" if self.selector_on_sound else "sound_icon"
        ui.screen.blit(ui.images[image_name], [x, y])

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
