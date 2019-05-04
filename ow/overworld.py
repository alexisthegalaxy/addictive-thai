import os
import random
from typing import List

import pygame

from lexicon.items import Words
from lexicon.test_services import pick_a_test_for_word
from npc.npc import Npc


class CellType(object):
    def __init__(self, letter, name, color, walkable, encounter_rate):
        self.letter = letter
        self.name = name
        self.color = color
        self.walkable = walkable
        self.encounter_rate = encounter_rate


class CellTypes:
    grass = CellType('.', 'grass', (100, 200, 100), True, 0.2)
    tree = CellType('t', 'tree', (85, 107, 47), False, 0)
    ground = CellType('^', 'ground', (176, 246, 176), True, 0)
    tall_grass = CellType('-', 'tall_grass', (0, 128, 0), True, 0.4)
    path = CellType('_', 'path', (200, 200, 200), True, 0)
    wall = CellType('W', 'wall', (22, 22, 22), False, 0)
    sign = CellType('s', 'sign', (71, 71, 71), False, 0)
    water = CellType('w', 'water', (57, 62, 255), False, 0.2)
    decoration = CellType('d', 'decoration', (123, 9, 9), False, 0)
    flower = CellType('f', 'flower', (231, 148, 193), True, 0)
    door = CellType('0', 'door', (255, 0, 204), True, 0)
    inn_floor = CellType('I', 'inn_floor', (117, 199, 242), True, 0)
    inn_map = CellType('}', 'inn_map', (99, 122, 80), False, 0)
    inn_map = CellType('}', 'inn_map', (99, 122, 80), False, 0)
    rock = CellType('r', 'rock', (94, 37, 37), False, 0)
    boulder = CellType('B', 'boulder', (172, 92, 113), False, 0)
    entrance = CellType('E', 'entrance', (227, 25, 77), True, 0)
    fruit_tree = CellType('F', 'fruit_tree', (192, 255, 81), False, 0)
    none = CellType('?', 'none', (0, 0, 0), False, 0)


class Cell(object):
    def __init__(self, x, y, typ: CellType):
        self.x = x
        self.y = y
        self.typ: CellType = typ
        self.goes_to = None  # can be a tuple (Map, x, y)

    def walkable(self) -> bool:
        return self.typ.walkable


class Occurrence(object):
    """
    Each map (Ma) has an occurrence.
    An occurrence gives for the map the probability for each word to appear
    """
    def __init__(self, ma, words: Words):
        self.ma = ma
        self.candidates = []
        self.rates = []
        file_path = f"{os.path.dirname(os.path.realpath(__file__))}/occurrences/{ma.filename}.occurrence"
        try:
            file = open(file_path, "r")
        except FileNotFoundError:
            # print(f"Could not find file {file_path}")
            return
        total_weight = 0
        for line in file:
            line = line.replace("\n", "")
            elements = line.split(" ")
            weight = int(elements[0])
            word = words.get_word(elements[1])
            total_weight += weight
            self.candidates.append(word)
            self.rates.append(weight)
        self.rates = [rate / total_weight for rate in self.rates]


