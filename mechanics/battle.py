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
from direction import string_from_direction, Direction


BUBBLE_STATUS_FREE = 0
BUBBLE_STATUS_WON = 1
BUBBLE_STATUS_LOST = 2


def square(x):
    return x * x


class Bubble(object):
    def __init__(self, word: Word, al, box, max_hp):
        self.status = BUBBLE_STATUS_FREE
        self.show_thai = bool(random.getrandbits(1))
        self.word = word
        self.al = al
        self.is_selected = False
        self.radius = 40
        self.color = (200, 0, 100)
        self.is_shown_in_thai = random.random() > 0.5

        self.max_hp = max_hp  # Each bubble has an amount of hp, so that the opponent has to work on it
        self.hp = self.max_hp

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

    def draw_bubble(self, x, y):
        ui = self.al.ui
        # the position we draw the circle at is the center of the circle
        pygame.draw.circle(
            ui.screen, self.color, (x, y), self.radius
        )
        shown_value = self.word.thai if self.is_shown_in_thai else self.word.english
        ui.screen.blit(
            ui.fonts.garuda32.render(shown_value, True, (0, 0, 0)),
            (x - 15, y - 20 - 15),
        )
        if self.hp != 0 and self.hp != self.max_hp:
            ui.screen.blit(
                ui.fonts.garuda32.render(str(self.hp), True, (0, 0, 0)),
                (x - 15, y - 20 - 15 + 20),
            )

    def draw(self):
        x_translated_inbox = int(self.x)
        y_translated_inbox = int(self.y)
        self.draw_bubble(x_translated_inbox, y_translated_inbox)

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
        - If you identify less by the end, you are knocked-out, and loses a 5th of you money

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
        self.selected_bubble = None
        self.bubbles_solved = 0

        # properties for the opponent
        self.bubble_selected_by_opponent = None
        self.bubbles_solved_by_opponent = 0

    def create_bubbles(self) -> None:
        max_hp = self.trainer.bubbles_max_hp
        for word in self.words:
            self.bubbles.append(
                Bubble(word, self.al, (self.x, self.y, self.width, self.height), max_hp)
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
                    self.selected_bubble = bubble
                    if bubble.is_shown_in_thai:
                        pick_a_test_for_thai_word(
                            al,
                            chosen_word=bubble.word,
                            test_success_callback=self.solve_bubble,
                        )
                    else:
                        pick_a_test_for_english_word(
                            al,
                            chosen_word=bubble.word,
                            test_success_callback=self.solve_bubble,
                        )
                    bubble.hp = 0
                    break
            al.ui.click = None

    def opponent_play(self):
        if self.bubble_selected_by_opponent is None or self.bubble_selected_by_opponent.hp == 0:
            self.opponent_select_bubble()
        else:
            self.bubble_selected_by_opponent.reduce_hp(1)
            if self.bubble_selected_by_opponent.hp <= 0:
                self.bubble_selected_by_opponent.hp = 0
                self.bubble_selected_by_opponent.status = BUBBLE_STATUS_LOST
                self.bubbles_solved_by_opponent += 1
                if not [bubble for bubble in self.bubbles if bubble.status == BUBBLE_STATUS_FREE]:
                    self.end_battle()

    def opponent_select_bubble(self):
        if len(self.bubbles) > 0:
            self.bubble_selected_by_opponent = random.choice(self.bubbles)

    def draw_secondary(self):
        ui = self.al.ui
        screen = ui.screen
        # draw bubbles
        won_bubbles = 0
        lost_bubbles = 0
        for bubble in self.bubbles:
            if bubble.status == BUBBLE_STATUS_WON:
                bubble.draw_bubble(x=50, y=150 + ui.cell_size + won_bubbles * (ui.cell_size + 10))
                won_bubbles += 1
            elif bubble.status == BUBBLE_STATUS_LOST:
                bubble.draw_bubble(x=ui.percent_width(1.0) - ui.cell_size + 30, y=150 + ui.cell_size +lost_bubbles * (ui.cell_size + 10))
                lost_bubbles += 1

        # draw learner face
        face_x = 10
        face_y = 90
        pygame.draw.rect(
            screen, (150, 150, 150), (face_x, face_y, ui.cell_size, ui.cell_size)
        )
        pygame.draw.rect(
            screen, (0, 0, 0), (face_x, face_y, ui.cell_size, ui.cell_size), 1
        )
        sprite_name = f"{self.al.learner.sprite}_{string_from_direction(Direction.DOWN)}"
        if sprite_name in ui.npc_sprites:
            sprite = ui.npc_sprites[sprite_name]
            ui.screen.blit(sprite, [face_x, face_y])
        else:
            pygame.draw.rect(
                self.al.ui.screen,
                self.trainer.color,
                pygame.Rect(face_x, face_y, ui.cell_size, ui.cell_size),
            )

        # draw learner face
        face_x = ui.percent_width(1.0) - ui.cell_size - 10
        pygame.draw.rect(
            screen, (150, 150, 150), (face_x, face_y, ui.cell_size, ui.cell_size)
        )
        pygame.draw.rect(
            screen, (0, 0, 0), (face_x, face_y, ui.cell_size, ui.cell_size), 1
        )
        sprite_name = f"{self.trainer.sprite}_{string_from_direction(Direction.DOWN)}"
        if sprite_name in ui.npc_sprites:
            sprite = ui.npc_sprites[sprite_name]
            ui.screen.blit(sprite, [face_x, face_y])
        else:
            pygame.draw.rect(
                self.al.ui.screen,
                self.trainer.color,
                pygame.Rect(face_x, face_y, ui.cell_size, ui.cell_size),
            )

    def draw(self):
        # draw background
        ui = self.al.ui
        screen = ui.screen
        pygame.draw.rect(
            screen, (200, 200, 200), (self.x, self.y, self.width, self.height)
        )
        pygame.draw.rect(
            screen, (0, 0, 0), [self.x, self.y, self.width, self.height], 1
        )
        for bubble in self.bubbles:
            if bubble.status == BUBBLE_STATUS_FREE:
                bubble.draw()
        self.draw_secondary()

    def solve_bubble(self):
        self.selected_bubble.status = BUBBLE_STATUS_WON
        self.bubbles_solved += 1
        last_bubble = not [bubble for bubble in self.bubbles if bubble.status == BUBBLE_STATUS_FREE]
        if last_bubble:
            self.end_battle()

    def end_battle(self):
        self.al.active_battle = None
        self.al.active_npc = self.trainer
        victory = self.bubbles_solved >= self.bubbles_solved_by_opponent
        if victory:
            self.al.active_npc.active_dialog = self.al.active_npc.defeat_dialog
            self.al.active_npc.active_line_index = 0
            self.al.active_npc.wants_battle = False
            battle_money = self.al.active_npc.money
            self.al.learner.money += battle_money
            self.al.active_battle = None
            print('VICTORY!!!')
        else:
            self.al.active_npc.active_dialog = self.al.active_npc.victory_dialog
            self.al.active_npc.active_line_index = 0
            print('DEFEAT!!!')
