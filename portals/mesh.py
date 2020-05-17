import random
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

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


def maybe_get_grid_x_and_grid_y_for_new_unit(
    temp_grid, unit_with_links_we_try_to_add, central_x, central_y
) -> Tuple[int, int, Optional[int], Optional[int]]:
    for adjacent_grid_x, adjacent_grid_y in get_coronas(
        central_x, central_y, unit_with_links_we_try_to_add.thai
    ):
        if grid_is_free(temp_grid, adjacent_grid_x, adjacent_grid_y):
            return central_x, central_y, adjacent_grid_x, adjacent_grid_y

    return central_x + 1, central_y + 1, None, None


def get_grid_x_and_grid_y_for_new_unit(
    temp_grid, unit_with_links_we_try_to_add, relevant_link
) -> Tuple[int, int]:
    grid_x = None
    grid_y = None
    central_x, central_y = relevant_link.grid_x, relevant_link.grid_y
    while grid_x is None:
        central_x, central_y, grid_x, grid_y = maybe_get_grid_x_and_grid_y_for_new_unit(
            temp_grid, unit_with_links_we_try_to_add, central_x, central_y
        )
    return grid_x, grid_y


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
        self.nexuses = self.make_nexuses()
        self.compounds = self.make_compounds()
        self.offset = Point(0, 0)
        self.goal_offset = Point(0, 0)
        self.selected_nexus: Optional[Nexus] = None

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
        self.offset.x = int(
            (self.offset.x * current_position_weight + self.goal_offset.x * goal_weight)
            / (current_position_weight + goal_weight)
        )
        self.offset.y = int(
            (self.offset.y * current_position_weight + self.goal_offset.y * goal_weight)
            / (current_position_weight + goal_weight)
        )

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

    def add_first_nexus(self, nexuses_to_add, already_added_units_thai, nexuses, temp_grid):
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
            grid_x=0,
            grid_y=0,
        )
        nexuses[new_nexus.thai] = new_nexus
        add_to_grid(temp_grid, new_nexus)

    def make_nexuses(self):
        nexuses = {}
        already_added_units_thai: List[str] = []
        nexuses_to_add = [value for key, value in self.units_with_links.items()]
        relevant_link = None
        temp_grid = {}
        self.add_first_nexus(nexuses_to_add, already_added_units_thai, nexuses, temp_grid)

        i = 0
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
                grid_x, grid_y = get_grid_x_and_grid_y_for_new_unit(
                    temp_grid, unit_with_links_we_try_to_add, relevant_link
                )
                new_nexus = Nexus(
                    al=self.al,
                    thai=unit_with_links_we_try_to_add.thai,
                    map=unit_with_links_we_try_to_add.map,
                    map_x=unit_with_links_we_try_to_add.map_x,
                    map_y=unit_with_links_we_try_to_add.map_y,
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
            self.goal_offset.y -= OFFSET_MOVEMENT
            ui.down = False
        if ui.up:
            self.goal_offset.y += OFFSET_MOVEMENT
            ui.up = False
        if ui.right:
            self.goal_offset.x -= OFFSET_MOVEMENT
            ui.right = False
        if ui.left:
            self.goal_offset.x += OFFSET_MOVEMENT
            ui.left = False
        if ui.space:
            self.goal_offset.x = -self.selected_nexus.screen_x + self.al.ui.width / 2
            self.goal_offset.y = -self.selected_nexus.screen_y + self.al.ui.height / 2
            # self.go_to_random_direction()
            ui.space = False
        if ui.hover:
            if self.selected_nexus:
                self.selected_nexus.on_hover(ui.hover)
                ui.hover = None
        if ui.click:
            if self.selected_nexus:
                self.selected_nexus.on_click()
                ui.click = None
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