class Ma(object):
    def __init__(self, filename, words, cell_types, mas):
        self.filename = filename
        self.mas: Mas = mas
        self.ma = []
        x, y = (0, 0)
        file = open(f"{os.path.dirname(os.path.realpath(__file__))}/map_text_files/{filename}", "r")
        for i, line in enumerate(file):
            y += 1
            x = 0
            new_line = []
            for j, character in enumerate(line):
                x += 1
                t = cell_types.none
                cell_type_names = [a for a in dir(CellTypes) if not a.startswith('__')]
                for cell_type_name in cell_type_names:
                    cell_type = getattr(CellTypes, cell_type_name)
                    if character == cell_type.letter:
                        t = cell_type
                new_line.append(Cell(x=j, y=i, typ=t))
            self.ma.append(new_line)
        self.width = x
        self.height = y
        self.occ = Occurrence(self, words)
        self.npcs: List[Npc] = []

    def draw(self, al):
        offset_x = -al.ui.cell_size * (al.learner.x - 7)
        offset_y = -al.ui.cell_size * (al.learner.y - 4)

        if (not al.learner.can_move()) and al.learner.movement:
            al.learner.movement.update()
            movement_offset_x, movement_offset_y = al.learner.movement.get_offset()
            offset_x += movement_offset_x * al.ui.cell_size
            offset_y += movement_offset_y * al.ui.cell_size

        for line in self.ma:
            for cell in line:
                x = cell.x * al.ui.cell_size + offset_x
                y = cell.y * al.ui.cell_size + offset_y
                if al.ui.can_draw_cell(x, y):
                    color = cell.typ.color
                    if cell.typ.name in al.ui.sprites:
                        al.ui.screen.blit(al.ui.sprites[cell.typ.name], [x, y])
                    else:
                        pygame.draw.rect(
                            al.ui.screen,
                            color,
                            pygame.Rect(x, y, al.ui.cell_size, al.ui.cell_size)
                        )

    def get_cell_at(self, x, y) -> Cell:
        return self.ma[y][x]

    def add_npc(self, npc):
        self.npcs.append(npc)

    def response_to_movement(self, learner, x, y):
        cell = self.get_cell_at(x, y)

        # 1 - Test for map change
        if cell.goes_to is not None:
            self.mas.current_map = cell.goes_to[0]
            learner.ma = cell.goes_to[0]
            learner.x = cell.goes_to[1]
            learner.y = cell.goes_to[2]
            return

        # 2 - Test for word encounter
        if learner.free_steps <= 0:
            rate = cell.typ.encounter_rate
            rand = random.uniform(0, 1)
            if rand < rate:
                if len(self.occ.candidates) > 0:
                    chosen_word = random.choices(population=self.occ.candidates,
                                                 weights=self.occ.rates,
                                                 k=1)[0]
                    pick_a_test_for_word(self.mas.al, chosen_word)
                    learner.free_steps = learner.max_free_steps
                else:
                    print(f"ERROR: You didn't specify the encounter rate for {self.filename}")


