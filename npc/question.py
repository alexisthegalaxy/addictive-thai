from typing import Callable

import pygame


class Question(object):
    def __init__(self, precursor_text: str, choice_1: str, choice_2: str, choice_1_callback: Callable, choice_2_callback: Callable):
        # The question that appears, upon the end of which we get the two choices
        self.precursor_text = precursor_text
        self.choice_1 = choice_1  # the default choice
        self.choice_2 = choice_2
        # If the callback does nothing, then the dialog just continues as normal
        # The callback takes (al, npc) as parameters
        self.choice_1_callback = choice_1_callback
        self.choice_2_callback = choice_2_callback
        self.selected_choice = 1  # either 1 or 2 for now - could be any number in the future
        self.selected_choice_max = 2

    def add_to_index(self, amount):
        self.selected_choice += amount
        if amount > 0:
            if self.selected_choice > self.selected_choice_max:
                self.selected_choice = 1
        else:
            if self.selected_choice <= 0:
                self.selected_choice = self.selected_choice_max
        print(f'selected choice is now {self.selected_choice}')

    def execute_callback(self, al, npc):
        if self.selected_choice == 1:
            self.choice_1_callback(al, npc)
        elif self.selected_choice == 2:
            self.choice_2_callback(al, npc)

    def interact(self, al):
        if al.ui.up:
            self.add_to_index(-1)
            al.ui.up = False
        if al.ui.down:
            self.add_to_index(1)
            al.ui.down = False

    def draw(self, al):
        ui = al.ui
        rendered_choice_1 = ui.fonts.sarabun32.render(self.choice_1, True, (0, 0, 0))
        rendered_choice_2 = ui.fonts.sarabun32.render(self.choice_2, True, (0, 0, 0))

        # 1 - Background:
        y = ui.percent_height(0.71)
        width = ui.percent_width(0.05) + max(ui.percent_width(0.25), rendered_choice_1.get_width(), rendered_choice_2.get_width())
        x = ui.percent_width(0.99) - width
        height = ui.percent_height(0.2)

        screen = ui.screen
        pygame.draw.rect(screen, (150, 150, 150), (x, y, width, height))
        pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)

        # draw selected green rectangle
        height = ui.percent_height(0.1)
        if self.selected_choice == 1:
            y = ui.percent_height(0.71)
        else:
            y = ui.percent_height(0.81)
        pygame.draw.rect(screen, (150, 150, 150), (x, y, width, height))
        pygame.draw.rect(screen, (0, 255, 0), [x, y, width, height], 3)

        # Option 1
        # x = ui.percent_width(0.71)
        ui.screen.blit(rendered_choice_1, (x + 5, ui.percent_height(0.72)))

        # Option 2
        ui.screen.blit(rendered_choice_2, (x + 5, ui.percent_height(0.82)))
