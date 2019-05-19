from lexicon.items import Word
from lexicon.tests.tests import Test, TestAnswerBox
import random
import pygame


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

