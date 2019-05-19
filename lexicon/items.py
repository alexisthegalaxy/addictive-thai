# import pygame
from typing import List

from pygame import gfxdraw
from lexicon.tone import Tone, Length


class Syllable(object):
    def __init__(
        self,
        thai="no_thai",
        english="no_english",
        tone=Tone.UNKNOWN,
        length=Length.UNKNOWN,
        audio="",
    ):
        self.thai = thai
        self.english = english
        self.tone = tone
        self.long = length
        self.audio = audio

    def print(self, extra):
        print(f"{extra}thai:    {self.thai}")
        print(f"{extra}english: {self.english}")
        print(f"{extra}tone:    {self.tone}")


class Growable(object):
    """
        Words, and any learnable item that can be learnt over time
        Growable have xp and a level
    """

    def __init__(self):
        self.thai = ""
        self.total_xp = 0
        self.level = 1
        self.next_threshold = 1
        self.previous_threshold = 0

    def increase_xp(self, al, value):
        self.total_xp += value
        while self.total_xp >= self.next_threshold:
            self.level_up()
        if al.dex:
            al.dex.determine_words_to_show()

    def decrease_xp(self, al, value):
        # print('')
        # print('before the decreasing:')
        # print('total_xp = ', self.total_xp)

        final_xp = max(self.total_xp - value, 0)

        # reset
        self.total_xp = 0
        self.level = 1
        self.next_threshold = 1
        self.previous_threshold = 0

        self.increase_xp(al, final_xp)

        # print('after the decreasing')
        # print('total_xp = ', self.total_xp)
        # print('')

    def level_up(self):
        self.level += 1
        self.previous_threshold += self.level - 1
        self.next_threshold += self.level
        # print(f'{self.thai}levelled up to level {self.level}!')

    def reset(self, al, xp=0):
        if xp == 0:
            self.total_xp = 0
            self.level = 1
            self.next_threshold = 1
            self.previous_threshold = 0
            al.dex.determine_words_to_show()
        else:
            self.increase_xp(al, xp)

    def show_xp(self):
        print()
        print(f"level: {self.level}")
        print(f"total xp: {self.total_xp}")
        current_xp = self.total_xp - self.previous_threshold
        total_xp_in_level = self.next_threshold - self.previous_threshold
        print(f"current_xp: {current_xp}/{total_xp_in_level}")


class Syllables(object):
    def __init__(self):
        self.syllables = []

    def get_syllable(self, thai: str):
        for syllable in self.syllables:
            if syllable.thai == thai:
                return syllable

    def add_syllable(self, syllable: Syllable):
        self.syllables.append(syllable)

    def print(self):
        print("╔═════════════════════════════════════════════")
        for syllable in self.syllables:
            syllable.print("║")
            print("╠═════════════════════════════════════════════")
        print("╚═════════════════════════════════════════════")


class Word(Growable):
    """
    A word is made of one or more syllables.
    Example:
        thai = ใจดี
        english = kind
        syllables = [Syllable("ใจ"), Syllable("ดี")]
    """

    def __init__(
        self, syllables: Syllables, thai="no_thai", english="no_english", location=None
    ):
        super().__init__()
        self.thai = thai.replace("-", "")
        self.separated_form = thai
        self.english = english
        self.syllables = []  # list of syllables contained in that word
        self.sentences = []  # list of sentences containing that word
        self.map = None
        if location:
            self.map = location[0]
            self.x = location[1]
            self.y = location[2]

        syllables_in_word = thai.split("-")

        for syllable_in_word in syllables_in_word:
            syllable = syllables.get_syllable(syllable_in_word)
            if not syllable:
                from lexicon.items_creation import add_syllable

                add_syllable(
                    syllables, thai=syllable_in_word, english="", tone=Tone.UNKNOWN
                )
                syllable = syllables.get_syllable(syllable_in_word)
            self.syllables.append(syllable)

    def __str__(self):
        s = f"{self.thai} - {self.english}\n"
        if len(self.syllables) > 1:
            for syllable in self.syllables:
                s += f"│  {syllable.thai}   ({syllable.english})\n"
        if self.map is not None:
            s += f"│map: {self.map} ({self.x}, {self.y})\n"
        return s

    def print(self):
        print(self)

    def draw(self, al, offset_x, offset_y):
        x = self.x * al.ui.cell_size + offset_x
        y = self.y * al.ui.cell_size + offset_y
        gfxdraw.aacircle(
            al.ui.screen,
            x + int(al.ui.cell_size / 2),
            y + int(al.ui.cell_size / 2),
            int(al.ui.cell_size / 2),
            (255, 0, 0),
        )
        al.ui.screen.blit(
            al.ui.fonts.garuda32.render(self.thai, True, (0, 255, 255)), (x, y - 20)
        )


class Words(object):
    def __init__(self):
        self.words: List[Word] = []
        self.words_per_map = {}  # a dictionary giving al the words for a given map

    def add_word(self, word: Word):
        self.words.append(word)
        if word.map:
            if word.map in self.words_per_map:
                self.words_per_map[word.map].append(word)
            else:
                self.words_per_map[word.map] = [word]

    def get_word(self, separated_form: str):
        for word in self.words:
            if word.separated_form == separated_form:
                return word

    def time_to_xp_loss(self, number_of_seconds: int):
        """
        For now, there is one xp lost per day.
        Might be more complex in the future.
        """
        number_of_days = int(number_of_seconds / 86400)
        return number_of_days

    def get_known_words(self):
        return [word for word in self.words if word.total_xp > 0]

    def __str__(self):
        s = ""
        for word in self.words:
            s += str(word)
        return s

    def print(self):
        print(self)

    def reset_words(self, al, xp=0):
        for word in self.words:
            word.reset(al, xp=xp)


class Sentence(object):
    def __init__(self, words: str, thai: str, english: str):
        super().__init__()
        self.thai = thai.replace("-", "").replace("_", "")
        self.words = []
        self.english = english
        words_in_sentence = thai.split("_")

        for word_in_sentence in words_in_sentence:
            word = words.get_word(word_in_sentence)
            if not word:
                print(f"ERROR: word {word} ({word_in_sentence}) is not in words!")
            self.words.append(word)

    def print(self):
        print(self)

    def __str__(self):
        s = f"{self.thai}\n"
        s += f"{self.english}\n"
        for word in self.words:
            s += str(word)
        return s


class Sentences(object):
    def __init__(self):
        self.sentences = []

    # def get_syllable(self, thai: str):
    #     for syllable in self.syllables:
    #         if syllable.thai == thai:
    #             return syllable
    #
    def add_sentence(self, sentence: Sentence):
        self.sentences.append(sentence)

    def __str__(self):
        s = ""
        for sentence in self.sentences:
            s += str(sentence) + "\n"
        return s

    def print(self):
        print(self)


#
# class UserWord(object):
#     """
#     The word in relation to the user
#     """
#     def __init__(self, word):
#         self.word = word
#         self.xp = 0
#         self.lvl = 1
#
#
# class UserWords(object):
#     def __init__(self):
#         self.user_words = []
#
#     def add_word(self, user_word: UserWord):
#         self.user_words.append(user_word)
#
#     # def get_word(self, separated_form: str):
#     #     for user_word in self.user_words:
#     #         if word.separated_form == separated_form:
#     #             return word
#
#     # def print(self):
#     #     for word in self.words:
#     #         word.print()
