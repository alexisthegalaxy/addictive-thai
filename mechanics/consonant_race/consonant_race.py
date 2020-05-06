import random
import time

import pygame
from typing import List

from all import All
from lexicon.items import Letter
from npc.npc import Npc
from enum import Enum

from sounds.play_sound import play_thai_word


class Class(Enum):
    LOW = "LOW"
    MID = "MID"
    HIGH = "HIGH"


class ConsonantRace(object):
    def __init__(self, al: All, consonants, npc: Npc) -> None:
        self.al: All = al
        self.npc = npc
        self.consonants: List[Letter] = consonants
        self.index = 0

        random.shuffle(self.consonants)
        self.active_consonant = self.consonants[0]
        self.total_time = npc.hp
        self.beginning_time = time.time()

        # UI
        self.x = al.ui.percent_width(0.07)
        self.y = al.ui.percent_height(0.07)
        self.height = al.ui.percent_height(0.86)
        self.width = al.ui.percent_width(0.86)
        self.rendered_consonant = al.ui.fonts.sarabun128.render(self.active_consonant.thai, True, (0, 0, 0))

    def tick(self) -> None:
        if time.time() > self.total_time + self.beginning_time:
            self.defeat()

    def guessed_right(self):
        self.go_to_next_consonant()

    def guessed_wrong(self):
        self.defeat()

    def guess(self, guess: str):
        if guess == self.active_consonant.class_:
            self.guessed_right()
        else:
            self.guessed_wrong()

    def interact(self):
        # DOWN is LOW
        # SPACE is MID
        # UP is HIGH
        if self.al.ui.down:
            self.guess(Class.LOW.value)
            self.al.ui.down = False
        if self.al.ui.space:
            self.guess(Class.MID.value)
            self.al.ui.space = False
        if self.al.ui.up:
            self.guess(Class.HIGH.value)
            self.al.ui.up = False

    def go_to_next_consonant(self):
        self.index += 1
        try:
            self.active_consonant = self.consonants[self.index]
            self.rendered_consonant = self.al.ui.fonts.sarabun128.render(self.active_consonant.thai, True, (0, 0, 0))
        except IndexError:
            self.victory()

    def draw_timer(self, ui):
        height = ui.percent_height(0.05)
        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)
        yellow = (255, 255, 0)
        green = (0, 255, 0)

        left_time = self.total_time - (time.time() - self.beginning_time)

        time_left_percentage = min(max(left_time / self.total_time, 0), 1)

        if time_left_percentage < 0.2:
            time_left_color = red
        elif time_left_percentage < 0.5:
            time_left_color = yellow
        else:
            time_left_color = green

        # 1 - draw white background
        pygame.draw.rect(
            ui.screen, white, [0, 0, ui.width, height]
        )
        # 2 - draw color
        pygame.draw.rect(
            ui.screen, time_left_color, [0, 0, ui.percent_width(time_left_percentage), height]
        )
        # 3 - draw black edge
        pygame.draw.rect(
            ui.screen, black, [0, 0, ui.width, height], 1
        )

    def draw_instructions_and_letter(self, ui):
        explanatory_string = f"What's the class of this consonant?"
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        ui.screen.blit(ui.fonts.sarabun32.render(explanatory_string, True, (0, 0, 0)), (x, y))

        instructions_string = f"Press [UP] for High, [SPACE] for MID, and [DOWN] for LOW"
        x = ui.percent_width(0.13)
        y = ui.percent_height(0.2)
        ui.screen.blit(ui.fonts.sarabun24.render(instructions_string, True, (0, 0, 0)), (x, y))

        x = ui.percent_width(0.5)
        y = ui.percent_height(0.25)
        ui.screen.blit(self.rendered_consonant, (x - self.rendered_consonant.get_width() / 2, y))

    def draw_background(self, ui):
        pygame.draw.rect(
            ui.screen, (200, 200, 200), (self.x, self.y, self.width, self.height)
        )
        pygame.draw.rect(
            ui.screen, (0, 0, 0), [self.x, self.y, self.width, self.height], 1
        )

    def draw(self):
        ui = self.al.ui
        self.draw_background(ui)
        self.draw_instructions_and_letter(ui)
        self.draw_timer(ui)

    def defeat(self):
        self.end()
        self.al.learner.money -= max(self.al.active_npc.lost_money_on_defeat, 0)
        self.al.active_npc.active_dialog = self.al.active_npc.victory_dialog

    def victory(self):
        self.end()
        self.al.active_npc.active_dialog = self.al.active_npc.defeat_dialog
        self.al.active_npc.wants_battle = False
        self.al.learner.money += self.al.active_npc.money

    def end(self):
        self.al.active_consonant_race = None
        self.al.active_npc = self.npc
        self.al.active_npc.active_line_index = 0


