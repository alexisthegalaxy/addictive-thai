import random
import pygame
from enum import Enum
from typing import List

from lexicon.items import Word
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


def draw_box(screen, fonts, x, y, width, height, string, selected=False):
    # 1 - Draw background
    screen_color = (0, 220, 0) if selected else (0, 0, 0)
    pygame.draw.rect(screen, screen_color, [x - 5, y - 5, width + 10, height + 10])
    pygame.draw.rect(screen, (220, 220, 220), (x, y, width, height))

    # 2 - Draw the word inside
    rendered_text = fonts.garuda32.render(string, True, (0, 0, 0))
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

    def succeeds(self, words_to_level_up):
        # 1 - Puts in the xp
        for word in words_to_level_up:
            word.increase_xp(self.al, 1)

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


class TappingTestSentence(Test):
    def __init__(
        self,
        al: "All",
        correct_word: Word,
        sentence,
        learning=None,
        test_success_callback=None,
    ):
        super().__init__(al, learning, test_success_callback)
        self.correct_word = correct_word
        self.number_of_distr = 6
        self.selected_picked_syllable_index = 0
        self.constructed_sentence = []  # List of syllables
        self.is_validating = False  # means that the selector is in the lower part of the screen
        self.sentence = sentence
        self.option_boxes = []
        self.sentence_boxes = []
        self.validate_box = None
        self.failed_attempts = 0
        self.failed_attempts_limit = 3  # After three failed attempts, show the answer

        # 1 - Determine the correct options
        self.correct_syllables = []
        syllable_only = []
        for word in self.sentence.words:
            for syllable in word.syllables:
                self.correct_syllables.append(syllable)
                syllable_only.append(syllable.thai)

        # 3 - Determine the distractors
        self.distractors = []
        self.select_distractors(syllable_only)

        # 4 - Mix distractors and correct options
        self.choices = self.correct_syllables + self.distractors
        random.shuffle(self.choices)

        # 5 - Set boxes position - both options and already built sentence
        self.set_boxes()

    def set_boxes(self):
        # Reset boxes
        self.sentence_boxes = []
        self.option_boxes = []
        self.validate_box = None

        # options
        ui = self.al.ui
        fonts = ui.fonts
        x = ui.percent_width(0.15)
        y = ui.percent_height(0.30)
        height = ui.percent_height(0.1)
        for i, syllable in enumerate(self.choices):
            rendered_text = fonts.garuda32.render(syllable.thai, True, (0, 0, 0))
            text_length = rendered_text.get_width()
            width = text_length + 20
            self.option_boxes.append(
                TestAnswerBox(
                    x=x, y=y, width=width, height=height, string=syllable.thai, index=i
                )
            )
            x += width + 20
            if x > ui.percent_width(0.85):
                x = ui.percent_width(0.15)
                y += ui.percent_height(0.30)

        # built sentence
        x = ui.percent_width(0.15)
        y = ui.percent_height(0.60)
        validated_box_index = 0
        for i, syllable in enumerate(self.constructed_sentence):
            rendered_text = fonts.garuda32.render(syllable.thai, True, (0, 0, 0))
            text_length = rendered_text.get_width()
            width = text_length + 20
            self.sentence_boxes.append(
                TestAnswerBox(
                    x=x, y=y, width=width, height=height, string=syllable.thai, index=i
                )
            )
            x += width + 20
            if x > ui.percent_width(0.85):
                x = ui.percent_width(0.15)
                y += ui.percent_height(0.15)
            validated_box_index += 1

        rendered_text = fonts.garuda32.render("Validate", True, (0, 0, 0))
        text_length = rendered_text.get_width()
        width = text_length + 20

        if x + width > ui.percent_width(0.85):
            x = ui.percent_width(0.15)
            y += ui.percent_height(0.15)
        self.validate_box = TestAnswerBox(
            x=x,
            y=y,
            width=width,
            height=height,
            string="Validate",
            index=validated_box_index,
        )

    def select_distractors(self, syllable_only):
        # We select amongst sentences.words rather than amongst words to get
        # more common words
        for sentence in random.choices(population=self.al.sentences.sentences):
            for word in random.choices(population=sentence.words):
                for syllable in word.syllables:
                    if syllable.thai not in syllable_only:
                        self.distractors.append(syllable)
                        syllable_only.append(syllable.thai)
                    if len(self.distractors) > self.number_of_distr:
                        return

    def draw(self):
        ui = self.al.ui
        x = ui.percent_width(0.1)
        y = ui.percent_height(0.1)
        height = ui.percent_height(0.8)
        width = ui.percent_width(0.8)

        screen = ui.screen
        fonts = ui.fonts
        # Draw the background
        pygame.draw.rect(screen, (150, 150, 150), (x, y, width, height))
        pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)

        # Draw "Write the following sentence in Thai"
        explanatory_string = "Write the following sentence in Thai:"
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        screen.blit(fonts.garuda32.render(explanatory_string, True, (0, 0, 0)), (x, y))

        # Draw prompt
        x = ui.percent_width(0.15)
        y = ui.percent_height(0.18)
        screen.blit(
            fonts.garuda32.render(self.sentence.english, True, (0, 0, 0)), (x, y)
        )

        # Draw all the options
        for i, option_box in enumerate(self.option_boxes):
            option_box.draw(
                screen,
                fonts,
                # selected=self.selected_option_index == i and not self.is_validating,
                selected=self.selected_option_index == i and not self.is_validating,
            )

        # Draw the constructed sentence
        for i, sentence_box in enumerate(self.sentence_boxes):
            sentence_box.draw(
                screen,
                fonts,
                # selected=self.selected_option_index == i and not self.is_validating,
                selected=self.is_validating and self.selected_picked_syllable_index == i,
            )

        # Draw Validate Answer box
        self.validate_box.draw(
            screen,
            fonts,
            selected=self.is_validating
            and self.selected_picked_syllable_index == self.validate_box.index,
        )

        if self.failed_attempts >= self.failed_attempts_limit:
            x = ui.percent_width(0.15)
            y = ui.percent_height(0.78)
            screen.blit(
                fonts.garuda32.render("Correct answer: " + self.sentence.thai, True, (0, 0, 0)), (x, y)
            )

    def interact(self, al):
        if al.ui.left:
            al.ui.left = False
            if self.is_validating:
                self.selected_picked_syllable_index -= 1
                if self.selected_picked_syllable_index < 0:
                    self.selected_picked_syllable_index = len(self.sentence_boxes)
            else:
                self.selected_option_index -= 1
                if self.selected_option_index < 0:
                    self.selected_option_index = len(self.choices) - 1
        if al.ui.right:
            al.ui.right = False
            if self.is_validating:
                self.selected_picked_syllable_index += 1
                if self.selected_picked_syllable_index > len(self.sentence_boxes):
                    self.selected_picked_syllable_index = 0
            else:
                self.selected_option_index += 1
                if self.selected_option_index > len(self.choices) - 1:
                    self.selected_option_index = 0
        if al.ui.down:
            al.ui.down = False
            self.is_validating = True
        if al.ui.up:
            al.ui.up = False
            self.is_validating = False
        if al.ui.space:
            al.ui.space = False
            if self.is_validating:
                if self.selected_picked_syllable_index == len(self.constructed_sentence):
                    self.validate_answer()
                else:
                    self.learner_remove_picked_syllable(self.selected_picked_syllable_index)
            else:
                self.learner_select_option()
        if al.ui.backspace:
            al.ui.backspace = False
            self.remove_last_word()

        if al.ui.hover:
            self.process_hover()
        if al.ui.click:
            self.process_click()

    def set_box_as_selected_and_unselect_others(self, box):
        for other_box in (
            self.option_boxes + self.sentence_boxes + [self.validate_box]
        ):
            other_box.selected = False
        box.selected = True

    def process_hover(self):
        for box in self.option_boxes:
            if box.contains(self.al.ui.hover):
                self.al.ui.hover = None
                self.is_validating = False
                self.set_box_as_selected_and_unselect_others(box)
                self.selected_option_index = box.index
                return
        for box in self.sentence_boxes:
            if box.contains(self.al.ui.hover):
                self.al.ui.hover = None
                self.is_validating = True
                self.selected_picked_syllable_index = box.index
                self.set_box_as_selected_and_unselect_others(box)
                return
        if self.validate_box.contains(self.al.ui.hover):
            self.al.ui.hover = None
            self.set_box_as_selected_and_unselect_others(self.validate_box)
            self.selected_picked_syllable_index = self.validate_box.index
            self.is_validating = True

    def process_click(self):
        for box in self.option_boxes:
            if box.contains(self.al.ui.click):
                self.al.ui.click = None
                self.selected_option_index = box.index
                self.learner_select_option()
                return
        for box in self.sentence_boxes:
            if box.contains(self.al.ui.click):
                self.al.ui.click = None
                self.learner_remove_picked_syllable(box.index)
                return
        if self.validate_box.contains(self.al.ui.click):
            self.al.ui.click = None
            self.validate_answer()

    def validate_answer(self):
        constructed = "".join([word.thai for word in self.constructed_sentence])
        if constructed == self.sentence.thai:
            words_to_level_up = []
            for syllable in self.constructed_sentence:
                for word in self.al.words.words:
                    if syllable.thai == word.thai:
                        words_to_level_up.append(word)
            self.succeeds(words_to_level_up)
        else:
            self.fails()
            self.failed_attempts += 1

    def learner_remove_picked_syllable(self, picked_syllable_index: int):
        self.constructed_sentence.remove(self.constructed_sentence[picked_syllable_index])
        self.set_boxes()

    def learner_select_option(self):
        self.constructed_sentence.append(self.choices[self.selected_option_index])
        self.set_boxes()

    def remove_last_word(self):
        if len(self.constructed_sentence) > 0:
            self.constructed_sentence.pop()


class ThaiFromEnglish(Test):
    def __init__(
        self, al: "All", correct_word: Word, learning=None, test_success_callback=None
    ):
        super().__init__(al, learning, test_success_callback)
        self.correct_word: Word = correct_word
        self.number_of_distr: int = 3

    def select_distractors(self):
        known_words = self.al.words.get_known_words()
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
                distractor = random.choices(self.al.words.words)[0]
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
            self.succeeds([self.correct_word])
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
        known_words = self.al.words.get_known_words()
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
                distractor = random.choices(self.al.words.words)[0]
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
            self.succeeds([self.correct_word])
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
