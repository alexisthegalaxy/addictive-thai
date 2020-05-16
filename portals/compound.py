import pygame

from portals.nexus import Nexus


class Compound(object):
    def __init__(self, al, nexus_1: Nexus, nexus_2: Nexus, english: str):
        self.al = al
        self.english = english
        self.nexus_1 = nexus_1
        self.nexus_2 = nexus_2
        self.screen_x_1 = nexus_1.screen_x
        self.screen_y_1 = nexus_1.screen_y
        self.screen_x_2 = nexus_2.screen_x
        self.screen_y_2 = nexus_2.screen_y

    def is_linked_to_current_nexus(self):
        return self.al.mesh.selected_nexus in [self.nexus_1, self.nexus_2]

    def is_hovered(self):
        a = {self.al.mesh.selected_nexus, self.al.mesh.selected_nexus.best_link}
        b = {self.nexus_1, self.nexus_2}
        return a == b
        return {self.al.mesh.selected_nexus, self.al.mesh.selected_nexus.best_link} == {self.nexus_1, self.nexus_2}

    def draw(self):
        # https://stackoverflow.com/questions/30578068/pygame-draw-anti-aliased-thick-line
        is_linked_to_current_nexus = self.is_linked_to_current_nexus()
        is_hovered = is_linked_to_current_nexus and self.is_hovered()
        if is_linked_to_current_nexus:
            if is_hovered:
                color = (60, 255, 255)
            else:
                color = (60, 120, 120)
        else:
            color = (60, 60, 60)
        if is_linked_to_current_nexus:
            if is_hovered:
                thickness = 50
            else:
                thickness = 30
        else:
            thickness = 10

        pygame.draw.line(
            self.al.ui.screen,
            color,
            (self.screen_x_1 + self.al.mesh.offset.x, self.screen_y_1 + self.al.mesh.offset.y),
            (self.screen_x_2 + self.al.mesh.offset.x, self.screen_y_2 + self.al.mesh.offset.y),
            thickness,
        )
