import random
import pygame
from enum import Enum
from typing import List

from lexicon.items import Word
from sounds.play_sound import play_thai_word, play_transformed_thai_word

from sounds.thai.sound_processing import transform_english_into_track_name


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


class Test(object):
    def __init__(self, al: 'All', learning=None):
        self.al = al
        self.learning = learning
        self.selected_option_index = 0

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

    def fails(self):
        # 1 - Hurts the player.
        self.al.learner.hurt(1)

        # 2 - Play sound.
        play_thai_word("wrong")

        # 3 - If part of a learning, pass the baton to the next test
        if self.learning:
            self.learning.test_finished(failed=True)


class TappingTestSentence(Test):
    def __init__(self, al: 'All', correct_word: Word, sentence, learning=None):
        super().__init__(al, learning)
        self.correct_word = correct_word
        self.number_of_distr = 6
        self.constructed_sentence = []  # List of syllables
        self.is_validating = False
        self.sentence = sentence

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
        x = ui.percent_width(0.15)
        y = ui.percent_height(0.30)
        height = ui.percent_height(0.1)
        for i, syllable in enumerate(self.choices):
            rendered_text = fonts.garuda32.render(syllable.thai, True, (0, 0, 0))
            text_length = rendered_text.get_width()
            width = text_length + 20
            draw_box(
                self.al.ui.screen,
                self.al.ui.fonts,
                x=x,
                y=y,
                width=width,
                height=height,
                string=syllable.thai,
                selected=self.selected_option_index == i and not self.is_validating,
            )

            x += width + 20
            if x > ui.percent_width(0.85):
                x = ui.percent_width(0.15)
                y += ui.percent_height(0.30)

        # Draw the constructed sentence
        x = ui.percent_width(0.15)
        y = ui.percent_height(0.60)
        for i, syllable in enumerate(self.constructed_sentence):
            rendered_text = fonts.garuda32.render(syllable.thai, True, (0, 0, 0))
            text_length = rendered_text.get_width()
            width = text_length + 20
            # if x + width + 40 > ui.percent_width(0.85):
            #     x = ui.percent_width(0.15)
            #     y += ui.percent_height(0.15)

            draw_box(
                self.al.ui.screen,
                self.al.ui.fonts,
                x=x,
                y=y,
                width=width,
                height=height,
                string=syllable.thai,
            )

            x += width + 20
            if x > ui.percent_width(0.85):
                x = ui.percent_width(0.15)
                y += ui.percent_height(0.15)

        # Draw Validate Answer box
        rendered_text = fonts.garuda32.render("Validate", True, (0, 0, 0))
        text_length = rendered_text.get_width()
        width = text_length + 20

        if x + width > ui.percent_width(0.85):
            x = ui.percent_width(0.15)
            y += ui.percent_height(0.15)

        draw_box(
            self.al.ui.screen,
            self.al.ui.fonts,
            x=x,
            y=y,
            width=width,
            height=height,
            string="Validate",
            selected=self.is_validating,
        )

    def interact(self, al):
        if al.ui.left:
            al.ui.left = False
            self.selected_option_index -= 1
            if self.selected_option_index < 0:
                self.selected_option_index = len(self.choices) - 1
        if al.ui.right:
            al.ui.right = False
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
                self.validate_answer()
            else:
                self.learner_select_option()
        if al.ui.backspace:
            al.ui.backspace = False
            self.remove_last_word()

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

    def learner_select_option(self):
        self.constructed_sentence.append(self.choices[self.selected_option_index])
        # option = self.selected_option_index
        # if self.choices[option] == self.correct_word:
        #     self.succeeds([self.correct_word])
        # else:
        #     self.fails()

    def remove_last_word(self):
        if len(self.constructed_sentence) > 0:
            self.constructed_sentence.pop()


