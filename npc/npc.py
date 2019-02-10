import pygame
from typing import List

from all import All
from direction import string_from_direction, opposite_direction
from lexicon.items import Word
from lexicon.learning import Learning
from sounds.play_sound import play_thai_word


def can_turn(sprite_type):
    if sprite_type == "sign":
        return False
    return True


class Npc(object):
    def __init__(
        self,
        al,
        name,
        ma,
        x,
        y,
        dialog_0,
        dialog_1,
        dialog_2,
        dialog_3,
        direction,
        sprite,
        taught_word: Word = None,
    ):
        self.name = name
        self.ma = ma
        self.sprite = sprite
        self.x = x
        self.y = y
        self.dialog_0: List[str] = dialog_0
        self.dialog_1: List[str] = dialog_1
        self.dialog_2: List[str] = dialog_2
        self.dialog_3: List[str] = dialog_3
        self.review_dialog: List[str] = ["Do you want to review the word"]
        self.dialogs = [self.dialog_0, self.dialog_1, self.dialog_2, self.dialog_3]
        self.active_dialog: List[str] = self.dialog_0
        self.direction = direction
        self.active_line_index = -1
        self.color = (0, 222, 222)
        self.taught_word = taught_word

        self.process_dialog(al)

    def process_dialog(self, al):
        for dialog in self.dialogs:
            for i, line in enumerate(dialog):
                dialog[i] = line.replace("[Name]", al.learner.name)
        if self.taught_word:
            self.review_dialog[0] = (
                self.review_dialog[0] + f" {self.taught_word.thai} ?"
            )

    def is_saying_last_sentence(self):
        return self.active_line_index == len(self.active_dialog) - 1

    def special_interaction(self, al):
        if self.sprite == "nurse":
            if self.active_line_index == -1:
                play_thai_word("welcome")
            if self.active_line_index == 0:
                al.learner.inn_heal()
        if self.sprite == "sign":
            if self.active_line_index == -1:
                play_thai_word(self.name)
        if self.taught_word:
            if self.is_saying_last_sentence() and (
                self.active_dialog == self.dialog_0
                or self.active_dialog == self.review_dialog
            ):
                al.active_learning = Learning(al=al, word=self.taught_word, npc=self)
                al.active_learning.goes_to_first_step()

    def interact(self, al):
        # Then this is the beginning of the interaction with that NPC
        if not al.active_npc:
            if self.taught_word:  # If this NPC teaches
                if self.taught_word.total_xp >= 5:  # If the word is known
                    self.active_dialog = self.review_dialog
        else:
            al.active_npc = self

        self.special_interaction(al)
        self.active_line_index += 1
        if self.active_line_index >= len(self.active_dialog):
            self.active_line_index = -1
            al.active_npc = None
        self.direction = opposite_direction(al.learner.direction)

    def draw_ow(self, al, x, y):
        sprite = None
        if can_turn(self.sprite):
            sprite_name = f"{self.sprite}_{string_from_direction(self.direction)}"
            if sprite_name in al.ui.npc_sprites:
                sprite = al.ui.npc_sprites[sprite_name]
        else:
            if self.sprite in al.ui.npc_sprites:
                sprite = al.ui.npc_sprites[self.sprite]

        if sprite:
            al.ui.screen.blit(sprite, [x, y])
        else:
            pygame.draw.rect(
                al.ui.screen,
                self.color,
                pygame.Rect(x, y, al.ui.cell_size, al.ui.cell_size),
            )

    def draw(self, al):
        offset_x = -al.ui.cell_size * (al.learner.x - 7)
        offset_y = -al.ui.cell_size * (al.learner.y - 4)

        if (not al.learner.can_move()) and al.learner.movement:
            movement_offset_x, movement_offset_y = al.learner.movement.get_offset()
            offset_x += movement_offset_x * al.ui.cell_size
            offset_y += movement_offset_y * al.ui.cell_size

        x = self.x * al.ui.cell_size + offset_x
        y = self.y * al.ui.cell_size + offset_y
        self.draw_ow(al, x, y)

    def switch_to_dialog(self, dialog):
        self.active_dialog = dialog
        self.active_line_index = 0

    def draw_text(self, al: All):
        # 1 - Background:
        ui = al.ui
        x = 0
        y = ui.percent_height(0.9)
        width = ui.percent_width(1)
        height = ui.percent_height(0.1)

        screen = ui.screen
        pygame.draw.rect(screen, (150, 150, 150), (x, y, width, height))
        pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)

        # 2 - Draw text:
        text = self.active_dialog[self.active_line_index]
        rendered_text = ui.fonts.garuda32.render(text, True, (0, 0, 0))
        screen.blit(rendered_text, (x + 10, y + int(height / 2.2) - 20))
