import random
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