def draw_box(screen, fonts, x, y, width, height, string, selected=False):
    # 1 - Draw background
    screen_color = (0, 220, 0) if selected else (0, 0, 0)
    pygame.draw.rect(screen, screen_color, [x - 5, y - 5, width + 10, height + 10])
    pygame.draw.rect(screen, (220, 220, 220), (x, y, width, height))

    # 2 - Draw the word inside
    rendered_text = fonts.garuda32.render(string, True, (0, 0, 0))
    screen.blit(rendered_text, (x + 10, y + int(height / 2.2) - 20))


class ThaiFromEnglish(Test):
    def __init__(self, al: 'All', correct_word: Word, learning=None):
        super().__init__(al, learning)
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
                self.selected_option_index += (self.number_of_distr + 1)
            al.ui.up = False
        if al.ui.down:
            self.selected_option_index += 2
            if self.selected_option_index >= (self.number_of_distr + 1):
                self.selected_option_index -= (self.number_of_distr + 1)
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
    def __init__(self, al: 'All', correct_word: Word, learning=None):
        super().__init__(al, correct_word, learning)
        self.number_of_distr: int = 3

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
        random.shuffle(self.choices)

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
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(0.35),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[0].thai,
            selected=self.selected_option_index == 0,
        )

        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(0.35),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[1].thai,
            selected=self.selected_option_index == 1,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(0.625),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[2].thai,
            selected=self.selected_option_index == 2,
        )

        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(0.625),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[3].thai,
            selected=self.selected_option_index == 3,
        )


class ThaiFromEnglish6(ThaiFromEnglish):
    def __init__(self, al: 'All', correct_word: Word, learning=None):
        super().__init__(al, correct_word, learning)
        self.number_of_distr: int = 5

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
        random.shuffle(self.choices)

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
        y = 0.30
        y_space = 0.025
        y_length = 0.175
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[0].thai,
            selected=self.selected_option_index == 0,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[1].thai,
            selected=self.selected_option_index == 1,
        )
        y += y_space + y_length
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[2].thai,
            selected=self.selected_option_index == 2,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[3].thai,
            selected=self.selected_option_index == 3,
        )
        y += y_space + y_length
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[4].thai,
            selected=self.selected_option_index == 4,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[5].thai,
            selected=self.selected_option_index == 5,
        )


class EnglishFromThai4(ThaiFromEnglish):
    def __init__(self, al: 'All', correct_word: Word, learning=None):
        super().__init__(al, correct_word, learning)
        self.number_of_distr: int = 3

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
        random.shuffle(self.choices)

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
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(0.35),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[0].english,
            selected=self.selected_option_index == 0,
        )

        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(0.35),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[1].english,
            selected=self.selected_option_index == 1,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(0.625),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[2].english,
            selected=self.selected_option_index == 2,
        )

        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(0.625),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[3].english,
            selected=self.selected_option_index == 3,
        )


class EnglishFromThai6(ThaiFromEnglish):
    def __init__(self, al: 'All', correct_word: Word, learning=None):
        super().__init__(al, correct_word, learning)
        self.number_of_distr: int = 5

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
        random.shuffle(self.choices)

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
        y = 0.30
        y_space = 0.025
        y_length = 0.175
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[0].english,
            selected=self.selected_option_index == 0,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[1].english,
            selected=self.selected_option_index == 1,
        )
        y += y_space + y_length
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[2].english,
            selected=self.selected_option_index == 2,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[3].english,
            selected=self.selected_option_index == 3,
        )
        y += y_space + y_length
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[4].english,
            selected=self.selected_option_index == 4,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[5].english,
            selected=self.selected_option_index == 5,
        )


def get_correct_option(options: List[Option]):
    for option in options:
        if option.correct:
            return option
    print("ERROR: no correct option in options!")


class FromSound(Test):
    def __init__(self, al: 'All', correct_word: Word, learning=None):
        super().__init__(al, learning)
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
    def __init__(self, al: 'All', correct_word: Word, learning=None):
        super().__init__(al, learning, correct_word)


