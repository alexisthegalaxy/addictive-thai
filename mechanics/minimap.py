from datetime import datetime

import pygame, os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def draw_square(screen, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)


class MinimapCell(object):
    def __init__(self, x, y, typ):
        self.x = x
        self.y = y
        self.typ = typ

    def draw(self, ui, x, y, size, blinking=False):
        # print(x, y)
        screen = ui.screen
        color = self.typ.postcolor

        if blinking and datetime.now().microsecond > 1000000/2:
            color = (255, 0, 0)
        pygame.draw.rect(screen, color, (x, y, size, size))


class Minimap(object):
    def __init__(self, al, x=None, y=None, size=40):
        from overworld import get_cell_type_dictionary
        self.learner_x = al.learner.x + al.mas.current_map.x_shift
        self.learner_y = al.learner.y + al.mas.current_map.y_shift
        self.al = al
        self.x = self.learner_x if x is None else x
        self.y = self.learner_y if y is None else y
        self.size = size
        self.x1 = self.x - self.size
        self.x2 = self.x + self.size
        self.y1 = self.y - self.size
        self.y2 = self.y + self.size
        self.table = []
        self.cell_dictionary = get_cell_type_dictionary()
        text_file_path = f'{DIR_PATH}/../ow/map_text_files/postmap'
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
        for x, file_line in enumerate(self.file_lines[self.x1:self.x2]):
            line = []
            for y, character in enumerate(file_line[self.y1:self.y2]):
                try:
                    cell_type = self.cell_dictionary[character]
                except KeyError:
                    cell_type = CellTypes.none
                line.append(MinimapCell(x=x + self.x1, y=y + self.y1, typ=cell_type))
            self.table.append(line)

    def change_size(self, goes_up=False, goes_down=False):
        down = {
            20: 40,
            40: 60,
            60: 90,
            90: 120,
            120: 120,
        }
        up = {
            20: 20,
            40: 20,
            60: 40,
            90: 60,
            120: 90,
        }
        if goes_up:
            self.size = up[self.size]
        if goes_down:
            self.size = down[self.size]


    def interact(self):
        offset = self.size
        ui = self.al.ui
        if self.al.active_presentation:
            self.al.active_presentation.interact()
            return
        if ui.down:
            self.y += offset
            ui.down = False
            self.recompute()
        if ui.up:
            self.y -= offset
            ui.up = False
            self.recompute()
        if ui.right:
            self.x += offset
            ui.right = False
            self.recompute()
        if ui.left:
            self.x -= offset
            ui.left = False
            self.recompute()
        if ui.plus:
            self.change_size(goes_up=True)
            ui.plus = False
            print(self.size)
            self.recompute()
        if ui.minus:
            self.change_size(goes_down=True)
            print(self.size)
            ui.minus = False
            self.recompute()

    def cell_should_blink(self, x, y):
        x = x + self.x1
        y = y + self.y1
        offset = int(self.size / 30) or 1
        return self.learner_x - offset < x < self.learner_x + offset and self.learner_y - offset < y < self.learner_y + offset

    def draw(self):
        pixel_size = 90 * 4 / self.size
        for x, line in enumerate(self.table):
            for y, cell in enumerate(line):
                cell.draw(self.al.ui, 240 + x * pixel_size, y * pixel_size, pixel_size, blinking=self.cell_should_blink(x, y))
