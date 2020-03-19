from dataclasses import dataclass
from datetime import datetime
import time
import pygame
from typing import List, Tuple, Optional, Union

# from all import All
from direction import string_from_direction, opposite_direction, Direction, dir_equal
from lexicon.items import Word, Letter
from lexicon.learning import LetterLearning, WordLearning
from models import xp_from_word, should_we_show_thai
from sounds.play_sound import play_thai_word


def _get_time_type():
    now = datetime.now().microsecond
    if now < 250_000:
        return 1
    if now < 500_000:
        return 2
    if now < 750_000:
        return 3
    return 4


def _process_dialog(dialog: List[str], al: "All"):
    for i, line in enumerate(dialog):
        dialog[i] = line.replace("[Name]", al.learner.name)


def _can_turn(sprite_type):
    return not (
        sprite_type
        in [
            "sign",
            "bed",
            "chest_open",
            "chest_closed",
            "television_on",
            "television_off",
            "boat",
        ]
        or "spell" in sprite_type
    )


def _is_gif(sprite):
    return sprite and sprite[0] == "_"


@dataclass
class Position:
    x: int
    y: int


class Npc(object):
    def __init__(
        self,
        al,
        ma,
        x,
        y,
        name="...",
        standard_dialog=None,  # pre-fight, normal talk, pre-learn
        defeat_dialog=None,  # post-fight
        victory_dialog=None,  # post-fight
        extra_dialog_1=None,  # use in triggers
        extra_dialog_2=None,  # use in triggers
        extra_dialog_3=None,  # use in triggers
        extra_dialog_4=None,  # use in triggers
        extra_dialog_5=None,  # use in triggers
        direction=Direction.UP,
        sprite="kid",
        taught: Union[Word, Letter] = None,
        battle_words: List[Word] = None,
        money: int = 5,  # amount given when lost the fight
        eyesight: int = 5,  # how far the trainer can see
        wanna_meet: bool = False,  # if true, non trainers will also walk to the learner and start talking
        bubbles_max_hp: int = 1000,
        appears_between: Tuple[int, int] = (0, 24),
        end_dialog_trigger_event: List[str] = None,
        beginning_dialog_trigger_event: List[str] = None,
        wobble=False,
    ):
        standard_dialog = standard_dialog or ["Hello"]
        defeat_dialog = defeat_dialog or ["Well done!"]
        victory_dialog = victory_dialog or ["I won! Try again when you're stronger!"]
        self.end_dialog_trigger_event = end_dialog_trigger_event or []
        self.beginning_dialog_trigger_event = beginning_dialog_trigger_event or []
        self.extra_dialog_1 = extra_dialog_1 or []
        self.extra_dialog_2 = extra_dialog_2 or []
        self.extra_dialog_3 = extra_dialog_3 or []
        self.extra_dialog_4 = extra_dialog_4 or []
        self.extra_dialog_5 = extra_dialog_5 or []

        self.name = name
        self.ma = ma
        self.sprite = sprite
        self.x = x
        self.y = y
        self.money = money
        self.standard_dialog: List[str] = standard_dialog
        self.defeat_dialog: List[str] = defeat_dialog
        self.victory_dialog: List[str] = victory_dialog
        self.review_dialog: List[str] = ["Do you want to review the word"]
        self.dialogs = [
            self.standard_dialog,
            self.defeat_dialog,
            self.victory_dialog,
            self.extra_dialog_1,
            self.extra_dialog_2,
            self.extra_dialog_3,
            self.extra_dialog_4,
            self.extra_dialog_5,
        ]
        self.active_dialog: List[str] = self.standard_dialog
        self.direction = direction
        self.active_line_index = -1
        self.color = (0, 222, 222)
        self.taught = taught
        self.battle_words = battle_words
        self.has_learning_mark = self.taught and xp_from_word(self.taught.id) <= 0
        self.wants_battle = True
        self.wanna_meet = wanna_meet
        self.eyesight = eyesight
        self.have_exclamation_mark_until = None
        # must_walk_to - list of position: must first walk to the first, then when reached the first is removed
        self.must_walk_to: List[Position] = []
        self.walked_float = 0
        self.draw_text_since = 0
        self.bubbles_max_hp = bubbles_max_hp
        self.appears_between = appears_between
        self.process_dialog(al)
        self.wobble = wobble

    def process_dialog(self, al):
        for dialog in self.dialogs:
            _process_dialog(dialog, al)
            # for i, line in enumerate(dialog):
            #     dialog[i] = line.replace("[Name]", al.learner.name)
        if self.taught:
            self.review_dialog[0] = self.review_dialog[0] + f" {self.taught.thai} ?"

    def is_trainer(self):
        return bool(self.battle_words)

    def sees_learner(self, al) -> Optional[List[Position]]:
        """
        :return: the must_walk_to position if there's one, else None
        """
        result = None
        if dir_equal(self.direction, Direction.UP):
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
                    result = Position(x=al.learner.x, y=al.learner.y + 1)
        elif dir_equal(self.direction, Direction.DOWN):
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
                    result = Position(x=al.learner.x, y=al.learner.y - 1)
        elif dir_equal(self.direction, Direction.RIGHT):
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
                    result = Position(x=al.learner.x - 1, y=al.learner.y)
        elif dir_equal(self.direction, Direction.LEFT):
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
                    result = Position(x=al.learner.x + 1, y=al.learner.y)
        if result:
            return [result]
        return None

    def is_saying_last_sentence(self) -> bool:
        return self.active_line_index == len(self.active_dialog) - 1

    def special_interaction(self, al):
        from event import execute_event

        if self.active_line_index == -1 and self.active_dialog == self.standard_dialog:
            for event in self.beginning_dialog_trigger_event:
                execute_event(event, al)
        if self.name == "nurse":
            if self.active_line_index == -1:
                play_thai_word("welcome")
            if self.active_line_index == 0:
                al.learner.inn_heal()
        if self.name == "bed":
            if self.active_line_index == 0:
                al.learner.bed_heal()
        if self.active_line_index == -1:
            play_thai_word(self.name)
        if self.taught:
            if self.is_saying_last_sentence() and (
                self.active_dialog == self.standard_dialog
                or self.active_dialog == self.review_dialog
            ):
                al.active_learning = (
                    WordLearning(al=al, word=self.taught, npc=self)
                    if isinstance(self.taught, Word)
                    else LetterLearning(al=al, letter=self.taught, npc=self)
                )
                al.active_learning.goes_to_first_step()
        if self == "is a spell": # TODO
            if self.is_saying_last_sentence() and (
                self.active_dialog == self.standard_dialog
                or self.active_dialog == self.review_dialog
            ):
                al.active_learning = (
                    WordLearning(al=al, word=self.taught, npc=self)
                    if isinstance(self.taught, Word)
                    else LetterLearning(al=al, letter=self.taught, npc=self)
                )
                al.active_learning.goes_to_first_step()
        if self.battle_words:
            if self.is_saying_last_sentence():
                if self.active_dialog == self.standard_dialog:
                    # from mechanics.battle import Battle
                    from mechanics.fight.fight import Fight

                    # al.active_battle = Battle(
                    #     al=al, words=self.battle_words, trainer=self
                    # )
                    al.active_fight = Fight(
                        al=al, words=self.battle_words, npc=self, starting="npc"
                    )
                if self.active_dialog == self.victory_dialog:
                    al.learner.faints()
                    self.active_dialog = self.standard_dialog
                    self.active_line_index = 0

    def interact(self, al):
        from event import execute_event

        self.direction = opposite_direction(al.learner.direction)
        self.wanna_meet = False
        self.has_learning_mark = False
        self.reset_cursor()
        if not al.active_npc:
            if self.taught:  # If this NPC teaches
                if self.taught.total_xp >= 5:  # If the word is known
                    self.active_dialog = self.review_dialog
        al.active_npc = self

        self.special_interaction(al)
        self.active_line_index += 1

        if self.active_line_index >= len(
            self.active_dialog
        ):  # if this is the end of the current dialog
            self.active_line_index = -1
            trigger_event = False
            if self.taught:
                if self.active_dialog == self.defeat_dialog:
                    trigger_event = True
            else:
                trigger_event = True
            if trigger_event:
                for event in self.end_dialog_trigger_event:
                    execute_event(event, al)
            al.active_npc = None

    def get_precise_position(self, x, y):
        if dir_equal(self.direction, Direction.UP):
            return x, y - self.walked_float
        if dir_equal(self.direction, Direction.DOWN):
            return x, y + self.walked_float
        if dir_equal(self.direction, Direction.RIGHT):
            return x + self.walked_float, y
        if dir_equal(self.direction, Direction.LEFT):
            return x - self.walked_float, y

    def should_appear(self):
        now = datetime.now().hour
        # appears_between = 23 - 5
        a0 = self.appears_between[0]
        a1 = self.appears_between[1]
        if a0 > a1:
            # a0 = 23
            # a1 = 5
            return now >= a0 or now < a1
        elif a1 > a0:
            # a0 = 8
            # a1 = 16
            return a0 <= now < a1
        return True

    def draw_ow(self, al, x, y):
        if not self.should_appear():
            return

        # get sprite
        time_type = _get_time_type()
        sprite_name = self.sprite
        sprite = None
        if _can_turn(self.sprite):
            sprite_name += f"_{string_from_direction(self.direction)}"
        if _is_gif(self.sprite):
            sprite_name = f"{self.sprite}_{time_type}"
        if sprite_name in al.ui.npc_sprites:
            sprite = al.ui.npc_sprites[sprite_name]

        x, y = self.get_precise_position(x, y)
        if self.wobble:
            if time_type == 1:
                y -= 1
            elif time_type == 2:
                y -= 2
            elif time_type == 3:
                y -= 1

        if sprite:
            al.ui.screen.blit(sprite, [x, y])
        else:
            pygame.draw.rect(
                al.ui.screen,
                self.color,
                pygame.Rect(x, y, al.ui.cell_size, al.ui.cell_size),
            )

        if self.have_exclamation_mark_until:
            now = time.time()
            if self.have_exclamation_mark_until > now:
                al.ui.screen.blit(
                    al.ui.images["exclamation_mark"], [x, y - al.ui.cell_size]
                )
            else:
                self.have_exclamation_mark_until = None
        elif self.has_learning_mark:
            al.ui.screen.blit(al.ui.images["learning_mark"], [x, y - al.ui.cell_size])

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

    def gets_exclamation_mark(self):
        now = time.time()
        self.have_exclamation_mark_until = now + 0.5

    def makes_a_step_towards_goal(self, al):
        must_walk_to = self.must_walk_to[0]
        if must_walk_to.x > self.x:
            self.x += 1
        elif must_walk_to.x < self.x:
            self.x -= 1
        elif must_walk_to.y > self.y:
            self.y += 1
        elif must_walk_to.y < self.y:
            self.y -= 1

        if self.x == must_walk_to.x and self.y == must_walk_to.y:
            self.must_walk_to.pop(0)
            if self.must_walk_to:
                if self.must_walk_to[0] == Position(x=0, y=0):
                    self.disappears(al)
                else:
                    must_walk_to = self.must_walk_to[0]
                    if must_walk_to.x > self.x:
                        self.direction = Direction.RIGHT
                    elif must_walk_to.x < self.x:
                        self.direction = Direction.LEFT
                    elif must_walk_to.y > self.y:
                        self.direction = Direction.DOWN
                    elif must_walk_to.y < self.y:
                        self.direction = Direction.UP
            elif al.learner.next_position() == (self.x, self.y):
                al.learner.direction = opposite_direction(self.direction)
                self.interact(al)

    def disappears(self, al):
        al.mas.current_map.npcs = [
            npc for npc in al.mas.current_map.npcs if npc != self
        ]

    def switch_to_dialog(self, dialog):
        self.active_dialog = dialog
        self.active_line_index = 0
        self.reset_cursor()

    def reset_cursor(self):
        self.draw_text_since = time.time()

    def _progressively_draw_line(
        self, line: str, number_of_characters_to_show, ui, screen, height, x, y
    ):
        line = line[:number_of_characters_to_show]
        rendered_text = ui.fonts.garuda32.render(line, True, (0, 0, 0))
        screen.blit(rendered_text, (x + 10, y + int(height / 2.2) - 20))

    def draw_text(self, al):
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
        number_of_characters_to_show = int((now - self.draw_text_since) * 75)
        text = self.active_dialog[self.active_line_index]
        if "//" in text:
            english, thai = text.split("//")
            we_should_show_thai = should_we_show_thai(thai)
            if we_should_show_thai:
                thai = thai.replace("_", "").replace("-", "")
                self._progressively_draw_line(
                    thai, number_of_characters_to_show, ui, screen, height, x, y
                )
            else:
                self._progressively_draw_line(
                    english, number_of_characters_to_show, ui, screen, height, x, y
                )
        else:
            self._progressively_draw_line(
                text, number_of_characters_to_show, ui, screen, height, x, y
            )
