from lexicon.items import Word
from lexicon.tests.tests import Test, draw_box
import random
import pygame
from time import mktime
from datetime import datetime

from models import get_random_known_word_id, find_word_by_id_get_thai


class Cell(object):
    def __init__(self):
        self.thai = ""
        self.word_id = None
        self.links_to = None
        self.selected = False


class Timer(object):
    """
    Has a bar that gets filled slowly, starting at 0, going up to 20 or something
    """
    def __init__(self, al, seconds=20):
        self.start = mktime(datetime.now().timetuple())

    def draw(self):
        pass


class Grid(object):
    def __init__(self, al, sentence):
        self.cells = [
            [Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell()],
        ]
        self.al = al
        self.sentence = sentence
        print(self.sentence)
        self.fill_with_random_words()
        self.embed_sentence()

    def set_cell(self, x, y, thai, word_id):
        assert 0 <= x <= 3
        assert 0 <= y <= 3
        self.cells[x][y].thai = thai
        self.cells[x][y].word_id = word_id

    def get_cell(self, x, y):
        assert 0 <= x <= 3
        assert 0 <= y <= 3
        return self.cells[x][y]

    def embed_sentence(self):
        succeeded = self.try_to_embed_sentence()
        if not succeeded:
            self.embed_sentence()

    def try_to_embed_sentence(self) -> bool:
        words = self.sentence.words
        positions = []
        previous_position = None
        for _ in words:
            if not positions:
                x = random.choice([0, 1, 2, 3])
                y = random.choice([0, 1, 2, 3])
                position = (x, y)
                previous_position = position
                positions.append(position)
            else:
                position_is_correct = False
                i, x, y = 0, 0, 0
                while not position_is_correct:
                    x = previous_position[0] + random.choice([-1, 0, 1])
                    y = previous_position[1] + random.choice([-1, 0, 1])
                    position_is_correct = 0 <= x <= 3 and 0 <= y <= 3 and (x, y) not in positions
                    i += 1
                    if i > 100:  # Then, there is no possibility
                        return False
                position = (x, y)
                previous_position = position
                positions.append(position)
        assert len(positions) == len(words)
        for i, position in enumerate(positions):
            x, y = position
            thai = words[i].thai
            word_id = -1
            self.set_cell(x, y, thai=thai, word_id=word_id)
        return True


    def fill_with_random_words(self):
        for line in self.cells:
            for cell in line:
                if not cell.thai:
                    random_word_id = get_random_known_word_id()
                    cell.word_id = random_word_id
                    cell.thai = find_word_by_id_get_thai(random_word_id)

    def draw(self):
        ui = self.al.ui
        width = 130
        height = 130
        shift_x = (ui.percent_width(1) - 580) / 2
        shift_y = (ui.percent_height(1) - 580) / 2

        for i, line in enumerate(self.cells):
            for j, cell in enumerate(line):
                x = shift_x + i * 150
                y = shift_y + j * 150
                string = cell.thai
                draw_box(ui.screen, ui.fonts, x, y, width, height, string)


