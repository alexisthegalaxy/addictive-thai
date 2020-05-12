import random
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict

import pygame

from overworld import Ma
from portals.vocabulary import get_compounds, get_naive_units

OFFSET_MOVEMENT = 80


@dataclass
class UnitWithLinks:
    thai: str
    map: Ma
    map_x: int
    map_y: int
    linked: List["UnitWithLinks"]


@dataclass
class Unit:
    thai: str
    map: Ma
    map_x: int
    map_y: int
    linked: List["Unit"]
    grid_x: int
    grid_y: int


def get_corona_1(x, y, thai):
    random.seed(thai)
    adjacent_x_y = [(x - 1, y - 1), (x, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y)]
    random.shuffle(adjacent_x_y)
    return adjacent_x_y


def get_corona_2(x, y, thai):
    """
    Get the cells in a David star pattern around the central cell
    """
    random.seed(thai)
    adjacent_x_y = [(x - 1, y - 2), (x + 1, y - 1), (x + 2, y + 1), (x + 1, y + 2), (x - 1, y + 1), (x - 2, y - 1)]
    random.shuffle(adjacent_x_y)
    return adjacent_x_y


def get_corona_3(x, y, thai):
    """
    Get the cells in between the 6 summits of the David star pattern around the central cell
    """
    random.seed(thai)
    adjacent_x_y = [(x, y - 2), (x + 2, y), (x + 2, y + 2), (x, y + 2), (x - 2, y), (x - 2, y - 2)]
    random.shuffle(adjacent_x_y)
    return adjacent_x_y


def get_coronas(x, y, thai):
    return get_corona_1(x, y, thai) + get_corona_2(x, y, thai) + get_corona_3(x, y, thai)


def get_further_adjacent_cells(x, y, thai):
    # TODO the bigger circle around the cell
    return
    # random.seed(thai)
    # adjacent_x_y = [(x - 1, y - 1), (x, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y)]
    # random.shuffle(adjacent_x_y)
    # return adjacent_x_y


def grid_is_free(grid, x, y):
    return not (x in grid and y in grid[x])


def add_to_grid(grid, unit):
    x = unit.grid_x
    y = unit.grid_y
    if x not in grid:
        grid[x] = {}
    grid[x][y] = unit


