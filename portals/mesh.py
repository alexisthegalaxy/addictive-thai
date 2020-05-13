import random
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict

import pygame

from overworld import Ma
from portals.compound import Compound
from portals.coronas import get_coronas
from portals.definitions import OFFSET_MOVEMENT, DISTANCE
from portals.nexus import Nexus
from portals.vocabulary import get_naive_compounds, get_naive_units


@dataclass
class UnitWithLinks:
    thai: str
    map: Ma
    map_x: int
    map_y: int
    linked: List["UnitWithLinks"]


@dataclass
class Point:
    x: int
    y: int


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
        self.al = al
        self.naive_compounds = get_naive_compounds()
        self.naive_units = get_naive_units(al)
        self.units_with_links: Dict[str, UnitWithLinks] = self.get_units_with_links()
        self.grid = {}
        self.nexuses = self.make_nexuses()  # contain their links as well as their position in space
        self.compounds = self.make_compounds()
        self.offset = Point(0, 0)
        self.goal_offset = Point(0, 0)
        self.selected_nexus = None

    def make_compounds(self):
        compounds = []
        for naive_compound in self.naive_compounds:
            compounds.append(
                Compound(
                    al=self.al,
                    english=naive_compound.english,
                    nexus_1=self.nexuses[naive_compound.word_1],
                    nexus_2=self.nexuses[naive_compound.word_2],
                )
            )
        return compounds

    def tick(self):
        goal_weight = 1
        current_position_weight = 15
        self.offset.x = int((self.offset.x * current_position_weight + self.goal_offset.x * goal_weight) / (current_position_weight + goal_weight))
        self.offset.y = int((self.offset.y * current_position_weight + self.goal_offset.y * goal_weight) / (current_position_weight + goal_weight))

    def get_units_with_links(self):
        units_with_links = {}
        for naive_unit in self.naive_units:
            units_with_links[naive_unit] = UnitWithLinks(
                thai=naive_unit,
                map=self.naive_units[naive_unit].map,
                map_x=self.naive_units[naive_unit].x,
                map_y=self.naive_units[naive_unit].y,
                linked=[],
            )
        for compound in self.naive_compounds:
            try:
                units_with_links[compound.word_1].linked.append(
                    units_with_links[compound.word_2]
                )
            except KeyError:
                print(
                    f"KeyError!! {compound.word_1} or {compound.word_2} was not added to the list of naive units"
                )
                raise KeyError

            try:
                units_with_links[compound.word_2].linked.append(
                    units_with_links[compound.word_1]
                )
            except KeyError:
                print(
                    f"KeyError!! {compound.word_2} or {compound.word_1} was not added to the list of naive units"
                )
                raise KeyError
        return units_with_links

    def make_nexuses(self):
        nexuses = {}
        already_added_units_thai: List[str] = []
        nexuses_to_add = [value for key, value in self.units_with_links.items()]
        i = 0
        relevant_link = None

        # We add the first element:
        first_unit = nexuses_to_add[0]
        nexuses_to_add.remove(first_unit)
        already_added_units_thai.append(first_unit.thai)
        new_nexus = Nexus(
            al=self.al,
            thai=first_unit.thai,
            map=first_unit.map,
            map_x=first_unit.map_x,
            map_y=first_unit.map_y,
            # linked=first_unit.linked,
            grid_x=0,
            grid_y=0,
        )
        nexuses[new_nexus.thai] = new_nexus
        temp_grid = (
            {}
        )  # a dictionary of dictionary that we can use with temp_grid[x][y]
        add_to_grid(temp_grid, new_nexus)

        # We add the rest
        while len(nexuses_to_add):
            has_already_added_link = False
            try:
                unit_with_links_we_try_to_add = nexuses_to_add[i]
            except IndexError:
                i = 0
                continue

            for linked in unit_with_links_we_try_to_add.linked:
                if linked.thai in already_added_units_thai:
                    relevant_link = nexuses[linked.thai]
                    has_already_added_link = (
                        True
                    )  # TODO make this better and put it where it can have more neighbors
            if has_already_added_link:
                nexuses_to_add.remove(unit_with_links_we_try_to_add)
                grid_x = None
                grid_y = None
                central_x, central_y = relevant_link.grid_x, relevant_link.grid_y
                while not grid_x:
                    for adjacent_grid_x, adjacent_grid_y in get_coronas(
                        central_x, central_y, unit_with_links_we_try_to_add.thai
                    ):
                        if grid_is_free(temp_grid, adjacent_grid_x, adjacent_grid_y):
                            grid_x, grid_y = adjacent_grid_x, adjacent_grid_y
                            break
                    central_x, central_y = central_x + 1, central_y + 1

                # we make the proper unit
                new_nexus = Nexus(
                    al=self.al,
                    thai=unit_with_links_we_try_to_add.thai,
                    map=unit_with_links_we_try_to_add.map,
                    map_x=unit_with_links_we_try_to_add.map_x,
                    map_y=unit_with_links_we_try_to_add.map_y,
                    # linked=unit_with_links_we_try_to_add.linked,
                    grid_x=grid_x,
                    grid_y=grid_y,
                )
                add_to_grid(temp_grid, new_nexus)
                nexuses[new_nexus.thai] = new_nexus
                already_added_units_thai.append(unit_with_links_we_try_to_add.thai)
            else:
                i += 1
                if i >= len(nexuses_to_add):
                    i = 0
        self.grid = temp_grid
        # before returning we need to do a pass where we convert the linked in units from UnitswithLinks to proper Units
        for naive_compound in self.naive_compounds:
            nexuses[naive_compound.word_1].linked.append(nexuses[naive_compound.word_2])
            nexuses[naive_compound.word_2].linked.append(nexuses[naive_compound.word_1])
        # print(Counter([len(unit.linked) for key, unit in units.items()]))
        return nexuses

    def learner_enters(self, current_unit: str):
        self.nexuses[current_unit].set_selected(True)

    def go_to_random_direction(self):
        linked = self.selected_nexus.linked
        random.choice(linked).set_selected(True)

    def interact(self, al):
        ui = al.ui
        if ui.down:
            self.offset.y -= OFFSET_MOVEMENT
            ui.down = False
        if ui.up:
            self.offset.y += OFFSET_MOVEMENT
            ui.up = False
        if ui.right:
            self.offset.x -= OFFSET_MOVEMENT
            ui.right = False
        if ui.left:
            self.offset.x += OFFSET_MOVEMENT
            ui.left = False
        if ui.space:
            self.go_to_random_direction()
            ui.space = False
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

    def draw_background(self):
        ui = self.al.ui
        pygame.draw.rect(ui.screen, (0, 0, 0), (0, 0, ui.width, ui.height))

    def render_x(self, x):
        return x * DISTANCE + 300 + self.offset.x

    def render_y(self, y, x):
        return y * DISTANCE + 300 - x * DISTANCE / 2 + self.offset_y

    def draw_mesh(self):
        for compound in self.compounds:
            compound.draw()
        for nexus in self.nexuses:
            self.nexuses[nexus].draw()

    def draw(self):
        self.draw_background()
        self.draw_mesh()
