from datetime import datetime

import pygame, os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def want_to_launch_map(al, x=None, y=None, size=40, show_learner=True, interest_point=None):
    # if al.mas.current_map.x_shift != -1 and al.mas.current_map.y_shift != -1:
    al.active_minimap = Minimap(al, x=x, y=y, size=size, show_learner=show_learner, interest_point=interest_point)


def draw_square(screen, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)


class MinimapCell(object):
    def __init__(self, x, y, typ, blinking_color=None):
        self.x = x
        self.y = y
        self.typ = typ
        self.blinking_color = blinking_color

    def draw(self, ui, x, y, size):
        # print(x, y)
        screen = ui.screen
        color = self.typ.postcolor

        if self.blinking_color and datetime.now().microsecond > 1_000_000 / 2:
            color = self.blinking_color
        pygame.draw.rect(screen, color, (x, y, size, size))


class Minimap(object):
    def __init__(
        self, al, x=None, y=None, size=40, show_learner=True, interest_point=None
    ):
        from overworld import get_cell_type_dictionary
        self.show_learner = show_learner
        self.interest_point = interest_point
        self.learner_x = al.learner.x + al.mas.current_map.x_shift
        self.learner_y = al.learner.y + al.mas.current_map.y_shift
        self.al = al
        if self.interest_point:
            self.x, self.y = self.interest_point
        elif x and y:
            self.x = x
            self.y = y
        else:
            self.x = self.learner_x
            self.y = self.learner_y
        self.size = size
        self.x1 = self.x - self.size
        self.x2 = self.x + self.size
        self.y1 = self.y - self.size
        self.y2 = self.y + self.size
        self.table = []
        self.cell_dictionary = get_cell_type_dictionary()
        text_file_path = f"{DIR_PATH}/../ow/map_text_files/postmap"
        with open(text_file_path, "r") as f:
            self.file_lines = f.readlines()
        self.recompute()

    def recompute(self):
        from overworld import CellTypes

        self.table = []
        self.x1 = self.x - self.size
        self.x2 = self.x + self.size
        self.y1 = self.y - self.size
        self.y2 = self.y + self.size
        for x, file_line in enumerate(self.file_lines[self.x1 : self.x2]):
            line = []
            for y, character in enumerate(file_line[self.y1 : self.y2]):
                try:
                    cell_type = self.cell_dictionary[character]
                except KeyError:
                    cell_type = CellTypes.none
                line.append(
                    MinimapCell(
                        x=x + self.x1,
                        y=y + self.y1,
                        typ=cell_type,
                        blinking_color=self.cell_should_blink(x, y),
                    )
                )
            self.table.append(line)

    def change_size(self, goes_up=False, goes_down=False):
        down = {20: 40, 40: 60, 60: 90, 90: 120, 120: 120}
        up = {20: 20, 40: 20, 60: 40, 90: 60, 120: 90}
        if goes_up:
            self.size = up[self.size]
        if goes_down:
            self.size = down[self.size]

    def click_in_map(self, click):
        try:
            x, y = click
            return 240 < x < 240 + len(self.table) * 90 * 4 / self.size and 0 < y < self.al.ui.percent_height(1)
        except TypeError:
            return False

    def interact(self):
        ui = self.al.ui
        if ui.down:
            self.y += self.size
            ui.down = False
            self.recompute()
        if ui.up:
            self.y = max(self.y - self.size, self.size)
            ui.up = False
            self.recompute()
        if ui.right:
            self.x += self.size
            ui.right = False
            self.recompute()
        if ui.left:
            self.x = max(self.x - self.size, self.size)
            ui.left = False
            self.recompute()
        if ui.plus:
            self.change_size(goes_up=True)
            ui.plus = False
            self.recompute()
            self.x = max(self.x, self.size)
            self.y = max(self.y, self.size)
        if ui.minus:
            self.change_size(goes_down=True)
            ui.minus = False
            self.recompute()
        if ui.click:
            if not self.click_in_map(ui.click):
                self.al.active_minimap = None
                ui.click = False

    def cell_should_blink(self, x, y):
        x = x + self.x1
        y = y + self.y1
        offset = int(self.size / 30) or 1
        if (
            self.show_learner
            and self.learner_x - offset < x < self.learner_x + offset
            and self.learner_y - offset < y < self.learner_y + offset
        ):
            return 255, 0, 0
        if (
            self.interest_point
            and self.interest_point[0] - offset < x < self.interest_point[0] + offset
            and self.interest_point[1] - offset < y < self.interest_point[1] + offset
        ):
            return 255, 255, 0

        else:
            return None

    def draw(self):
        pixel_size = 90 * 4 / self.size
        for x, line in enumerate(self.table):
            for y, cell in enumerate(line):
                cell.draw(self.al.ui, 240 + x * pixel_size, y * pixel_size, pixel_size)
