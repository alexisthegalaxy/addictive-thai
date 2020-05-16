import math
import random

from math_service.distance import distance_2d
from overworld import Ma
from portals.definitions import DISTANCE, RANDOM_RANGE

SELECTED_COLOR = (255, 255, 255)
UNSELECTED_COLOR = (100, 100, 100)


class Nexus(object):
    def __init__(
        self,
        al,
        thai: str,
        map: Ma,
        map_x: int,
        map_y: int,
        grid_x: int = 0,
        grid_y: int = 0,
    ):
        random.seed(thai)
        self.al = al
        self.thai = thai
        self.map = map
        self.map_x = map_x
        self.map_y = map_y
        self.linked = []
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.screen_x = (
            grid_x * DISTANCE + 300 + random.randint(-RANDOM_RANGE, RANDOM_RANGE)
        )
        self.screen_y = (
            grid_y * DISTANCE
            + 300
            - grid_x * DISTANCE / 2
            + random.randint(-RANDOM_RANGE, RANDOM_RANGE)
        )
        self.font = al.ui.fonts.sarabun96
        self.rendered_letter = self.font.render(thai, True, UNSELECTED_COLOR)
        self.width = self.rendered_letter.get_width()
        self.height = self.rendered_letter.get_height()
        self.best_link = None

    def draw(self):
        x = self.screen_x - self.width / 2 + self.al.mesh.offset.x
        y = self.screen_y - self.height / 2 + self.al.mesh.offset.y
        self.al.ui.screen.blit(self.rendered_letter, (x, y))

    def set_selected(self, selected: bool):
        if selected:
            if self.al.mesh.selected_nexus:
                self.al.mesh.selected_nexus.set_selected(False)
            self.al.mesh.selected_nexus = self
            color = (255, 255, 255)
            self.al.mesh.goal_offset.x = -self.screen_x + self.al.ui.width / 2
            self.al.mesh.goal_offset.y = -self.screen_y + self.al.ui.height / 2
        else:
            color = (100, 100, 100)
        self.selected = selected
        self.rendered_letter = self.font.render(self.thai, True, color)

    def on_hover(self, point):
        hover_x, hover_y = point
        offset_from_center_x = hover_x - (self.screen_x + self.al.mesh.offset.x)
        offset_from_center_y = hover_y - (self.screen_y + self.al.mesh.offset.y)
        angle = math.atan2(offset_from_center_y, offset_from_center_x)

        best_fit = 100000
        best_link = None
        for linked in self.linked:
            linked_angle = math.atan2(linked.screen_y - self.screen_y, linked.screen_x - self.screen_x)
            distance = distance_2d(linked_angle, angle)
            if distance < best_fit:
                best_link = linked
                best_fit = distance
        if best_fit < 0.3:
            self.best_link = best_link
        else:
            self.best_link = None
        # print(best_fit, '----------', angle, offset_from_center_x, offset_from_center_y)

    def on_click(self, point):
        if self.best_link:
            self.best_link.set_selected(True)
