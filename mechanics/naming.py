import random
import pygame
from typing import List
from all import All
from lexicon.tests.tests import draw_box
from npc.npc import Npc


class Naming(object):
    def __init__(self, al: All, name: str, npc: Npc = None, distractors: List[str] = None, image=None, prompt="Spell its True Name!") -> None:
        self.al: All = al
        self.npc: Npc = npc
        self.name = name
        self.distractors = distractors if distractors else []
        self.image = al.ui.npc_sprites[image] if image else None
        self.image_size = self.image.get_size() if self.image else None
        self.prompt = prompt

        self.answer = ""

        # UI
        self.x = al.ui.percent_width(0.07)
        self.y = al.ui.percent_height(0.07)
        self.height = al.ui.percent_height(0.86)
        self.width = al.ui.percent_width(0.86)
        self.prompt_y = self.al.ui.percent_height(0.09) + (self.image_size[1] if self.image_size else 0)
        self.rendered_prompt = self.al.ui.fonts.garuda32.render(self.prompt, True, (0, 0, 0))
        self.answer_y = self.prompt_y + self.rendered_prompt.get_height() + al.ui.percent_height(0.02)

    def interact(self, al):
        if al.ui.click:
            al.ui.click = None

    def draw_background(self):
        pygame.draw.rect(
            self.al.ui.screen, (200, 200, 200), (self.x, self.y, self.width, self.height)
        )
        pygame.draw.rect(
            self.al.ui.screen, (0, 0, 0), [self.x, self.y, self.width, self.height], 1
        )

    def maybe_draw_npc_image(self):
        if self.image:
            x = self.al.ui.width / 2 - self.image_size[0] / 2
            y = self.al.ui.percent_height(0.08)
            self.al.ui.screen.blit(self.image, [x, y])

    def draw_answer(self):
        answer_width = self.al.ui.percent_width(0.8)
        answer_height = self.al.ui.percent_height(0.07)
        draw_box(
            screen=self.al.ui.screen,
            fonts=self.al.ui.fonts,
            x=self.al.ui.width / 2 - answer_width / 2,
            y=self.answer_y,
            width=answer_width,
            height=answer_height,
            string=f" {self.answer} ",
            # bg=self.bg_color,
            # default_color=self.color,
            font_size=32,
            # thickness=1,
        )

    def draw_distractors(self):
        initial_x = self.al.ui.percent_width(0.1)
        x = initial_x
        y = self.answer_y + self.al.ui.percent_height(0.25)
        width = 100
        height = self.al.ui.percent_height(0.1)
        for distractor in self.distractors:
            draw_box(
                screen=self.al.ui.screen,
                fonts=self.al.ui.fonts,
                x=x,
                y=y,
                width=width,
                height=height,
                string=f" {distractor} ",
                # bg=self.bg_color,
                # default_color=self.color,
                font_size=32,
                # thickness=1,
            )
            x += width + 20
            if x > 1000:
                x = initial_x
                y += height + self.al.ui.percent_height(0.04)

    def draw_prompt(self):
        text_length = self.rendered_prompt.get_width()
        x = self.al.ui.width / 2 - text_length / 2
        self.al.ui.screen.blit(self.rendered_prompt, (x, self.prompt_y))

    def draw(self):
        self.draw_background()
        self.maybe_draw_npc_image()
        self.draw_prompt()
        self.draw_answer()
        self.draw_distractors()

    def end_naming(self):
        self.al.active_naming = None
        self.al.active_npc = self.npc
        success = True
        if success:
            self.al.active_npc.active_dialog = self.al.active_npc.defeat_dialog
            self.al.active_npc.active_line_index = 0
            self.al.active_npc.wants_battle = False
            battle_money = self.al.active_npc.money
            self.al.learner.money += battle_money
        else:
            self.al.active_npc.active_dialog = self.al.active_npc.victory_dialog
            self.al.active_npc.active_line_index = 0
            print('DEFEAT!!!')
