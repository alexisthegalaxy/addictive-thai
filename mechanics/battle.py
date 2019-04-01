import math
import random
import pygame
from typing import List
from all import All
from lexicon.items import Word
from lexicon.test_services import (
    pick_a_test_for_english_word,
    pick_a_test_for_thai_word,
)
from npc.npc import Npc


def square(x):
    return x * x


class Bubble(object):
    def __init__(self, word: Word, al, box):
        self.show_thai = bool(random.getrandbits(1))
        self.word = word
        self.al = al
        self.is_selected = False
        self.radius = 30
        self.color = (200, 0, 100)
        self.is_shown_in_thai = random.random() > 0.5

        self.hp = 10  # Each bubble has an amount of hp, so that the opponent has to work on it


        self.box_x = box[0]
        self.box_y = box[1]
        self.box_width = box[2]
        self.box_height = box[3]

        # The center of the circle
        self.x = random.randint(
            self.box_x + self.radius, self.box_x + self.box_height - self.radius
        )  # can be 0, ..., n-1
        self.y = random.randint(
            self.box_y + self.radius, self.box_y + self.box_width - self.radius
        )  # can be 0, ..., n-1

        self.speed_x = random.random() * 10
        self.speed_y = random.random() * 10

    def draw(self):
        ui = self.al.ui
        x_translated_inbox = int(self.x)
        y_translated_inbox = int(self.y)
        # the position we draw the circle at is the center of the circle
        pygame.draw.circle(
            ui.screen, self.color, (x_translated_inbox, y_translated_inbox), self.radius
        )
        shown_value = self.word.thai if self.is_shown_in_thai else self.word.english
        ui.screen.blit(
            ui.fonts.garuda32.render(shown_value, True, (0, 0, 0)),
            (x_translated_inbox - 15, y_translated_inbox - 20 - 15),
        )
        ui.screen.blit(
            ui.fonts.garuda32.render(str(self.hp), True, (0, 0, 0)),
            (x_translated_inbox - 15, y_translated_inbox - 20 - 15 + 20),
        )

    def interact(self, al):
        if al.ui.click:
            print("al.ui.click", al.ui.click)
            print(self.word.thai)

    def tick(self):
        if self.x + self.radius > self.box_width + self.box_x:
            if self.speed_x > 0:
                self.speed_x = -self.speed_x
            self.x = self.box_width + self.box_x - self.radius
        elif self.x - self.radius < self.box_x:
            if self.speed_x < 0:
                self.speed_x = -self.speed_x
            self.x = self.box_x + self.radius
        else:
            self.x += self.speed_x

        if self.y + self.radius > self.box_height + self.box_y:
            if self.speed_y > 0:
                self.speed_y = -self.speed_y
            self.y = self.box_y + self.box_height - self.radius
        elif self.y - self.radius < self.box_y:
            if self.speed_y < 0:
                self.speed_y = -self.speed_y
            self.y = self.box_y + self.radius
        else:
            self.y += self.speed_y

    def contains_point(self, point):
        return (
            math.sqrt(square(point[0] - self.x) + square(point[1] - self.y))
            <= self.radius
        )

    def reduce_hp(self, damage):
        self.hp -= damage


class Battle(object):
    """
    Winning results in getting some money.
    Opponent walk up to you when seeing you the first time.
    Trainers can be fought once a day - A rematch is triggered by talking to them.

    Fighting trainers:
        - ±6 Words are floating around in bubbles in the middle.
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

    def __init__(self, al: All, words, trainer: Npc) -> None:
        # UI
        self.x = al.ui.percent_width(0.07)
        self.y = al.ui.percent_height(0.07)
        self.height = al.ui.percent_height(0.86)
        self.width = al.ui.percent_width(0.86)

        self.al: All = al
        self.trainer: Npc = trainer
        self.words: List[Word] = words
        self.bubbles = []
        self.create_bubbles()
        self.selected_bubble_index = -1

        # properties for the opponent
        self.bubble_selected_by_opponent = None

    def create_bubbles(self) -> None:
        for word in self.words:
            self.bubbles.append(
                Bubble(word, self.al, (self.x, self.y, self.width, self.height))
            )

    def tick(self) -> None:
        """
        In this function, we operate actions supposed to happen at each tick of the clock
        """
        for bubble in self.bubbles:
            bubble.tick()

    def interact(self, al):
        if al.ui.click:
            for bubble in self.bubbles:
                if bubble.contains_point(al.ui.click):
                    last_bubble = len(self.bubbles) == 1
                    if bubble.is_shown_in_thai:
                        pick_a_test_for_thai_word(
                            al,
                            chosen_word=bubble.word,
                            test_success_callback=self.end_battle if last_bubble else None,
                        )
                    else:
                        pick_a_test_for_english_word(
                            al,
                            chosen_word=bubble.word,
                            test_success_callback=self.end_battle if last_bubble else None,
                        )
                    self.kill_bubble(bubble)
                    break
            al.ui.click = None

    def opponent_play(self):
        if self.bubble_selected_by_opponent is None or self.bubble_selected_by_opponent.hp == 0:
            self.opponent_select_bubble()
        else:
            self.bubble_selected_by_opponent.reduce_hp(1)
            if self.bubble_selected_by_opponent.hp <= 0:
                self.kill_bubble(self.bubble_selected_by_opponent)
                if len(self.bubbles) == 0:
                    self.end_battle()

    def opponent_select_bubble(self):
        self.bubble_selected_by_opponent = random.choice(self.bubbles)

    def draw(self):
        ui = self.al.ui
        screen = ui.screen
        pygame.draw.rect(
            screen, (200, 200, 200), (self.x, self.y, self.width, self.height)
        )
        pygame.draw.rect(
            screen, (0, 0, 0), [self.x, self.y, self.width, self.height], 1
        )

        # draw bubbles
        for bubble in self.bubbles:
            bubble.draw()

    def kill_bubble(self, bubble):
        bubble.hp = 0
        self.bubbles.remove(bubble)

    def end_battle(self):
        self.al.active_battle = None
        self.al.active_npc = self.trainer
        self.al.active_npc.active_dialog = self.al.active_npc.dialog_1
        self.al.active_npc.active_line_index += 1

        battle_money = 1
        self.al.learner.money += battle_money