class EnglishFromSound4(EnglishFromSound):
    def __init__(self, al: 'All', correct_word: Word, learning=None):
        super().__init__(al, learning, correct_word)
        self.number_of_distr: int = 3

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
        random.shuffle(self.choices)

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
        image_name = 'sound_icon_green' if self.selector_on_sound else 'sound_icon'
        ui.screen.blit(ui.images[image_name], [x, y])

        # Draw all the options
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(0.35),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[0].english,
            selected=self.selected_option_index == 0,
        )

        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(0.35),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[1].english,
            selected=self.selected_option_index == 1,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(0.625),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[2].english,
            selected=self.selected_option_index == 2,
        )

        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(0.625),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[3].english,
            selected=self.selected_option_index == 3,
        )


class EnglishFromSound6(EnglishFromSound):
    def __init__(self, al: 'All', correct_word: Word, learning=None):
        super().__init__(al, learning, correct_word)
        self.number_of_distr: int = 5

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
        random.shuffle(self.choices)

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
        image_name = 'sound_icon_green' if self.selector_on_sound else 'sound_icon'
        ui.screen.blit(ui.images[image_name], [x, y])

        # Draw all the options
        y = 0.30
        y_space = 0.025
        y_length = 0.175
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[0].english,
            selected=self.selected_option_index == 0,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[1].english,
            selected=self.selected_option_index == 1,
        )
        y += y_space + y_length
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[2].english,
            selected=self.selected_option_index == 2,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[3].english,
            selected=self.selected_option_index == 3,
        )
        y += y_space + y_length
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[4].english,
            selected=self.selected_option_index == 4,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[5].english,
            selected=self.selected_option_index == 5,
        )


class ThaiFromSound4(EnglishFromSound):
    def __init__(self, al: 'All', correct_word: Word, learning: 'Learning' = None):
        super().__init__(al, learning, correct_word)
        self.number_of_distr: int = 3

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
        random.shuffle(self.choices)

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
        image_name = 'sound_icon_green' if self.selector_on_sound else 'sound_icon'
        ui.screen.blit(ui.images[image_name], [x, y])

        # Draw all the options
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(0.35),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[0].thai,
            selected=self.selected_option_index == 0,
        )

        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(0.35),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[1].thai,
            selected=self.selected_option_index == 1,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(0.625),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[2].thai,
            selected=self.selected_option_index == 2,
        )

        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(0.625),
            width=ui.percent_width(0.32),
            height=ui.percent_height(0.225),
            string=self.choices[3].thai,
            selected=self.selected_option_index == 3,
        )


class ThaiFromSound6(EnglishFromSound):
    def __init__(self, al: 'All', correct_word: Word, learning: 'Learning' = None):
        super().__init__(al, learning, correct_word)
        self.number_of_distr: int = 5

        self.distractors: List[Word] = self.select_distractors()
        self.choices: List[Word] = [self.correct_word] + self.distractors
        random.shuffle(self.choices)

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
        image_name = 'sound_icon_green' if self.selector_on_sound else 'sound_icon'
        ui.screen.blit(ui.images[image_name], [x, y])

        # Draw all the options
        y = 0.30
        y_space = 0.025
        y_length = 0.175
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[0].thai,
            selected=self.selected_option_index == 0,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[1].thai,
            selected=self.selected_option_index == 1,
        )
        y += y_space + y_length
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[2].thai,
            selected=self.selected_option_index == 2,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[3].thai,
            selected=self.selected_option_index == 3,
        )
        y += y_space + y_length
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.15),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[4].thai,
            selected=self.selected_option_index == 4,
        )
        draw_box(
            screen,
            fonts,
            x=ui.percent_width(0.53),
            y=ui.percent_height(y),
            width=ui.percent_width(0.32),
            height=ui.percent_height(y_length),
            string=self.choices[5].thai,
            selected=self.selected_option_index == 5,
        )

