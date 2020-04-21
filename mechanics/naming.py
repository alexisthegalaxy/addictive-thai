import pygame
from typing import List
from all import All
from lexicon.items import Letter
from lexicon.tests.tests import draw_box, TestAnswerBox
from npc.npc import Npc
import random


VALIDATE_STRING = "Validate"


class Naming(object):
    def __init__(self, al: All, name: str, npc: Npc = None, distractors: List[str] = None, image=None, prompt="Spell its True Name!", victory_callback=None) -> None:
        self.al: All = al
        self.npc: Npc = npc
        self.name = name
        letters_in_name = [letter for letter in name]
        self.distractors = letters_in_name + distractors if distractors else letters_in_name
        random.shuffle(self.distractors)
        self.image = al.ui.npc_sprites[image] if image else None
        self.image_size = self.image.get_size() if self.image else None
        self.prompt = prompt
        self.victory_callback = victory_callback

        self.answer = ""
        self.selected_option_index = None
        self.hover = None

        # UI
        self.x = al.ui.percent_width(0.07)
        self.y = al.ui.percent_height(0.07)
        self.height = al.ui.percent_height(0.86)
        self.width = al.ui.percent_width(0.86)
        self.prompt_y = self.al.ui.percent_height(0.09) + (self.image_size[1] if self.image_size else 0)
        self.rendered_prompt = self.al.ui.fonts.sarabun32.render(self.prompt, True, (0, 0, 0))
        self.answer_y = self.prompt_y + self.rendered_prompt.get_height() + al.ui.percent_height(0.02)

        self.boxes = self.make_boxes()

    def actualize(self):
        self.boxes = self.make_boxes()

    def make_boxes(self):
        initial_x = self.al.ui.percent_width(0.1)
        x = initial_x
        y = self.answer_y + self.al.ui.percent_height(0.15)
        width = self.al.ui.percent_width(0.1)
        height = self.al.ui.percent_height(0.08)

        boxes = []
        for i, distractor in enumerate(self.distractors):
            try:
                letter = Letter.get_by_thai(distractor)
            except UnboundLocalError:
                try:
                    letter = Letter.get_by_thai(f"-{distractor}")
                except UnboundLocalError:
                    letter = Letter.get_by_thai(f"{distractor}-")
            letter_is_greyed_out = not letter.get_total_xp() > 1
            boxes.append(
                TestAnswerBox(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    string=f" {distractor} ",
                    index=i,
                    greyed=letter_is_greyed_out,
                )
            )
            x += width + 20
            if x > self.al.ui.percent_width(0.8):
                x = initial_x
                y += height + self.al.ui.percent_height(0.04)
        boxes.append(
            TestAnswerBox(
                x=x,
                y=y,
                width=self.al.ui.percent_width(0.2) + 20,
                height=height,
                string=VALIDATE_STRING,
                index=len(self.distractors),
            )
        )
        return boxes

    def interact(self, al):
        if al.ui.hover:
            self.hover = None
            for box in self.boxes:
                if box.contains(al.ui.hover):
                    self.hover = al.ui.hover
                    al.ui.hover = None
                    for other_box in self.boxes:
                        other_box.selected = False
                    box.selected = True
                    self.selected_option_index = box.index
                    break
        if al.ui.click:
            for box in self.boxes:
                if not box.greyed and box.contains(al.ui.click):
                    self.learner_select_option(box.string)
                    break
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
        answer_height = self.al.ui.percent_height(0.1)
        draw_box(
            screen=self.al.ui.screen,
            fonts=self.al.ui.fonts,
            x=self.al.ui.width / 2 - answer_width / 2,
            y=self.answer_y,
            width=answer_width,
            height=answer_height,
            font_size=48,
            string=f" {self.answer}",
            centered=True,
        )

    def draw_distractors(self):
        draw_tooltip = False
        for box in self.boxes:
            box.draw(
                screen=self.al.ui.screen,
                fonts=self.al.ui.fonts,
            )
            if self.selected_option_index == box.index and box.greyed and self.hover:
                draw_tooltip = True
        if draw_tooltip:
            draw_box(
                self.al.ui.screen,
                self.al.ui.fonts,
                x=self.hover[0],
                y=self.hover[1],
                font_size=24,
                width=self.al.ui.percent_width(0.3),
                height=self.al.ui.percent_height(0.07),
                string="You must first learn this letter!",
                thickness=3,
            )


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

    def learner_select_option(self, string):
        if string == VALIDATE_STRING:
            self.end_naming(success=self.answer == self.name)
        else:
            cleaned_string = string.replace(' ', '').replace('-', '')
            self.answer += cleaned_string

    def end_naming(self, success=False):
        # Called by the escape key, and also when clicking on Validate
        self.al.active_naming = None
        self.al.active_npc = self.npc
        self.answer = ""
        if success:
            if self.victory_callback:
                self.victory_callback(self.al)
            self.al.active_npc.active_dialog = self.al.active_npc.defeat_dialog
            self.al.active_npc.active_line_index = 0
        else:
            self.al.active_npc.active_dialog = self.al.active_npc.victory_dialog
            self.al.active_npc.active_line_index = 0
            self.al.learner.hurt(0.25)
