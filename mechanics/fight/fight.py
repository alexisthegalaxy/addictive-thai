from enum import Enum

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


class AttackPhase(object):
    def __init__(self):
        pass

    def draw(self):
        pass


class DefensePhase(object):
    def __init__(self):
        pass

    def draw(self):
        pass


class FightStep(Enum):
    NONE = 0
    BEGINNING = 1

    DEFENSE_PHASE_STARTING_MESSAGE = 2
    DEFENSE_PHASE_TEST = 3
    DEFENSE_PHASE_END_MESSAGE = 4
    DEFENSE_PHASE_END_SPECIAL_EFFECT = 5

    ATTACK_PHASE_STARTING_MESSAGE = 6
    ATTACK_PHASE_PICK_WEAPON = 7
    ATTACK_PHASE_TEST = 8
    ATTACK_PHASE_TEST_RESULT = 9
    ATTACK_PHASE_SPECIAL_EFFECT = 10

    CONGRATULATION_MESSAGE = 11
    END = 12


class Fight(object):
    """
    https://docs.google.com/document/d/1VutaI2jjKVKtTi7dJIlB5unj_gQUbOEqOrTINYCJXpQ
    """
    def __init__(self, al: All, words, npc: Npc, starting: str = "player") -> None:
        self.al: All = al
        self.npc = npc
        self.words: List[Word] = words

        if starting == "player":
            self.current_step = FightStep.ATTACK_PHASE_STARTING_MESSAGE.value
            self.active_phase = AttackPhase(al, words, npc)
        elif starting == "npc":
            self.current_step = FightStep.DEFENSE_PHASE_STARTING_MESSAGE.value
            self.active_phase = DefensePhase()
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

    def interact(self, al):
        if al.ui.click:
            for bubble in []:
                if bubble.contains_point(al.ui.click):
                    if bubble.is_shown_in_thai:
                        pick_a_test_for_thai_word(
                            al,
                            chosen_word=bubble.word,
                            test_success_callback=self.solves_test,
                            test_failure_callback=self.fails_test,
                        )
                    else:
                        pick_a_test_for_english_word(
                            al,
                            chosen_word=bubble.word,
                            test_success_callback=self.solves_test,
                            test_failure_callback=self.fails_test,
                        )
                    bubble.hp = 0
                    break
            al.ui.click = None

    def solves_test(self):
        pass

    def fails_test(self):
        pass

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
        sprite_name = f"{self.al.learner.sprite}_{string_from_direction(Direction.DOWN)}"
        if sprite_name in ui.npc_sprites:
            sprite = ui.npc_sprites[sprite_name]
            ui.screen.blit(sprite, [face_x, face_y])
        else:
            pygame.draw.rect(
                self.al.ui.screen,
                self.npc.color,
                pygame.Rect(face_x, face_y, ui.cell_size, ui.cell_size),
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
        # for bubble in self.bubbles:
        #     if bubble.status == BUBBLE_STATUS_FREE:
        #         bubble.draw()
        # self.draw_secondary()


    def end_fight(self):
        self.al.active_fight = None
        self.al.active_npc = self.npc
        # victory = self.bubbles_solved >= self.bubbles_solved_by_opponent
        # if victory:
        #     self.al.active_npc.active_dialog = self.al.active_npc.defeat_dialog
        #     self.al.active_npc.active_line_index = 0
        #     self.al.active_npc.wants_battle = False
        #     battle_money = self.al.active_npc.money
        #     self.al.learner.money += battle_money
        #     self.al.active_battle = None
        #     print('VICTORY!!!')
        # else:
        #     self.al.active_npc.active_dialog = self.al.active_npc.victory_dialog
        #     self.al.active_npc.active_line_index = 0
        #     print('DEFEAT!!!')
