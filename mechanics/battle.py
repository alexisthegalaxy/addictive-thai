import random
import pygame
from typing import List
from all import All
from lexicon.items import Word
from npc.npc import Npc


class Bubble(object):
    def __init__(self, word: Word):
        self.x = random.randint(0, 100)  # can be 0, ..., n-1
        self.y = random.randint(0, 100)  # can be 0, ..., n-1
        self.show_thai = bool(random.getrandbits(1))
        self.word = word
        self.is_selected = False

    def draw(self):
        self.y = random.randint(0, 100)  # can be 0, ..., n-1


class Battle(object):
    """
    Winning results in getting some money.
    Opponent walk up to you when seeing you the first time.
    Trainers can be fought once a day - A rematch is triggered by talking to them.

    Fighting trainers:
        - ±6 Words are floating around in the middle.
        - You have to identify more than the trainer.

        To make it more complex:
            - words can be linked into combo pieces when grouped by tone
                - Ex: linking HIGH tones can steal trainer's caught words
                What else:
                    Make trainer slower (if used by trainer: make words move faster?)
                    Put his words back into the pool
                    Add new words to the pool
                    Delete words from the pool?
                    Increase difficulty of tests for him (more sentences)
        You can see what word he's focusing and try to steal it from him by being fast.

    Eventually, later, I could have words have extra properties
    Example of properties:
        - Get more money at the end of the battle
        - Get an item at the end of the battle
        - Make all words show in thai/in english

    Some words are are shown in the aquarium in english, other in thai, randomly.
    """
    def __init__(self, al: All, words):
        self.al: All = al
        self.trainer: Npc = al.active_npc
        self.words: List[Word] = words
        self.bubbles = []
        self.create_bubbles()
        self.selected_bubble_index = -1

    def create_bubbles(self):
        for word in self.words:
            self.bubbles.append(Bubble(word))

    def draw(self):
        ui = self.al.ui
        x = ui.percent_width(0.07)
        y = ui.percent_height(0.07)
        height = ui.percent_height(0.86)
        width = ui.percent_width(0.86)
        screen = ui.screen
        fonts = ui.fonts
        pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height))
        pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)

        # draw bubbles
        for bubble in self.bubbles:
            bubble.draw()
