from dataclasses import dataclass
from datetime import datetime
from time import mktime
import time
import pygame
from typing import List, Tuple, Optional

from all import All
from direction import string_from_direction, opposite_direction, Direction, dir_equal
from lexicon.items import Word
from lexicon.learning import Learning
from sounds.play_sound import play_thai_word


def can_turn(sprite_type):
    if sprite_type == "sign":
        return False
    return True


@dataclass
class Position:
    x: int
    y: int


class Npc(object):
    def __init__(
        self,
        al,
        name,
        ma,
        x,
        y,
        standard_dialog=None,  # pre-fight, normal talk, pre-learn
        defeat_dialog=None,  # post-fight
        victory_dialog=None,  # post-fight
        dialog_3=None,
        direction=Direction.UP,
        sprite="kid",
        taught_word: Word = None,
        battle_words: List[Word] = None,
        money: int = 5,  # amount given when lost the fight
        eyesight: int = 5,  # how far the trainer can see
        wanna_meet: bool = False,  # if true, non trainers will also walk to the learner and start talking
    ):
        standard_dialog = standard_dialog or ["Hello"]
        defeat_dialog = defeat_dialog or ["Well done!"]
        victory_dialog = victory_dialog or ["I won! Try again when you're stronger!"]
        dialog_3 = dialog_3 or []

        self.name = name
        self.ma = ma
        self.sprite = sprite
        self.x = x
        self.y = y
        self.money = money
        self.standard_dialog: List[str] = standard_dialog
        self.defeat_dialog: List[str] = defeat_dialog
        self.victory_dialog: List[str] = victory_dialog
        self.dialog_3: List[str] = dialog_3
        self.review_dialog: List[str] = ["Do you want to review the word"]
        self.dialogs = [
            self.standard_dialog,
            self.defeat_dialog,
            self.victory_dialog,
            self.dialog_3,
        ]
        self.active_dialog: List[str] = self.standard_dialog
        self.direction = direction
        self.active_line_index = -1
        self.color = (0, 222, 222)
        self.taught_word = taught_word
        self.battle_words = battle_words

        self.wants_battle = True
        self.wanna_meet = wanna_meet
        self.eyesight = eyesight
        self.have_exclamation_mark_until = None
        self.must_walk_to = None
        self.walked_float = 0
        self.draw_text_since = 0

        self.process_dialog(al)

    def process_dialog(self, al):
        for dialog in self.dialogs:
            for i, line in enumerate(dialog):
                dialog[i] = line.replace("[Name]", al.learner.name)
        if self.taught_word:
            self.review_dialog[0] = (
                self.review_dialog[0] + f" {self.taught_word.thai} ?"
            )

    def is_trainer(self):
        return bool(self.battle_words)

    def sees_learner(self, al) -> Optional[Position]:
        """
        :return: the must_walk_to position if there's one, else None
        """
        if self.direction == Direction.UP:
            if (
                al.learner.x == self.x
                and al.learner.y < self.y
                and self.y - al.learner.y <= self.eyesight
            ):
                can_walk_to_trainer = True
                for y in range(al.learner.y, self.y):
                    can_walk_to_trainer = (
                        can_walk_to_trainer
                        and al.mas.current_map.get_cell_at(self.x, y).walkable()
                    )
                if can_walk_to_trainer:
                    print(self.name + ": I can walk to you!")
                    return Position(x=al.learner.x, y=al.learner.y + 1)
        elif self.direction == Direction.DOWN:
            if (
                al.learner.x == self.x
                and al.learner.y > self.y
                and al.learner.y - self.y <= self.eyesight
            ):
                can_walk_to_trainer = True
                for y in range(self.y, al.learner.y):
                    can_walk_to_trainer = (
                        can_walk_to_trainer
                        and al.mas.current_map.get_cell_at(self.x, y).walkable()
                    )
                if can_walk_to_trainer:
                    print(self.name + ": I can walk to you!")
                    return Position(x=al.learner.x, y=al.learner.y - 1)
        elif self.direction == Direction.RIGHT:
            if (
                al.learner.y == self.y
                and al.learner.x > self.x
                and al.learner.x - self.x <= self.eyesight
            ):
                can_walk_to_trainer = True
                for x in range(self.x, al.learner.x):
                    can_walk_to_trainer = (
                        can_walk_to_trainer
                        and al.mas.current_map.get_cell_at(x, self.y).walkable()
                    )
                if can_walk_to_trainer:
                    print(self.name + ": I can walk to you!")
                    return Position(x=al.learner.x - 1, y=al.learner.y)
        elif self.direction == Direction.LEFT:
            if (
                al.learner.y == self.y
                and al.learner.x < self.x
                and self.x - al.learner.x <= self.eyesight
            ):
                can_walk_to_trainer = True
                for x in range(al.learner.x, self.x):
                    can_walk_to_trainer = (
                        can_walk_to_trainer
                        and al.mas.current_map.get_cell_at(x, self.y).walkable()
                    )
                if can_walk_to_trainer:
                    print(self.name + ": I can walk to you!")
                    return Position(x=al.learner.x + 1, y=al.learner.y)
        return None

    def is_saying_last_sentence(self):
        return self.active_line_index == len(self.active_dialog) - 1

    def special_interaction(self, al):
        if self.name == "nurse":
            if self.active_line_index == -1:
                play_thai_word("welcome")
            if self.active_line_index == 0:
                al.learner.inn_heal()
        # if self.sprite == "sign":
        if self.active_line_index == -1:
            #         play_thai_word(self.name)
            play_thai_word(self.name)
        if self.taught_word:
            if self.is_saying_last_sentence() and (
                self.active_dialog == self.standard_dialog
                or self.active_dialog == self.review_dialog
            ):
                al.active_learning = Learning(al=al, word=self.taught_word, npc=self)
                al.active_learning.goes_to_first_step()
        if self.battle_words:
            if self.is_saying_last_sentence():
                if self.active_dialog == self.standard_dialog:
                    from mechanics.battle import Battle

                    al.active_battle = Battle(
                        al=al, words=self.battle_words, trainer=self
                    )
                if self.active_dialog == self.victory_dialog:
                    al.learner.faints()
                    self.active_dialog = self.standard_dialog
                    self.active_line_index = 0

    def interact(self, al):
        # Then this is the beginning of the interaction with that NPC
        self.wanna_meet = False
        self.reset_cursor()
        if not al.active_npc:
            if self.taught_word:  # If this NPC teaches
                if self.taught_word.total_xp >= 5:  # If the word is known
                    self.active_dialog = self.review_dialog
        al.active_npc = self

        self.special_interaction(al)
        self.active_line_index += 1
        if self.active_line_index >= len(self.active_dialog):
            self.active_line_index = -1
            al.active_npc = None
        self.direction = opposite_direction(al.learner.direction)

    def get_precise_position(self, x, y):
        if dir_equal(self.direction, Direction.UP):
            return x, y - self.walked_float
        if dir_equal(self.direction, Direction.DOWN):
            return x, y + self.walked_float
        if dir_equal(self.direction, Direction.RIGHT):
            return x + self.walked_float, y
        if dir_equal(self.direction, Direction.LEFT):
            return x - self.walked_float, y

    def draw_ow(self, al, x, y):
        # get sprite
        sprite = None
        if can_turn(self.sprite):
            sprite_name = f"{self.sprite}_{string_from_direction(self.direction)}"
            if sprite_name in al.ui.npc_sprites:
                sprite = al.ui.npc_sprites[sprite_name]
        else:
            if self.sprite in al.ui.npc_sprites:
                sprite = al.ui.npc_sprites[self.sprite]

        x, y = self.get_precise_position(x, y)

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

        if self.have_exclamation_mark_until:
            now = mktime(datetime.now().timetuple())
            if self.have_exclamation_mark_until > now:
                al.ui.screen.blit(
                    al.ui.images["exclamation_mark"], [x, y - al.ui.cell_size]
                )
            else:
                self.have_exclamation_mark_until = None

    def gets_exclamation_mark(self):
        now = mktime(datetime.now().timetuple())
        self.have_exclamation_mark_until = now + 1

    def makes_a_step_towards_goal(self, al):
        if self.must_walk_to.x > self.x:
            self.x += 1
        if self.must_walk_to.x < self.x:
            self.x -= 1
        if self.must_walk_to.y > self.y:
            self.y += 1
        if self.must_walk_to.y < self.y:
            self.y -= 1
        if Position(x=self.x, y=self.y) == self.must_walk_to:
            self.must_walk_to = None
            al.learner.direction = opposite_direction(self.direction)
            self.interact(al)

    def switch_to_dialog(self, dialog):
        self.active_dialog = dialog
        self.active_line_index = 0
        self.reset_cursor()

    def reset_cursor(self):
        self.draw_text_since = time.time()

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
        now = time.time()
        number_of_characters_to_show = int((now - self.draw_text_since)*75)
        text = self.active_dialog[self.active_line_index][:number_of_characters_to_show]
        rendered_text = ui.fonts.garuda32.render(text, True, (0, 0, 0))
        screen.blit(rendered_text, (x + 10, y + int(height / 2.2) - 20))