class Mesh(object):
    def __init__(self, al):
        self.compounds = get_compounds()
        self.naive_units = get_naive_units(al)
        self.units_with_links: Dict[str, UnitWithLinks] = self.get_units_with_links(al)
        self.current_unit: str = ""  # where the learner stands at the moment
        self.grid = {}
        self.units = self.make_units(al)  # contain their links as well as their position in space
        self.offset_y = 0
        self.offset_x = 0

    def get_units_with_links(self, al):
        units_with_links = {}
        for naive_unit in self.naive_units:
            units_with_links[naive_unit] = UnitWithLinks(
                thai=naive_unit,
                map=self.naive_units[naive_unit].map,
                map_x=self.naive_units[naive_unit].x,
                map_y=self.naive_units[naive_unit].y,
                linked=[],
            )
        for compound in self.compounds:
            try:
                units_with_links[compound.word_1].linked.append(units_with_links[compound.word_2])
            except KeyError:
                print(f'KeyError!! {compound.word_1} was not added to the list of naive units')
                raise KeyError

            try:
                units_with_links[compound.word_2].linked.append(units_with_links[compound.word_1])
            except KeyError:
                print(f'KeyError!! {compound.word_2} was not added to the list of naive units')
                raise KeyError
        return units_with_links

    def make_units(self, al):
        units = {}
        already_added_units_thai: List[str] = []
        units_to_add = [value for key, value in self.units_with_links.items()]
        i = 0
        relevant_link = None

        # We add the first element:
        first_unit = units_to_add[0]
        units_to_add.remove(first_unit)
        already_added_units_thai.append(first_unit.thai)
        new_unit = Unit(
            thai=first_unit.thai,
            map=first_unit.map,
            map_x=first_unit.map_x,
            map_y=first_unit.map_y,
            linked=first_unit.linked,
            grid_x=0,
            grid_y=0,
        )
        units[new_unit.thai] = new_unit
        temp_grid = {}  # a dictionary of dictionary that we can use with temp_grid[x][y]
        add_to_grid(temp_grid, new_unit)

        # We add the rest
        while len(units_to_add):
            has_already_added_link = False
            try:
                unit_with_links_we_try_to_add = units_to_add[i]
            except IndexError:
                i = 0
                continue

            for linked in unit_with_links_we_try_to_add.linked:
                if linked.thai in already_added_units_thai:
                    relevant_link = units[linked.thai]
                    has_already_added_link = True  # TODO make this better and put it where it can have more neighbors
            if has_already_added_link:
                units_to_add.remove(unit_with_links_we_try_to_add)
                grid_x = None
                grid_y = None
                central_x, central_y = relevant_link.grid_x, relevant_link.grid_y
                while not grid_x:
                    for adjacent_grid_x, adjacent_grid_y in get_coronas(central_x, central_y, unit_with_links_we_try_to_add.thai):
                        if grid_is_free(temp_grid, adjacent_grid_x, adjacent_grid_y):
                            grid_x, grid_y = adjacent_grid_x, adjacent_grid_y
                            break
                    central_x, central_y = central_x + 1, central_y + 1

                # we make the proper unit
                new_unit = Unit(
                    thai=unit_with_links_we_try_to_add.thai,
                    map=unit_with_links_we_try_to_add.map,
                    map_x=unit_with_links_we_try_to_add.map_x,
                    map_y=unit_with_links_we_try_to_add.map_y,
                    linked=unit_with_links_we_try_to_add.linked,
                    grid_x=grid_x,
                    grid_y=grid_y,
                )
                add_to_grid(temp_grid, new_unit)
                units[new_unit.thai] = new_unit
                already_added_units_thai.append(unit_with_links_we_try_to_add.thai)
            else:
                i += 1
                if i >= len(units_to_add):
                    i = 0
        self.grid = temp_grid
        # before returning we need to do a pass where we convert the linked in units from UnitswithLinks to proper Units

        print(Counter([len(unit.linked) for key, unit in units.items()]))
        return units

    def interact(self, al):
        ui = al.ui
        if ui.down:
            self.offset_y -= OFFSET_MOVEMENT
            ui.down = False
        if ui.up:
            self.offset_y += OFFSET_MOVEMENT
            ui.up = False
        if ui.right:
            self.offset_x -= OFFSET_MOVEMENT
            ui.right = False
        if ui.left:
            self.offset_x += OFFSET_MOVEMENT
            ui.left = False
        # if ui.hover:
        #     self.hovered_box = None
        #     for box in self.letter_boxes:
        #         if ui.hover in box:
        #             for other_box in self.letter_boxes:
        #                 other_box.hovered = False
        #             self.hovered_box = box
        #             box.hovered = ui.hover
        #             ui.hover = None
        #             break
        # if ui.click:
        #     for box in self.letter_boxes:
        #         if ui.click in box:
        #             ui.click = None
        #             self.launch_presentation(box.letter)
        #             break
        if ui.escape:
            al.learner.in_portal_world = False
            al.ui.escape = False

    def draw_background(self, al):
        ui = al.ui
        pygame.draw.rect(ui.screen, (0, 0, 0), (0, 0, ui.width, ui.height))

    def render_x(self, x):
        return x * 120 + 300 + self.offset_x

    def render_y(self, y, x):
        return y * 120 + 300 - x * 60 + self.offset_y

    def draw_current_unit(self, al):
        for compound in self.compounds:
            screen = al.ui.screen
            color = (255, 0, 0)
            unit_1 = self.units[compound.word_1]
            unit_2 = self.units[compound.word_2]
            x_1, y_1 = (unit_1.grid_x, unit_1.grid_y)
            x_2, y_2 = (unit_2.grid_x, unit_2.grid_y)
            point_1 = (self.render_x(x_1), self.render_y(y_1, x_1))
            point_2 = (self.render_x(x_2), self.render_y(y_2, x_2))
            pygame.draw.aaline(screen, color, point_1, point_2)
        for x, column in self.grid.items():
            for y, unit in column.items():
                rendered_letter = al.ui.fonts.sarabun32.render(unit.thai, True, (255, 255, 255))
                render_x = self.render_x(x) - rendered_letter.get_width() / 2
                render_y = self.render_y(y, x) - rendered_letter.get_height() / 2
                al.ui.screen.blit(rendered_letter, (render_x, render_y))

    def draw(self, al):
        self.draw_background(al)
        self.draw_current_unit(al)
