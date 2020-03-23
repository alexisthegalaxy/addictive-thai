import pygame
from typing import List

from all import All
from learner import draw_hp
from lexicon.items import Word
from mechanics.fight.attack_phase import AttackPhase
from mechanics.fight.defense_phase import DefensePhase
from mechanics.fight.fight_steps import FightStep
from mechanics.fight.opponent import Opponent
from mechanics.fight.player import Player
from npc.npc import Npc
from direction import string_from_direction, Direction


class Fight(object):
    """
    https://docs.google.com/document/d/1VutaI2jjKVKtTi7dJIlB5unj_gQUbOEqOrTINYCJXpQ
    """

    def __init__(self, al: All, words, npc: Npc, starting: str = "player") -> None:
        self.al: All = al
        self.npc = npc  # used for the sprite mainly
        self.opponent = Opponent(al, npc)
        self.player = Player(al)
        self.words: List[Word] = words
        self.round = 0

        self.defense_phase = DefensePhase(al, self)
        self.attack_phase = None

        if starting == "player":
            self.current_step = FightStep.ATTACK_PHASE_PICK_WEAPON.value
            self.active_phase = self.attack_phase
        elif starting == "npc":
            self.current_step = FightStep.DEFENSE_PHASE_STARTING_MESSAGE.value
            self.active_phase = self.defense_phase
        else:
            raise ValueError

        # UI
        self.x = al.ui.percent_width(0.07)
        self.y = al.ui.percent_height(0.07)
        self.height = al.ui.percent_height(0.86)
        self.width = al.ui.percent_width(0.86)

    def tick(self) -> None:
        """
        In this function, we operate actions supposed to happen at each tick of the clock
        """
        pass

    def interact(self):
        self.active_phase.interact()

    def increase_round(self):
        self.round += 1

    def draw_secondary(self):
        ui = self.al.ui
        screen = ui.screen

        # draw learner face
        face_x = 10
        face_y = 90
        pygame.draw.rect(
            screen, (150, 150, 150), (face_x, face_y, ui.cell_size, ui.cell_size)
        )
        pygame.draw.rect(
            screen, (0, 0, 0), (face_x, face_y, ui.cell_size, ui.cell_size), 1
        )
        sprite_name = (
            f"{self.al.learner.sprite}_{string_from_direction(Direction.DOWN)}"
        )
        if sprite_name in ui.npc_sprites:
            sprite = ui.npc_sprites[sprite_name]
            ui.screen.blit(sprite, [face_x, face_y])
        else:
            pygame.draw.rect(
                self.al.ui.screen,
                self.npc.color,
                pygame.Rect(face_x, face_y, ui.cell_size, ui.cell_size),
            )
        draw_hp(
            self.al,
            self.player.hp,
            self.player.max_hp,
            x=face_x - 40 + 40 * self.player.max_hp,
            y=face_y + 80,
        )

        # draw opponent face
        face_x = ui.percent_width(1.0) - ui.cell_size - 10
        pygame.draw.rect(
            screen, (150, 150, 150), (face_x, face_y, ui.cell_size, ui.cell_size)
        )
        pygame.draw.rect(
            screen, (0, 0, 0), (face_x, face_y, ui.cell_size, ui.cell_size), 1
        )
        sprite_name = f"{self.npc.sprite}_{string_from_direction(Direction.DOWN)}"
        if sprite_name in ui.npc_sprites:
            sprite = ui.npc_sprites[sprite_name]
            ui.screen.blit(sprite, [face_x, face_y])
        else:
            pygame.draw.rect(
                self.al.ui.screen,
                self.npc.color,
                pygame.Rect(face_x, face_y, ui.cell_size, ui.cell_size),
            )
        draw_hp(
            self.al,
            self.opponent.hp,
            self.opponent.max_hp,
            x=face_x + 40,
            y=face_y + 80,
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

        self.active_phase.draw()
        self.draw_secondary()

    def defeat(self):
        self.end_fight()
        self.al.learner.hp = 0

        self.al.active_npc.active_dialog = self.al.active_npc.victory_dialog

    def victory(self):
        self.end_fight()

        self.al.active_npc.active_dialog = self.al.active_npc.defeat_dialog
        self.al.active_npc.wants_battle = False
        self.al.learner.money += self.al.active_npc.money

    def end_fight(self):
        self.al.active_fight = None
        self.al.active_npc = self.npc
        self.al.active_npc.active_line_index = 0
