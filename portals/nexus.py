import math
import random

from lexicon.tests.tests import draw_box
from math_service.distance import distance_1d, distance_2d
from math_service.intersection import get_intersection_with_screen_border
from math_service.rect import rect_contains_point
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
        self.show_exit = False
        self.hovers_over_exit = False

    def draw(self):
        x = self.screen_x - self.width / 2 + self.al.mesh.offset.x
        y = self.screen_y - self.height / 2 + self.al.mesh.offset.y
        self.al.ui.screen.blit(self.rendered_letter, (x, y))
        if self.show_exit:
            self.draw_exit()
        if self.best_link and self.al.mesh.selected_nexus == self:
            best_link_x = self.best_link.screen_x - self.best_link.width / 2 + self.al.mesh.offset.x
            best_link_y = self.best_link.screen_y - self.best_link.height / 2 + self.al.mesh.offset.y
            intersection_with_screen = get_intersection_with_screen_border(self.al, (x, y), (best_link_x, best_link_y))
            if intersection_with_screen:
                int_x, int_y = intersection_with_screen
                if int_x >= self.al.ui.width - 100:
                    int_x -= 100
                if int_y == self.al.ui.height:
                    int_y -= 60
                draw_box(
                    screen=self.al.ui.screen,
                    fonts=self.al.ui.fonts,
                    font_size=12,
                    x=int_x,
                    y=int_y,
                    string=self.best_link.thai,
                )

    def draw_exit(self):
        x = self.screen_x + self.al.mesh.offset.x
        y = self.screen_y + self.al.mesh.offset.y
        draw_box(
            screen=self.al.ui.screen,
            fonts=self.al.ui.fonts,
            font_size=16,
            x=x - 65,
            y=y + 50,
            width=150,
            height=50,
            string="Exit from here" if self.can_exit() else "Can't exit here",
            selected=self.hovers_over_exit and self.can_exit(),
        )

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
        # self.selected = selected
        self.rendered_letter = self.font.render(self.thai, True, color)

    def can_exit(self) -> bool:
        return bool(self.map)

    def on_hover(self, point):
        distance_from_center = distance_2d(point, (self.screen_x + self.al.mesh.offset.x, self.screen_y + self.al.mesh.offset.y))
        if self.show_exit:
            center_x = self.screen_x + self.al.mesh.offset.x
            center_y = self.screen_y + self.al.mesh.offset.y
            if rect_contains_point((center_x - 65 - 10, center_y + 50 - 10, center_x - 65 + 150 + 10, center_y + 50 + 50 + 10), point):
                self.hovers_over_exit = True
                return
            else:
                self.hovers_over_exit = False
        if distance_from_center < 75:
            self.show_exit = True
            self.best_link = None
        else:
            self.show_exit = False
            hover_x, hover_y = point
            offset_from_center_x = hover_x - (self.screen_x + self.al.mesh.offset.x)
            offset_from_center_y = hover_y - (self.screen_y + self.al.mesh.offset.y)
            angle = math.atan2(offset_from_center_y, offset_from_center_x)

            best_fit = 100000
            best_link = None
            linked_angle = None
            for linked in self.linked:
                linked_angle = math.atan2(linked.screen_y - self.screen_y, linked.screen_x - self.screen_x)
                distance = distance_1d(linked_angle, angle)
                if distance < best_fit:
                    best_link = linked
                    best_fit = distance
            if best_fit < 0.3:
                self.best_link = best_link
                self.best_link_angle = linked_angle
            else:
                self.best_link = None
                self.best_link_angle = None
            # print(best_fit, '----------', angle, offset_from_center_x, offset_from_center_y)

    def on_click(self):
        if self.best_link:
            self.best_link.set_selected(True)
        if self.show_exit and self.can_exit():
            self.al.learner.exit_spirit_world(self.map, self.map_x, self.map_y)