class GridTest(Test):
    """
    Concept:
    For a given word, choose a sentence that contains,
    (it should always be possible by construction of the game)
    And put it in a 4*4 grid
    The goal is then to find the longest sentence in a limited time
    Each sentence that you find gives you points, according to its size
    Finding the bonus sentence (which is translated on the side) gives a *3 bonus
    """

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
        self.grid = Grid(al=al, sentence=sentence)
        self.timer = Timer(al=al)
        self.number_of_distr = 6
        self.selected_picked_syllable_index = 0
        self.constructed_sentence = []  # List of syllables
        self.is_validating = (
            False
        )  # means that the selector is in the lower part of the screen
        self.sentence = sentence
        self.option_boxes = []
        self.sentence_boxes = []
        self.validate_box = None
        self.failed_attempts = 0
        self.failed_attempts_limit = 3  # After three failed attempts, show the answer

    def draw(self):
        ui = self.al.ui
        x = ui.percent_width(0.07)
        y = ui.percent_height(0.07)
        height = ui.percent_height(0.86)
        width = ui.percent_width(0.86)

        screen = ui.screen
        fonts = ui.fonts
        # Draw the background
        pygame.draw.rect(screen, (150, 150, 150), (x, y, width, height))
        pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)

        # # Draw "Write the following sentence in Thai"
        # explanatory_string = "Write the following sentence in Thai:"
        # x = ui.percent_width(0.12)
        # y = ui.percent_height(0.12)
        # screen.blit(fonts.garuda32.render(explanatory_string, True, (0, 0, 0)), (x, y))

        # # Draw prompt
        # x = ui.percent_width(0.15)
        # y = ui.percent_height(0.18)
        # screen.blit(
        #     fonts.garuda32.render(self.sentence.english, True, (0, 0, 0)), (x, y)
        # )

        # Draw grid
        self.grid.draw()

        # Draw timer
        self.timer.draw()

    def interact(self, al):
        pass
        # if al.ui.left:
        #     al.ui.left = False
        #     if self.is_validating:
        #         self.selected_picked_syllable_index -= 1
        #         if self.selected_picked_syllable_index < 0:
        #             self.selected_picked_syllable_index = len(self.sentence_boxes)
        #     else:
        #         self.selected_option_index -= 1
        #         if self.selected_option_index < 0:
        #             self.selected_option_index = len(self.choices) - 1
        # if al.ui.right:
        #     al.ui.right = False
        #     if self.is_validating:
        #         self.selected_picked_syllable_index += 1
        #         if self.selected_picked_syllable_index > len(self.sentence_boxes):
        #             self.selected_picked_syllable_index = 0
        #     else:
        #         self.selected_option_index += 1
        #         if self.selected_option_index > len(self.choices) - 1:
        #             self.selected_option_index = 0
        # if al.ui.down:
        #     al.ui.down = False
        #     self.is_validating = True
        # if al.ui.up:
        #     al.ui.up = False
        #     self.is_validating = False
        # if al.ui.space:
        #     al.ui.space = False
        #     if self.is_validating:
        #         if self.selected_picked_syllable_index == len(
        #             self.constructed_sentence
        #         ):
        #             self.validate_answer()
        #         else:
        #             self.learner_remove_picked_syllable(
        #                 self.selected_picked_syllable_index
        #             )
        #     else:
        #         self.learner_select_option()
        # if al.ui.backspace:
        #     al.ui.backspace = False
        #     self.remove_last_word()
        #
        # if al.ui.hover:
        #     self.process_hover()
        # if al.ui.click:
        #     self.process_click()

    def set_box_as_selected_and_unselect_others(self, box):
        for other_box in self.option_boxes + self.sentence_boxes + [self.validate_box]:
            other_box.selected = False
        box.selected = True

    def process_hover(self):
        pass
        # for box in self.option_boxes:
        #     if box.contains(self.al.ui.hover):
        #         self.al.ui.hover = None
        #         self.is_validating = False
        #         self.set_box_as_selected_and_unselect_others(box)
        #         self.selected_option_index = box.index
        #         return
        # for box in self.sentence_boxes:
        #     if box.contains(self.al.ui.hover):
        #         self.al.ui.hover = None
        #         self.is_validating = True
        #         self.selected_picked_syllable_index = box.index
        #         self.set_box_as_selected_and_unselect_others(box)
        #         return
        # if self.validate_box.contains(self.al.ui.hover):
        #     self.al.ui.hover = None
        #     self.set_box_as_selected_and_unselect_others(self.validate_box)
        #     self.selected_picked_syllable_index = self.validate_box.index
        #     self.is_validating = True

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
        self.constructed_sentence.remove(
            self.constructed_sentence[picked_syllable_index]
        )
        self.set_boxes()

    def learner_select_option(self):
        self.constructed_sentence.append(self.choices[self.selected_option_index])
        self.set_boxes()

    def remove_last_word(self):
        if len(self.constructed_sentence) > 0:
            self.constructed_sentence.pop()