class Mas(object):
    def __init__(self, words, cell_types):
        self.al: 'All' = None
        self.house1 = Ma(filename="house1", words=words, cell_types=cell_types, mas=self)
        self.house2 = Ma(filename="house2", words=words, cell_types=cell_types, mas=self)
        self.house3 = Ma(filename="house3", words=words, cell_types=cell_types, mas=self)
        self.house4 = Ma(filename="house4", words=words, cell_types=cell_types, mas=self)
        self.house5 = Ma(filename="house5", words=words, cell_types=cell_types, mas=self)
        self.lab = Ma(filename="lab", words=words, cell_types=cell_types, mas=self)

        self.inn1 = Ma(filename="inn1", words=words, cell_types=cell_types, mas=self)
        self.inn2 = Ma(filename="inn2", words=words, cell_types=cell_types, mas=self)
        self.inn3 = Ma(filename="inn3", words=words, cell_types=cell_types, mas=self)
        self.inn4 = Ma(filename="inn4", words=words, cell_types=cell_types, mas=self)
        self.inn5 = Ma(filename="inn5", words=words, cell_types=cell_types, mas=self)
        self.chaiyaphum = Ma(filename="chaiyaphum", words=words, cell_types=cell_types, mas=self)
        self.chumphae = Ma(filename="chumphae", words=words, cell_types=cell_types, mas=self)
        self.chumphae_khonkaen = Ma(filename="chumphae_khonkaen", words=words, cell_types=cell_types, mas=self)

        self.chumphae_khonkaen_house_1 = Ma(filename="chumphae_khonkaen_house_1", words=words, cell_types=cell_types, mas=self)
        self.chumphae_khonkaen_house_2 = Ma(filename="chumphae_khonkaen_house_2", words=words, cell_types=cell_types, mas=self)
        self.chumphae_khonkaen_house_3 = Ma(filename="chumphae_khonkaen_house_3", words=words, cell_types=cell_types, mas=self)
        self.chumphae_khonkaen_house_4 = Ma(filename="chumphae_khonkaen_house_4", words=words, cell_types=cell_types, mas=self)

        self.chumphae_school = Ma(filename="chumphae_school", words=words, cell_types=cell_types, mas=self)
        self.chumphae_house1 = Ma(filename="chumphae_house1", words=words, cell_types=cell_types, mas=self)
        self.chumphae_house2 = Ma(filename="chumphae_house2", words=words, cell_types=cell_types, mas=self)
        self.chumphae_house3 = Ma(filename="chumphae_house3", words=words, cell_types=cell_types, mas=self)
        self.non_muang_house_1 = Ma(filename="non_muang_house_1", words=words, cell_types=cell_types, mas=self)
        self.chumphae_lomsak_house1 = Ma(filename="chumphae_lomsak_house1", words=words, cell_types=cell_types, mas=self)
        self.chumphae_lomsak_house2 = Ma(filename="chumphae_lomsak_house2", words=words, cell_types=cell_types, mas=self)
        self.chumphae_lomsak_house3 = Ma(filename="chumphae_lomsak_house3", words=words, cell_types=cell_types, mas=self)

        self.lomsak = Ma(filename="lomsak", words=words, cell_types=cell_types, mas=self)
        self.lomsak_house_1 = Ma(filename="lomsak_house_1", words=words, cell_types=cell_types, mas=self)
        self.lomsak_house_2 = Ma(filename="lomsak_house_2", words=words, cell_types=cell_types, mas=self)
        self.lomsak_school = Ma(filename="lomsak_school", words=words, cell_types=cell_types, mas=self)
        self.lomsak_gym = Ma(filename="lomsak_gym", words=words, cell_types=cell_types, mas=self)

        self.phetchabun = Ma(filename="phetchabun", words=words, cell_types=cell_types, mas=self)

        self.current_map: Ma = self.chaiyaphum

    def get_map_from_name(self, name):
        return getattr(self, name)

    def form_links(self):
        """
        In this function we define the 'links' (for example, a door leading to the
        inside of a house, i.e. to another map)
        """
        # chaiyaphum - chumphae
        self.chaiyaphum.get_cell_at(42, 14).goes_to = (self.chumphae, 123, 80)
        self.chaiyaphum.get_cell_at(43, 14).goes_to = (self.chumphae, 124, 80)
        self.chumphae.get_cell_at(123, 81).goes_to = (self.chaiyaphum, 42, 15)
        self.chumphae.get_cell_at(124, 81).goes_to = (self.chaiyaphum, 43, 15)
        # chaiyaphum
        self.chaiyaphum.get_cell_at(28, 91).goes_to = (self.house1, 5, 12)
        self.house1.get_cell_at(5, 13).goes_to = (self.chaiyaphum, 28, 92)

        self.chaiyaphum.get_cell_at(20, 89).goes_to = (self.house2, 5, 12)
        self.house2.get_cell_at(5, 13).goes_to = (self.chaiyaphum, 20, 90)
        self.chaiyaphum.get_cell_at(20, 86).goes_to = (self.house2, 5, 6)
        self.house2.get_cell_at(5, 5).goes_to = (self.chaiyaphum, 20, 85)
        self.chaiyaphum.get_cell_at(27, 99).goes_to = (self.lab, 5, 12)
        self.lab.get_cell_at(5, 13).goes_to = (self.chaiyaphum, 27, 100)

        self.chaiyaphum.get_cell_at(19, 97).goes_to = (self.house3, 5, 12)
        self.house3.get_cell_at(5, 13).goes_to = (self.chaiyaphum, 19, 98)
        self.chaiyaphum.get_cell_at(30, 39).goes_to = (self.house4, 5, 12)
        self.house4.get_cell_at(5, 13).goes_to = (self.chaiyaphum, 30, 40)
        self.chaiyaphum.get_cell_at(53, 10).goes_to = (self.house5, 5, 12)
        self.house5.get_cell_at(5, 13).goes_to = (self.chaiyaphum, 53, 11)
        # chumphae
        self.chumphae.get_cell_at(126, 74).goes_to = (self.inn1, 4, 7)
        self.inn1.get_cell_at(4, 8).goes_to = (self.chumphae, 126, 75)
        self.chumphae_school.get_cell_at(13, 25).goes_to = (self.chumphae, 123, 61)
        self.chumphae.get_cell_at(123, 60).goes_to = (self.chumphae_school, 13, 24)
        self.chumphae_house2.get_cell_at(5, 13).goes_to = (self.chumphae, 117, 64)
        self.chumphae.get_cell_at(117, 63).goes_to = (self.chumphae_house2, 5, 12)
        self.chumphae_house1.get_cell_at(5, 13).goes_to = (self.chumphae, 127, 62)
        self.chumphae.get_cell_at(127, 61).goes_to = (self.chumphae_house1, 5, 12)
        self.chumphae_house3.get_cell_at(7, 13).goes_to = (self.chumphae, 118, 74)
        self.chumphae.get_cell_at(118, 73).goes_to = (self.chumphae_house3, 7, 12)

        self.non_muang_house_1.get_cell_at(7, 13).goes_to = (self.chumphae, 113, 76)
        self.chumphae.get_cell_at(113, 75).goes_to = (self.non_muang_house_1, 7, 12)
        # chumphae_khonkaen
        self.chumphae_khonkaen.get_cell_at(12, 78).goes_to = (self.chumphae, 137, 66)
        self.chumphae_khonkaen.get_cell_at(12, 79).goes_to = (self.chumphae, 137, 67)
        self.chumphae.get_cell_at(138, 66).goes_to = (self.chumphae_khonkaen, 13, 78)
        self.chumphae.get_cell_at(138, 67).goes_to = (self.chumphae_khonkaen, 13, 79)
        self.chumphae_khonkaen.get_cell_at(18, 76).goes_to = (self.chumphae_khonkaen_house_1, 5, 12)
        self.chumphae_khonkaen_house_1.get_cell_at(5, 13).goes_to = (self.chumphae_khonkaen, 18, 77)
        self.chumphae_khonkaen.get_cell_at(29, 71).goes_to = (self.chumphae_khonkaen_house_2, 5, 12)
        self.chumphae_khonkaen_house_2.get_cell_at(5, 13).goes_to = (self.chumphae_khonkaen, 29, 72)
        self.chumphae_khonkaen.get_cell_at(34, 83).goes_to = (self.chumphae_khonkaen_house_3, 5, 12)
        self.chumphae_khonkaen_house_3.get_cell_at(5, 13).goes_to = (self.chumphae_khonkaen, 34, 84)
        self.chumphae_khonkaen.get_cell_at(43, 69).goes_to = (self.chumphae_khonkaen_house_4, 7, 12)
        self.chumphae_khonkaen_house_4.get_cell_at(7, 13).goes_to = (self.chumphae_khonkaen, 43, 70)
        # chumphae_lomsak
        self.chumphae.get_cell_at(104, 42).goes_to = (self.chumphae_lomsak_house1, 5, 12)
        self.chumphae_lomsak_house1.get_cell_at(5, 13).goes_to = (self.chumphae, 104, 43)
        self.chumphae.get_cell_at(87, 36).goes_to = (self.chumphae_lomsak_house2, 5, 12)
        self.chumphae_lomsak_house2.get_cell_at(5, 13).goes_to = (self.chumphae, 87, 37)
        self.chumphae.get_cell_at(36, 32).goes_to = (self.chumphae_lomsak_house3, 5, 12)
        self.chumphae_lomsak_house3.get_cell_at(5, 13).goes_to = (self.chumphae, 36, 33)
        # lomsak
        self.chumphae.get_cell_at(13, 19).goes_to = (self.lomsak, 36, 39)
        self.chumphae.get_cell_at(13, 20).goes_to = (self.lomsak, 36, 40)
        self.lomsak.get_cell_at(37, 39).goes_to = (self.chumphae, 14, 19)
        self.lomsak.get_cell_at(37, 40).goes_to = (self.chumphae, 14, 20)
        self.lomsak.get_cell_at(29, 32).goes_to = (self.inn2, 4, 7)
        self.inn2.get_cell_at(4, 8).goes_to = (self.lomsak, 29, 33)
        self.lomsak.get_cell_at(19, 36).goes_to = (self.lomsak_house_1, 5, 12)
        self.lomsak_house_1.get_cell_at(5, 13).goes_to = (self.lomsak, 19, 37)
        self.lomsak.get_cell_at(7, 24).goes_to = (self.lomsak_house_2, 5, 12)
        self.lomsak_house_2.get_cell_at(5, 13).goes_to = (self.lomsak, 7, 25)
        self.lomsak.get_cell_at(28, 24).goes_to = (self.lomsak_school, 13, 24)
        self.lomsak_school.get_cell_at(13, 25).goes_to = (self.lomsak, 28, 25)
        self.lomsak.get_cell_at(31, 23).goes_to = (self.lomsak_school, 19, 16)
        self.lomsak_school.get_cell_at(20, 16).goes_to = (self.lomsak, 32, 23)
        self.lomsak.get_cell_at(16, 24).goes_to = (self.lomsak_gym, 13, 24)
        self.lomsak_gym.get_cell_at(13, 25).goes_to = (self.lomsak, 16, 25)

        self.phetchabun.get_cell_at(49, 8).goes_to = (self.lomsak, 12, 37)
        self.lomsak.get_cell_at(12, 38).goes_to = (self.phetchabun, 49, 9)
        self.phetchabun.get_cell_at(50, 8).goes_to = (self.lomsak, 13, 37)
        self.lomsak.get_cell_at(13, 38).goes_to = (self.phetchabun, 50, 9)


