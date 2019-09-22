import os
import random
from typing import List

import pygame

from derive_from_mothermap import mothermap
from direction import Direction
from lexicon.items import Word
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
    grass = CellType('草', 'grass', (100, 200, 100), True, 0.05)
    tree = CellType('树', 'tree', (85, 107, 47), False, 0)
    ground = CellType('土', 'ground', (176, 246, 176), True, 0)
    tall_grass = CellType('稂', 'tall_grass', (0, 128, 0), True, 0.1)
    path = CellType('道', 'path', (200, 200, 200), True, 0)
    road = CellType('路', 'road', (154, 154, 154), True, 0)
    wall = CellType('壁', 'wall', (22, 22, 22), False, 0)
    sign = CellType('標', 'sign', (71, 71, 71), False, 0)
    water = CellType('水', 'water', (57, 62, 255), False, 0.05)
    cave_water = CellType('湿', 'cave_water', (24, 24, 58), False, 0.05)
    decoration = CellType('飾', 'decoration', (123, 9, 9), False, 0)
    flower = CellType('花', 'flower', (231, 148, 193), True, 0)
    flower_2 = CellType('李', 'flower_2', (231, 148, 194), True, 0)
    nenuphar = CellType('华', 'nenuphar', (189, 176, 246), True, 0)
    door = CellType('门', 'door', (255, 0, 204), True, 0)
    inn_floor = CellType('床', 'inn_floor', (117, 199, 242), True, 0)
    inn_sign = CellType('館', 'inn_sign', (255, 152, 234), False, 0)
    inn_map = CellType('図', 'inn_map', (99, 122, 80), False, 0)
    temple_floor = CellType('寺', 'temple_floor', (183, 183, 183), True, 0)

    # Cave
    cave_floor = CellType('穴', 'cave_floor', (159, 122, 120), True, 0.05)  # should be 0.05
    boulder_2 = CellType('岩', 'boulder_2', (53, 14, 14), False, 0)
    rock = CellType('石', 'rock', (94, 37, 37), False, 0)
    rocky_ground = CellType('嶝', 'rocky_path', (210, 185, 184), True, 0.05)  # should be 0.05
    boulder = CellType('砾', 'boulder', (172, 92, 113), False, 0)
    entrance = CellType('入', 'entrance', (227, 25, 77), True, 0)
    cave_0010 = CellType('┏', 'cave_0010', (63, 222, 141), False, 0)
    cave_0110 = CellType('┣', 'cave_0110', (63, 201, 222), False, 0)
    cave_0100 = CellType('┗', 'cave_0100', (63, 104, 222), False, 0)
    cave_1100 = CellType('┻', 'cave_1100', (149, 63, 222), False, 0)
    cave_1000 = CellType('┛', 'cave_1000', (209, 63, 222), False, 0)
    cave_1001 = CellType('┫', 'cave_1001', (222, 63, 104), False, 0)
    cave_0001 = CellType('┓', 'cave_0001', (222, 100, 63), False, 0)
    cave_0011 = CellType('┳', 'cave_0011', (183, 222, 63), True, 0)
    cave_1110 = CellType('┐', 'cave_1110', (80, 95, 138), False, 0)
    cave_1101 = CellType('┌', 'cave_1101', (122, 95, 124), False, 0)
    cave_entrance_down = CellType('u', 'cave_entrance_down', (25, 227, 58), True, 0)
    cave_stairs_1100 = CellType('║', 'cave_stairs_1100', (138, 0, 255), True, 0)
    cave_stairs_0110 = CellType('═', 'cave_stairs_0110', (77, 178, 193), True, 0)
    cave_stairs_1001 = CellType('─', 'cave_stairs_1001', (177, 85, 109), True, 0)
    cave_stairs_0011 = CellType('│', 'cave_stairs_0011', (161, 186, 87), True, 0.05)
    cave_0010_over_edge = CellType('┲', 'cave_0010_over_edge', (121, 222, 103), False, 0)
    cave_0001_over_edge = CellType('┱', 'cave_0001_over_edge', (203, 159, 63), False, 0)

    fruit_tree = CellType('果', 'fruit_tree', (192, 255, 81), False, 0)
    waterfall = CellType('滝', 'waterfall', (57, 150, 255), True, 0.1)
    bridge_hor = CellType('橋', 'bridge_hor', (163, 165, 255), True, 0)
    bridge_ver = CellType('圯', 'bridge_ver', (163, 164, 255), True, 0)
    fence = CellType('垣', 'fence', (102, 102, 102), False, 0)
    arena_sign = CellType('競', 'arena_sign', (255, 192, 0), False, 0)
    school_sign = CellType('学', 'school_sign', (103, 229, 216), False, 0)
    shop_sign = CellType('買', 'shop_sign', (65, 71, 193), False, 0)
    field = CellType('畑', 'field', (225, 232, 168), True, 0.04)
    sand = CellType('砂', 'sand', (255, 218, 105), True, 0)
    buddha_statue = CellType('仏', 'buddha_statue', (255, 215, 54), False, 0)
    none = CellType('無', 'none', (0, 0, 0), False, 0)


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
    def __init__(self, ma):
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
            # TODO Alexis do it so that it fetches word by id rather than by thai to avoid confusions
            word = Word.get_by_split_form(elements[1])
            total_weight += weight
            self.candidates.append(word)
            self.rates.append(weight)
        self.rates = [rate / total_weight for rate in self.rates]


class Ma(object):
    def __init__(self, filename, cell_types, mas, x_shift=-1, y_shift=-1):
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
        self.occ = Occurrence(self)
        self.npcs: List[Npc] = []
        self.x_shift = x_shift
        self.y_shift = y_shift

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
        try:
            return self.ma[y][x]
        except:
            print('The map', self.filename)
            print(f' only has dimensions ({len(self.ma)}, {len(self.ma[0])})')
            print(f' and the cell requested is ({x}, {y})')

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
            try:
                learner.direction = cell.goes_to[3]
            except IndexError:
                pass
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
    def __init__(self, cell_types):
        self.al: 'All' = None
        self.house_learner_f2 = Ma(filename="house_learner_f2", cell_types=cell_types, mas=self)
        self.house_learner_f1 = Ma(filename="house_learner_f1", cell_types=cell_types, mas=self)
        self.house_rival_f1 = Ma(filename="house_rival_f1", cell_types=cell_types, mas=self)
        self.house_rival_f2 = Ma(filename="house_rival_f2", cell_types=cell_types, mas=self)
        self.chaiyaphum_house_1 = Ma(filename="chaiyaphum_house_1", cell_types=cell_types, mas=self)
        self.chaiyaphum_house_2 = Ma(filename="chaiyaphum_house_2", cell_types=cell_types, mas=self)
        self.lover_house = Ma(filename="lover_house", cell_types=cell_types, mas=self)
        self.house4 = Ma(filename="house4", cell_types=cell_types, mas=self)
        self.house5 = Ma(filename="house5", cell_types=cell_types, mas=self)

        self.inn1 = Ma(filename="inn1", cell_types=cell_types, mas=self)
        self.inn2 = Ma(filename="inn2", cell_types=cell_types, mas=self)
        self.inn3 = Ma(filename="inn3", cell_types=cell_types, mas=self)
        self.inn4 = Ma(filename="inn4", cell_types=cell_types, mas=self)
        self.inn5 = Ma(filename="inn5", cell_types=cell_types, mas=self)
        self.inn_khonkaen = Ma(filename="inn_khonkaen", cell_types=cell_types, mas=self)
        self.inn_buengsamphan = Ma(filename="inn_buengsamphan", cell_types=cell_types, mas=self)

        self.chaiyaphum = Ma(filename="chaiyaphum", cell_types=cell_types, mas=self, x_shift=780, y_shift=629)
        self.chumphae = Ma(filename="chumphae", cell_types=cell_types, mas=self, x_shift=699, y_shift=563)
        self.chumphae_khonkaen = Ma(filename="chumphae_khonkaen", cell_types=cell_types, mas=self, x_shift=824, y_shift=551)

        self.chumphae_khonkaen_house_1 = Ma(filename="chumphae_khonkaen_house_1", cell_types=cell_types, mas=self)
        self.chumphae_khonkaen_house_2 = Ma(filename="chumphae_khonkaen_house_2", cell_types=cell_types, mas=self)
        self.chumphae_khonkaen_house_3 = Ma(filename="chumphae_khonkaen_house_3", cell_types=cell_types, mas=self)
        self.chumphae_khonkaen_house_4 = Ma(filename="chumphae_khonkaen_house_4", cell_types=cell_types, mas=self)

        self.chumphae_school = Ma(filename="chumphae_school", cell_types=cell_types, mas=self)
        self.chumphae_house1 = Ma(filename="chumphae_house1", cell_types=cell_types, mas=self)
        self.chumphae_house2 = Ma(filename="chumphae_house2", cell_types=cell_types, mas=self)
        self.chumphae_house3 = Ma(filename="chumphae_house3", cell_types=cell_types, mas=self)
        self.non_muang_house_1 = Ma(filename="non_muang_house_1", cell_types=cell_types, mas=self)
        self.chumphae_lomsak_house1 = Ma(filename="chumphae_lomsak_house1", cell_types=cell_types, mas=self)
        self.chumphae_lomsak_house2 = Ma(filename="chumphae_lomsak_house2", cell_types=cell_types, mas=self)
        self.chumphae_lomsak_house3 = Ma(filename="chumphae_lomsak_house3", cell_types=cell_types, mas=self)

        self.lomsak = Ma(filename="lomsak", cell_types=cell_types, mas=self, x_shift=676, y_shift=543)
        self.lomsak_house_1 = Ma(filename="lomsak_house_1", cell_types=cell_types, mas=self)
        self.lomsak_house_2 = Ma(filename="lomsak_house_2", cell_types=cell_types, mas=self)
        self.lomsak_house_3 = Ma(filename="lomsak_house_3", cell_types=cell_types, mas=self)
        self.lomsak_house_4 = Ma(filename="lomsak_house_4", cell_types=cell_types, mas=self)
        self.lomsak_school = Ma(filename="lomsak_school", cell_types=cell_types, mas=self)
        self.lomsak_gym = Ma(filename="lomsak_gym", cell_types=cell_types, mas=self)
        self.lomsak_temple = Ma(filename="lomsak_temple", cell_types=cell_types, mas=self)

        self.question_cave = Ma(filename="question_cave", cell_types=cell_types, mas=self)
        self.cat_cave = Ma(filename="cat_cave", cell_types=cell_types, mas=self)
        self.bat_cave = Ma(filename="bat_cave", cell_types=cell_types, mas=self)
        self.cat_cove = Ma(filename="cat_cove", cell_types=cell_types, mas=self, x_shift=710, y_shift=616)
        self.cat_cove_house = Ma(filename="cat_cove_house", cell_types=cell_types, mas=self)

        self.phetchabun = Ma(filename="phetchabun", cell_types=cell_types, mas=self, x_shift=639, y_shift=572)
        self.banyaeng = Ma(filename="banyaeng", cell_types=cell_types, mas=self, x_shift=599, y_shift=578)
        self.labyrinth = Ma(filename="labyrinth", cell_types=cell_types, mas=self, x_shift=586, y_shift=545)
        self.phitsalunok = Ma(filename="phitsalunok", cell_types=cell_types, mas=self, x_shift=530, y_shift=545)
        self.lomsak_labyrinth = Ma(filename="lomsak_labyrinth", cell_types=cell_types, mas=self, x_shift=620, y_shift=548)
        self.phetchabun_mountain_house_1 = Ma(filename="phetchabun_mountain_house_1", cell_types=cell_types, mas=self)
        self.phetchabun_mountain_house_2 = Ma(filename="phetchabun_mountain_house_2", cell_types=cell_types, mas=self)
        self.phetchabun_farm = Ma(filename="phetchabun_farm", cell_types=cell_types, mas=self)

        self.phetchabun_buengsamphan = Ma(filename="phetchabun_buengsamphan", cell_types=cell_types, mas=self, x_shift=647, y_shift=640)
        self.buengsamphan = Ma(filename="buengsamphan", cell_types=cell_types, mas=self, x_shift=650, y_shift=704)
        self.taphan_hin = Ma(filename="taphan_hin", cell_types=cell_types, mas=self, x_shift=537, y_shift=597)
        self.buengsamphan_chumsaeng = Ma(filename="buengsamphan_chumsaeng", cell_types=cell_types, mas=self, x_shift=569, y_shift=664)
        self.thapkhlo = Ma(filename="thapkhlo", cell_types=cell_types, mas=self, x_shift=578, y_shift=648)
        self.nakhon_sawan = Ma(filename="nakhon_sawan", cell_types=cell_types, mas=self, x_shift=502, y_shift=703)
        self.chumsaeng = Ma(filename="chumsaeng", cell_types=cell_types, mas=self, x_shift=537, y_shift=660)
        self.thapkhlo_phitsalunok = Ma(filename="thapkhlo_phitsalunok", cell_types=cell_types, mas=self, x_shift=572, y_shift=596)
        self.khonkaen = Ma(filename="khonkaen", cell_types=cell_types, mas=self, x_shift=897, y_shift=611)
        self.buengsamphan_chaiyaphum = Ma(filename="buengsamphan_chaiyaphum", cell_types=cell_types, mas=self, x_shift=697, y_shift=689)
        self.buengsamphan_mountain = Ma(filename="buengsamphan_mountain", cell_types=cell_types, mas=self, x_shift=719, y_shift=689)

        self.kasetsombum = Ma(filename="kasetsombum", cell_types=cell_types, mas=self, x_shift=761, y_shift=635)

        self.buengsamphan_cave = Ma(filename="buengsamphan_cave", cell_types=cell_types, mas=self)
        self.inn_banyaeng = Ma(filename="inn_banyaeng", cell_types=cell_types, mas=self)
        self.inn_nakhon_sawan = Ma(filename="inn_nakhon_sawan", cell_types=cell_types, mas=self)
        self.inn_chumsaeng = Ma(filename="inn_chumsaeng", cell_types=cell_types, mas=self)
        self.inn_phetchabun = Ma(filename="inn_phetchabun", cell_types=cell_types, mas=self)
        self.inn_phitsalunok = Ma(filename="inn_phitsalunok", cell_types=cell_types, mas=self)
        self.inn_phitsalunok_2 = Ma(filename="inn_phitsalunok_2", cell_types=cell_types, mas=self)
        self.nakhon_sawan_aquarium = Ma(filename="nakhon_sawan_aquarium", cell_types=cell_types, mas=self)
        self.banyaeng_cave = Ma(filename="banyaeng_cave", cell_types=cell_types, mas=self)
        self.phetchabun_school = Ma(filename="phetchabun_school", cell_types=cell_types, mas=self)
        self.phetchabun_cave = Ma(filename="phetchabun_cave", cell_types=cell_types, mas=self)
        self.phetchabun_house_1 = Ma(filename="phetchabun_house_1", cell_types=cell_types, mas=self)
        self.phetchabun_house_2 = Ma(filename="phetchabun_house_2", cell_types=cell_types, mas=self)
        self.phitsalunok_underground = Ma(filename="phitsalunok_underground", cell_types=cell_types, mas=self)
        self.lomsak_labyrinth_house_1 = Ma(filename="lomsak_labyrinth_house_1", cell_types=cell_types, mas=self)
        self.lomsak_labyrinth_house_2 = Ma(filename="lomsak_labyrinth_house_2", cell_types=cell_types, mas=self)
        self.phetchabun_temple = Ma(filename="phetchabun_temple", cell_types=cell_types, mas=self)
        self.phetchabun_gym = Ma(filename="phetchabun_gym", cell_types=cell_types, mas=self)
        self.banyaeng_house_1 = Ma(filename="banyaeng_house_1", cell_types=cell_types, mas=self)
        self.banyaeng_house_2 = Ma(filename="banyaeng_house_2", cell_types=cell_types, mas=self)
        self.banyaeng_school = Ma(filename="banyaeng_school", cell_types=cell_types, mas=self)
        self.banyaeng_temple = Ma(filename="banyaeng_temple", cell_types=cell_types, mas=self)
        self.banyaeng_house_3 = Ma(filename="banyaeng_house_3", cell_types=cell_types, mas=self)
        self.phetchabun_shop = Ma(filename="phetchabun_shop", cell_types=cell_types, mas=self)
        self.lomsak_labyrinth_shop = Ma(filename="lomsak_labyrinth_shop", cell_types=cell_types, mas=self)
        self.chumphae_kasetsombum_cave = Ma(filename="chumphae_kasetsombum_cave", cell_types=cell_types, mas=self)
        self.labyrinth_shop = Ma(filename="labyrinth_shop", cell_types=cell_types, mas=self)
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
        self.chaiyaphum.get_cell_at(28, 101).goes_to = (self.house_learner_f1, 5, 12)
        self.house_learner_f1.get_cell_at(5, 13).goes_to = (self.chaiyaphum, 28, 102)
        self.house_learner_f1.get_cell_at(8, 7).goes_to = (self.house_learner_f2, 8, 8, Direction.DOWN)
        self.house_learner_f2.get_cell_at(8, 7).goes_to = (self.house_learner_f1, 8, 8, Direction.DOWN)
        self.chaiyaphum.get_cell_at(20, 89).goes_to = (self.lover_house, 5, 12)
        self.lover_house.get_cell_at(5, 13).goes_to = (self.chaiyaphum, 20, 90)
        self.chaiyaphum.get_cell_at(20, 86).goes_to = (self.lover_house, 8, 8)
        self.lover_house.get_cell_at(8, 7).goes_to = (self.chaiyaphum, 20, 85)
        self.chaiyaphum.get_cell_at(32, 91).goes_to = (self.house_rival_f1, 5, 12)
        self.house_rival_f1.get_cell_at(5, 13).goes_to = (self.chaiyaphum, 32, 92)
        self.house_rival_f1.get_cell_at(8, 7).goes_to = (self.house_rival_f2, 8, 8, Direction.DOWN)
        self.house_rival_f2.get_cell_at(8, 7).goes_to = (self.house_rival_f1, 8, 8, Direction.DOWN)
        self.chaiyaphum.get_cell_at(26, 87).goes_to = (self.chaiyaphum_house_1, 5, 12)
        self.chaiyaphum_house_1.get_cell_at(5, 13).goes_to = (self.chaiyaphum, 26, 88)
        self.chaiyaphum.get_cell_at(34, 97).goes_to = (self.chaiyaphum_house_2, 4, 12)
        self.chaiyaphum_house_2.get_cell_at(4, 13).goes_to = (self.chaiyaphum, 34, 98)
        self.chaiyaphum_house_2.get_cell_at(10, 13).goes_to = (self.chaiyaphum, 34, 98)

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

        self.chumphae.get_cell_at(97, 77).goes_to = (self.chumphae_kasetsombum_cave, 19, 4)
        self.chumphae_kasetsombum_cave.get_cell_at(19, 5).goes_to = (self.chumphae, 97, 78)

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
        self.chumphae.get_cell_at(13, 19).goes_to = (self.lomsak, 36 + 6, 39)
        self.chumphae.get_cell_at(13, 20).goes_to = (self.lomsak, 36 + 6, 40)
        self.lomsak.get_cell_at(37 + 6, 39).goes_to = (self.chumphae, 14, 19)
        self.lomsak.get_cell_at(37 + 6, 40).goes_to = (self.chumphae, 14, 20)
        self.lomsak.get_cell_at(29 + 6, 32).goes_to = (self.inn2, 4, 7)
        self.inn2.get_cell_at(4, 8).goes_to = (self.lomsak, 29 + 6, 33)
        self.lomsak.get_cell_at(19 + 6, 36).goes_to = (self.lomsak_house_1, 5, 12)
        self.lomsak_house_1.get_cell_at(5, 13).goes_to = (self.lomsak, 19 + 6, 37)
        self.lomsak.get_cell_at(13, 24).goes_to = (self.lomsak_house_2, 5, 12)
        self.lomsak_house_2.get_cell_at(5, 13).goes_to = (self.lomsak, 13, 25)
        self.lomsak.get_cell_at(28 + 6, 24).goes_to = (self.lomsak_school, 13, 24)
        self.lomsak_school.get_cell_at(13, 25).goes_to = (self.lomsak, 28 + 6, 25)
        self.lomsak.get_cell_at(31 + 6, 23).goes_to = (self.lomsak_school, 19, 16)
        self.lomsak_school.get_cell_at(20, 16).goes_to = (self.lomsak, 37, 22)
        self.lomsak.get_cell_at(16 + 6, 24).goes_to = (self.lomsak_gym, 13, 24)
        self.lomsak_gym.get_cell_at(13, 25).goes_to = (self.lomsak, 16 + 6, 25)
        self.lomsak.get_cell_at(21 + 6, 12).goes_to = (self.lomsak_temple, 13, 24)
        self.lomsak_temple.get_cell_at(13, 25).goes_to = (self.lomsak, 21 + 6, 13)

        self.cat_cave.get_cell_at(13, 3).goes_to = (self.cat_cove, 19, 29)
        self.cat_cove.get_cell_at(19, 30).goes_to = (self.cat_cave, 13, 4)

        self.cat_cove.get_cell_at(11, 6).goes_to = (self.cat_cove_house, 5, 12)
        self.cat_cove_house.get_cell_at(5, 13).goes_to = (self.cat_cove, 11, 7)

        self.phetchabun.get_cell_at(49, 8).goes_to = (self.lomsak, 12 + 6, 37)
        self.lomsak.get_cell_at(12 + 6, 38).goes_to = (self.phetchabun, 49, 9)
        self.phetchabun.get_cell_at(50, 8).goes_to = (self.lomsak, 13 + 6, 37)
        self.lomsak.get_cell_at(13 + 6, 38).goes_to = (self.phetchabun, 50, 9)

        # Banyaeng forest
        self.banyaeng.get_cell_at(8, 10).goes_to = (self.labyrinth, 21, 43)
        self.banyaeng.get_cell_at(9, 10).goes_to = (self.labyrinth, 22, 43)
        self.labyrinth.get_cell_at(21, 44).goes_to = (self.banyaeng, 8, 11)
        self.labyrinth.get_cell_at(22, 44).goes_to = (self.banyaeng, 9, 11)

        self.labyrinth.get_cell_at(7, 16).goes_to = (self.phitsalunok, 63, 16)
        self.labyrinth.get_cell_at(8, 16).goes_to = (self.phitsalunok, 64, 16)
        self.phitsalunok.get_cell_at(63, 15).goes_to = (self.labyrinth, 7, 15)
        self.phitsalunok.get_cell_at(64, 15).goes_to = (self.labyrinth, 8, 15)

        self.labyrinth.get_cell_at(42, 9).goes_to = (self.lomsak_labyrinth, 8, 6)
        self.labyrinth.get_cell_at(42, 10).goes_to = (self.lomsak_labyrinth, 8, 7)
        self.lomsak_labyrinth.get_cell_at(7, 6).goes_to = (self.labyrinth, 41, 9)
        self.lomsak_labyrinth.get_cell_at(7, 7).goes_to = (self.labyrinth, 41, 10)

        self.lomsak.get_cell_at(677 - mothermap.minimaps['lomsak'].x, 567 - mothermap.minimaps['lomsak'].y).goes_to = (self.lomsak_labyrinth, 677 - mothermap.minimaps['lomsak_labyrinth'].x, 567 - mothermap.minimaps['lomsak_labyrinth'].y)
        self.lomsak.get_cell_at(677 - mothermap.minimaps['lomsak'].x, 568 - mothermap.minimaps['lomsak'].y).goes_to = (self.lomsak_labyrinth, 677 - mothermap.minimaps['lomsak_labyrinth'].x, 568 - mothermap.minimaps['lomsak_labyrinth'].y)
        self.lomsak_labyrinth.get_cell_at(677 + 1 - mothermap.minimaps['lomsak_labyrinth'].x, 567 - mothermap.minimaps['lomsak_labyrinth'].y).goes_to = (self.lomsak, 677 + 1 - mothermap.minimaps['lomsak'].x, 567 - mothermap.minimaps['lomsak'].y)
        self.lomsak_labyrinth.get_cell_at(677 + 1 - mothermap.minimaps['lomsak_labyrinth'].x, 568 - mothermap.minimaps['lomsak_labyrinth'].y).goes_to = (self.lomsak, 677 + 1 - mothermap.minimaps['lomsak'].x, 568 - mothermap.minimaps['lomsak'].y)

        # Phetchabun
        self.phetchabun.get_cell_at(8, 57).goes_to = (self.banyaeng, 48, 51)
        self.phetchabun.get_cell_at(8, 58).goes_to = (self.banyaeng, 48, 52)
        self.banyaeng.get_cell_at(49, 51).goes_to = (self.phetchabun, 9, 57)
        self.banyaeng.get_cell_at(49, 52).goes_to = (self.phetchabun, 9, 58)
        self.phetchabun.get_cell_at(17, 17).goes_to = (self.question_cave, 24, 26)
        self.question_cave.get_cell_at(24, 27).goes_to = (self.phetchabun, 17, 18)
        self.phetchabun.get_cell_at(11, 27).goes_to = (self.question_cave, 18, 39)
        self.question_cave.get_cell_at(18, 40).goes_to = (self.phetchabun, 11, 28)

        self.phetchabun.get_cell_at(24, 35).goes_to = (self.question_cave, 31, 47)
        self.question_cave.get_cell_at(31, 48).goes_to = (self.phetchabun, 24, 36)
        self.phetchabun.get_cell_at(10, 19).goes_to = (self.question_cave, 18, 10)
        self.question_cave.get_cell_at(18, 11).goes_to = (self.phetchabun, 10, 20)

        self.phetchabun.get_cell_at(36, 54).goes_to = (self.cat_cave, 6, 12)
        self.cat_cave.get_cell_at(6, 13).goes_to = (self.phetchabun, 36, 55)
        self.phetchabun.get_cell_at(26, 60).goes_to = (self.phetchabun_house_1, 5, 12)
        self.phetchabun_house_1.get_cell_at(5, 13).goes_to = (self.phetchabun, 26, 61)
        self.phetchabun.get_cell_at(21, 7).goes_to = (self.lomsak_labyrinth, 40, 31)
        self.phetchabun.get_cell_at(22, 7).goes_to = (self.lomsak_labyrinth, 41, 31)
        self.lomsak_labyrinth.get_cell_at(40, 32).goes_to = (self.phetchabun, 21, 8)
        self.lomsak_labyrinth.get_cell_at(41, 32).goes_to = (self.phetchabun, 22, 8)
        self.phetchabun.get_cell_at(42, 18).goes_to = (self.lomsak_house_3, 13, 24)
        self.lomsak_house_3.get_cell_at(13, 25).goes_to = (self.phetchabun, 42, 19)
        self.phetchabun.get_cell_at(59, 13).goes_to = (self.lomsak_house_4, 13, 24)
        self.lomsak_house_4.get_cell_at(13, 25).goes_to = (self.phetchabun, 59, 14)
        self.phetchabun.get_cell_at(24, 10).goes_to = (self.phetchabun_mountain_house_1, 7, 12)
        self.phetchabun_mountain_house_1.get_cell_at(7, 13).goes_to = (self.phetchabun, 24, 11)
        self.phetchabun.get_cell_at(22, 24).goes_to = (self.phetchabun_mountain_house_2, 7, 12)
        self.phetchabun_mountain_house_2.get_cell_at(7, 13).goes_to = (self.phetchabun, 22, 25)
        self.phetchabun.get_cell_at(46, 62).goes_to = (self.phetchabun_farm, 10, 24)
        self.phetchabun_farm.get_cell_at(10, 25).goes_to = (self.phetchabun, 46, 63)
        self.phetchabun_farm.get_cell_at(16, 25).goes_to = (self.phetchabun, 49, 63)
        self.phetchabun.get_cell_at(49, 62).goes_to = (self.phetchabun_farm, 16, 24)
        self.phetchabun.get_cell_at(677 - mothermap.minimaps['phetchabun'].x, 645 - mothermap.minimaps['phetchabun'].y).goes_to = (self.phetchabun_buengsamphan, 677 - mothermap.minimaps['phetchabun_buengsamphan'].x, 645 - mothermap.minimaps['phetchabun_buengsamphan'].y)
        self.phetchabun.get_cell_at(678 - mothermap.minimaps['phetchabun'].x, 645 - mothermap.minimaps['phetchabun'].y).goes_to = (self.phetchabun_buengsamphan, 678 - mothermap.minimaps['phetchabun_buengsamphan'].x, 645 - mothermap.minimaps['phetchabun_buengsamphan'].y)
        self.phetchabun_buengsamphan.get_cell_at(677 - mothermap.minimaps['phetchabun_buengsamphan'].x, 643 - mothermap.minimaps['phetchabun_buengsamphan'].y).goes_to = (self.phetchabun, 677 - mothermap.minimaps['phetchabun'].x, 643 - mothermap.minimaps['phetchabun'].y)
        self.phetchabun_buengsamphan.get_cell_at(678 - mothermap.minimaps['phetchabun_buengsamphan'].x, 643 - mothermap.minimaps['phetchabun_buengsamphan'].y).goes_to = (self.phetchabun, 678 - mothermap.minimaps['phetchabun'].x, 643 - mothermap.minimaps['phetchabun'].y)
        self.phetchabun_buengsamphan.get_cell_at(21, 67).goes_to = (self.buengsamphan, 668 - mothermap.minimaps['buengsamphan'].x, 706 - mothermap.minimaps['buengsamphan'].y)
        self.phetchabun_buengsamphan.get_cell_at(21, 68).goes_to = (self.buengsamphan, 668 - mothermap.minimaps['buengsamphan'].x, 707 - mothermap.minimaps['buengsamphan'].y)
        self.buengsamphan.get_cell_at(19, 5).goes_to = (self.phetchabun_buengsamphan, 669 - mothermap.minimaps['phetchabun_buengsamphan'].x, 707 - mothermap.minimaps['phetchabun_buengsamphan'].y)
        self.buengsamphan.get_cell_at(19, 4).goes_to = (self.phetchabun_buengsamphan, 669 - mothermap.minimaps['phetchabun_buengsamphan'].x, 706 - mothermap.minimaps['phetchabun_buengsamphan'].y)
        self.phetchabun.get_cell_at(13, 52).goes_to = (self.phetchabun_school, 13, 24)
        self.phetchabun_school.get_cell_at(13, 25).goes_to = (self.phetchabun, 13, 53)
        self.phetchabun.get_cell_at(26, 52).goes_to = (self.inn_phetchabun, 4, 7)
        self.inn_phetchabun.get_cell_at(4, 8).goes_to = (self.phetchabun, 26, 53)
        self.phetchabun.get_cell_at(66, 22).goes_to = (self.phetchabun_cave, 4, 1)
        self.phetchabun_cave.get_cell_at(4, 2).goes_to = (self.phetchabun, 66, 23)
        self.phetchabun.get_cell_at(66, 34).goes_to = (self.phetchabun_cave, 4, 13)
        self.phetchabun_cave.get_cell_at(4, 14).goes_to = (self.phetchabun, 66, 35)
        self.phetchabun.get_cell_at(33, 62).goes_to = (self.phetchabun_temple, 13, 24)
        self.phetchabun_temple.get_cell_at(13, 25).goes_to = (self.phetchabun, 33, 63)
        self.phetchabun.get_cell_at(15, 62).goes_to = (self.phetchabun_gym, 12, 24)
        self.phetchabun_gym.get_cell_at(12, 25).goes_to = (self.phetchabun, 15, 63)
        self.phetchabun.get_cell_at(21, 50).goes_to = (self.phetchabun_house_2, 5, 12)
        self.phetchabun_house_2.get_cell_at(5, 13).goes_to = (self.phetchabun, 21, 51)
        self.phetchabun.get_cell_at(21, 56).goes_to = (self.phetchabun_shop, 5, 12)
        self.phetchabun_shop.get_cell_at(5, 13).goes_to = (self.phetchabun, 21, 57)

        self.buengsamphan.get_cell_at(7, 11).goes_to = (self.buengsamphan_chumsaeng, 657 - mothermap.minimaps['buengsamphan_chumsaeng'].x, 713 - mothermap.minimaps['buengsamphan_chumsaeng'].y)
        self.buengsamphan.get_cell_at(7, 10).goes_to = (self.buengsamphan_chumsaeng, 657 - mothermap.minimaps['buengsamphan_chumsaeng'].x, 712 - mothermap.minimaps['buengsamphan_chumsaeng'].y)
        self.buengsamphan_chumsaeng.get_cell_at(89, 48).goes_to = (self.buengsamphan, 658 - mothermap.minimaps['buengsamphan'].x, 712 - mothermap.minimaps['buengsamphan'].y)
        self.buengsamphan_chumsaeng.get_cell_at(89, 49).goes_to = (self.buengsamphan, 658 - mothermap.minimaps['buengsamphan'].x, 713 - mothermap.minimaps['buengsamphan'].y)

        self.buengsamphan_chumsaeng.get_cell_at(32, 6).goes_to = (self.thapkhlo, 601 - mothermap.minimaps['thapkhlo'].x, 670 - mothermap.minimaps['thapkhlo'].y)
        self.buengsamphan_chumsaeng.get_cell_at(33, 6).goes_to = (self.thapkhlo, 602 - mothermap.minimaps['thapkhlo'].x, 670 - mothermap.minimaps['thapkhlo'].y)
        self.thapkhlo.get_cell_at(23, 23).goes_to = (self.buengsamphan_chumsaeng, 601 - mothermap.minimaps['buengsamphan_chumsaeng'].x, 671 - mothermap.minimaps['buengsamphan_chumsaeng'].y)
        self.thapkhlo.get_cell_at(24, 23).goes_to = (self.buengsamphan_chumsaeng, 602 - mothermap.minimaps['buengsamphan_chumsaeng'].x, 671 - mothermap.minimaps['buengsamphan_chumsaeng'].y)

        self.thapkhlo.get_cell_at(7, 16).goes_to = (self.chumsaeng, 585 - mothermap.minimaps['chumsaeng'].x, 664 - mothermap.minimaps['chumsaeng'].y)
        self.thapkhlo.get_cell_at(7, 17).goes_to = (self.chumsaeng, 585 - mothermap.minimaps['chumsaeng'].x, 665 - mothermap.minimaps['chumsaeng'].y)
        self.chumsaeng.get_cell_at(49, 4).goes_to = (self.thapkhlo, 586 - mothermap.minimaps['thapkhlo'].x, 664 - mothermap.minimaps['thapkhlo'].y)
        self.chumsaeng.get_cell_at(49, 5).goes_to = (self.thapkhlo, 586 - mothermap.minimaps['thapkhlo'].x, 665 - mothermap.minimaps['thapkhlo'].y)

        self.taphan_hin.get_cell_at(23, 6).goes_to = (self.phitsalunok, 560 - mothermap.minimaps['phitsalunok'].x, 600 - mothermap.minimaps['phitsalunok'].y)
        self.taphan_hin.get_cell_at(24, 6).goes_to = (self.phitsalunok, 561 - mothermap.minimaps['phitsalunok'].x, 600 - mothermap.minimaps['phitsalunok'].y)
        self.phitsalunok.get_cell_at(30, 56).goes_to = (self.taphan_hin, 560 - mothermap.minimaps['taphan_hin'].x, 601 - mothermap.minimaps['taphan_hin'].y)
        self.phitsalunok.get_cell_at(31, 56).goes_to = (self.taphan_hin, 561 - mothermap.minimaps['taphan_hin'].x, 601 - mothermap.minimaps['taphan_hin'].y)

        self.phitsalunok.get_cell_at(21, 68).goes_to = (self.taphan_hin, 560 - mothermap.minimaps['taphan_hin'].x, 601 - mothermap.minimaps['taphan_hin'].y)
        self.phitsalunok.get_cell_at(21, 68).goes_to = (self.taphan_hin, 561 - mothermap.minimaps['taphan_hin'].x, 601 - mothermap.minimaps['taphan_hin'].y)

        self.thapkhlo.get_cell_at(597 - mothermap.minimaps['thapkhlo'].x, 652 - mothermap.minimaps['thapkhlo'].y).goes_to = (self.thapkhlo_phitsalunok, 597 - mothermap.minimaps['thapkhlo_phitsalunok'].x, 652 - mothermap.minimaps['thapkhlo_phitsalunok'].y)
        self.thapkhlo.get_cell_at(598 - mothermap.minimaps['thapkhlo'].x, 652 - mothermap.minimaps['thapkhlo'].y).goes_to = (self.thapkhlo_phitsalunok, 598 - mothermap.minimaps['thapkhlo_phitsalunok'].x, 652 - mothermap.minimaps['thapkhlo_phitsalunok'].y)
        self.thapkhlo_phitsalunok.get_cell_at(597 - mothermap.minimaps['thapkhlo_phitsalunok'].x, 653 - mothermap.minimaps['thapkhlo_phitsalunok'].y).goes_to = (self.thapkhlo, 597 - mothermap.minimaps['thapkhlo'].x, 653 - mothermap.minimaps['thapkhlo'].y)
        self.thapkhlo_phitsalunok.get_cell_at(598 - mothermap.minimaps['thapkhlo_phitsalunok'].x, 653 - mothermap.minimaps['thapkhlo_phitsalunok'].y).goes_to = (self.thapkhlo, 598 - mothermap.minimaps['thapkhlo'].x, 653 - mothermap.minimaps['thapkhlo'].y)

        self.thapkhlo_phitsalunok.get_cell_at(579 - mothermap.minimaps['thapkhlo_phitsalunok'].x, 602 - mothermap.minimaps['thapkhlo_phitsalunok'].y).goes_to = (self.phitsalunok, 579 - mothermap.minimaps['phitsalunok'].x, 602 - mothermap.minimaps['phitsalunok'].y)
        self.thapkhlo_phitsalunok.get_cell_at(579 - mothermap.minimaps['thapkhlo_phitsalunok'].x, 603 - mothermap.minimaps['thapkhlo_phitsalunok'].y).goes_to = (self.phitsalunok, 579 - mothermap.minimaps['phitsalunok'].x, 603 - mothermap.minimaps['phitsalunok'].y)
        self.phitsalunok.get_cell_at(580 - mothermap.minimaps['phitsalunok'].x, 602 - mothermap.minimaps['phitsalunok'].y).goes_to = (self.thapkhlo_phitsalunok, 580 - mothermap.minimaps['thapkhlo_phitsalunok'].x, 602 - mothermap.minimaps['thapkhlo_phitsalunok'].y)
        self.phitsalunok.get_cell_at(580 - mothermap.minimaps['phitsalunok'].x, 603 - mothermap.minimaps['phitsalunok'].y).goes_to = (self.thapkhlo_phitsalunok, 580 - mothermap.minimaps['thapkhlo_phitsalunok'].x, 603 - mothermap.minimaps['thapkhlo_phitsalunok'].y)

        self.taphan_hin.get_cell_at(22, 73).goes_to = (self.chumsaeng, 559 - mothermap.minimaps['chumsaeng'].x, 667 - mothermap.minimaps['chumsaeng'].y)
        self.taphan_hin.get_cell_at(23, 73).goes_to = (self.chumsaeng, 560 - mothermap.minimaps['chumsaeng'].x, 667 - mothermap.minimaps['chumsaeng'].y)
        self.chumsaeng.get_cell_at(22, 6).goes_to = (self.taphan_hin, 559 - mothermap.minimaps['taphan_hin'].x, 666 - mothermap.minimaps['taphan_hin'].y)
        self.chumsaeng.get_cell_at(23, 6).goes_to = (self.taphan_hin, 560 - mothermap.minimaps['taphan_hin'].x, 666 - mothermap.minimaps['taphan_hin'].y)

        # Khonkaen
        self.chumphae_khonkaen.get_cell_at(82, 80).goes_to = (self.khonkaen, 906 - mothermap.minimaps['khonkaen'].x, 631 - mothermap.minimaps['khonkaen'].y)
        self.chumphae_khonkaen.get_cell_at(82, 81).goes_to = (self.khonkaen, 906 - mothermap.minimaps['khonkaen'].x, 632 - mothermap.minimaps['khonkaen'].y)
        self.khonkaen.get_cell_at(8, 20).goes_to = (self.chumphae_khonkaen, 905 - mothermap.minimaps['chumphae_khonkaen'].x, 631 - mothermap.minimaps['chumphae_khonkaen'].y)
        self.khonkaen.get_cell_at(8, 21).goes_to = (self.chumphae_khonkaen, 905 - mothermap.minimaps['chumphae_khonkaen'].x, 632 - mothermap.minimaps['chumphae_khonkaen'].y)
        self.inn_khonkaen.get_cell_at(4, 8).goes_to = (self.khonkaen, 916 - mothermap.minimaps['khonkaen'].x, 631 - mothermap.minimaps['khonkaen'].y)
        self.khonkaen.get_cell_at(916 - mothermap.minimaps['khonkaen'].x, 630 - mothermap.minimaps['khonkaen'].y).goes_to = (self.inn_khonkaen, 4, 7)

        # Buengsamphan
        self.chaiyaphum.get_cell_at(11, 92).goes_to = (self.buengsamphan_chaiyaphum, 791 - mothermap.minimaps['buengsamphan_chaiyaphum'].x, 721 - mothermap.minimaps['buengsamphan_chaiyaphum'].y)
        self.chaiyaphum.get_cell_at(11, 93).goes_to = (self.buengsamphan_chaiyaphum, 791 - mothermap.minimaps['buengsamphan_chaiyaphum'].x, 722 - mothermap.minimaps['buengsamphan_chaiyaphum'].y)
        self.buengsamphan_chaiyaphum.get_cell_at(73, 32).goes_to = (self.chaiyaphum, 792 - mothermap.minimaps['chaiyaphum'].x, 721 - mothermap.minimaps['chaiyaphum'].y)
        self.buengsamphan_chaiyaphum.get_cell_at(73, 33).goes_to = (self.chaiyaphum, 792 - mothermap.minimaps['chaiyaphum'].x, 722 - mothermap.minimaps['chaiyaphum'].y)
        self.buengsamphan_chaiyaphum.get_cell_at(7, 32).goes_to = (self.buengsamphan, 726 - mothermap.minimaps['buengsamphan'].x, 721 - mothermap.minimaps['buengsamphan'].y)
        self.buengsamphan_chaiyaphum.get_cell_at(7, 33).goes_to = (self.buengsamphan, 726 - mothermap.minimaps['buengsamphan'].x, 722 - mothermap.minimaps['buengsamphan'].y)
        self.buengsamphan.get_cell_at(20, 22).goes_to = (self.inn_buengsamphan, 4, 7)
        self.inn_buengsamphan.get_cell_at(4, 8).goes_to = (self.buengsamphan, 670 - mothermap.minimaps['buengsamphan'].x, 725 - mothermap.minimaps['buengsamphan'].y)
        self.buengsamphan.get_cell_at(61, 6).goes_to = (self.buengsamphan_cave, 10, 21)
        self.buengsamphan_cave.get_cell_at(10, 22).goes_to = (self.buengsamphan, 61, 7)
        self.buengsamphan_cave.get_cell_at(17, 17).goes_to = (self.buengsamphan_mountain, 718 - mothermap.minimaps['buengsamphan_mountain'].x, 704 - mothermap.minimaps['buengsamphan_mountain'].y)
        self.buengsamphan_cave.get_cell_at(3, 10).goes_to = (self.buengsamphan_mountain, 704 - mothermap.minimaps['buengsamphan_mountain'].x, 697 - mothermap.minimaps['buengsamphan_mountain'].y)
        self.buengsamphan_cave.get_cell_at(35, 10).goes_to = (self.buengsamphan_mountain, 736 - mothermap.minimaps['buengsamphan_mountain'].x, 697 - mothermap.minimaps['buengsamphan_mountain'].y)
        self.buengsamphan_mountain.get_cell_at(7, 7).goes_to = (self.buengsamphan_cave, 3, 9)
        self.buengsamphan_mountain.get_cell_at(21, 14).goes_to = (self.buengsamphan_cave, 17, 16)
        self.buengsamphan_mountain.get_cell_at(39, 7).goes_to = (self.buengsamphan_cave, 35, 9)

        # Banyaeng
        self.banyaeng.get_cell_at(45, 6).goes_to = (self.bat_cave, 9, 15)
        self.bat_cave.get_cell_at(9, 16).goes_to = (self.banyaeng, 45, 7)
        self.banyaeng.get_cell_at(36, 12).goes_to = (self.inn_banyaeng, 4, 7)
        self.inn_banyaeng.get_cell_at(4, 8).goes_to = (self.banyaeng, 36, 13)

        self.chumsaeng.get_cell_at(553 - mothermap.minimaps['chumsaeng'].x, 714 - mothermap.minimaps['chumsaeng'].y).goes_to = (self.nakhon_sawan, 553 - mothermap.minimaps['nakhon_sawan'].x, 714 - mothermap.minimaps['nakhon_sawan'].y)
        self.nakhon_sawan.get_cell_at(553 - mothermap.minimaps['nakhon_sawan'].x, 713 - mothermap.minimaps['nakhon_sawan'].y).goes_to = (self.chumsaeng, 553 - mothermap.minimaps['chumsaeng'].x, 713 - mothermap.minimaps['chumsaeng'].y)

        self.chumsaeng.get_cell_at(30, 27).goes_to = (self.inn_chumsaeng, 4, 7)
        self.inn_chumsaeng.get_cell_at(4, 8).goes_to = (self.chumsaeng, 30, 28)

        # Phitsalunok
        self.phitsalunok.get_cell_at(38, 17).goes_to = (self.inn_phitsalunok, 4, 7)
        self.inn_phitsalunok.get_cell_at(4, 8).goes_to = (self.phitsalunok, 38, 18)
        self.phitsalunok.get_cell_at(26, 28).goes_to = (self.phitsalunok_underground, 6, 4)
        self.phitsalunok.get_cell_at(40, 42).goes_to = (self.phitsalunok_underground, 20, 18)
        self.phitsalunok.get_cell_at(24, 40).goes_to = (self.phitsalunok_underground, 4, 16)
        self.phitsalunok_underground.get_cell_at(20, 19).goes_to = (self.phitsalunok, 40, 43)
        self.phitsalunok_underground.get_cell_at(6, 5).goes_to = (self.phitsalunok, 26, 29)
        self.phitsalunok_underground.get_cell_at(4, 17).goes_to = (self.phitsalunok, 24, 41)

        self.nakhon_sawan.get_cell_at(57, 19).goes_to = (self.nakhon_sawan_aquarium, 13, 24)
        self.nakhon_sawan_aquarium.get_cell_at(13, 25).goes_to = (self.nakhon_sawan, 57, 20)
        self.nakhon_sawan.get_cell_at(32, 20).goes_to = (self.inn_nakhon_sawan, 4, 7)
        self.inn_nakhon_sawan.get_cell_at(4, 8).goes_to = (self.nakhon_sawan, 32, 21)
        self.banyaeng.get_cell_at(37, 55).goes_to = (self.banyaeng_cave, 16, 10)
        self.banyaeng.get_cell_at(27, 51).goes_to = (self.banyaeng_cave, 6, 6)
        self.banyaeng_cave.get_cell_at(6, 7).goes_to = (self.banyaeng, 27, 52)
        self.banyaeng_cave.get_cell_at(16, 11).goes_to = (self.banyaeng, 37, 56)

        # Lomsak Labyrinth
        self.lomsak_labyrinth.get_cell_at(48, 12).goes_to = (self.lomsak_labyrinth_house_1, 5, 12)
        self.lomsak_labyrinth_house_1.get_cell_at(5, 13).goes_to = (self.lomsak_labyrinth, 48, 13)
        self.lomsak_labyrinth.get_cell_at(49, 11).goes_to = (self.lomsak_labyrinth_house_1, 8, 3)
        self.lomsak_labyrinth_house_1.get_cell_at(8, 2).goes_to = (self.lomsak_labyrinth, 49, 10)
        self.lomsak_labyrinth.get_cell_at(33, 12).goes_to = (self.lomsak_labyrinth_house_2, 13, 24)
        self.lomsak_labyrinth_house_2.get_cell_at(13, 25).goes_to = (self.lomsak_labyrinth, 33, 13)
        self.lomsak_labyrinth.get_cell_at(25, 16).goes_to = (self.lomsak_labyrinth_shop, 5, 12)
        self.lomsak_labyrinth_shop.get_cell_at(5, 13).goes_to = (self.lomsak_labyrinth, 25, 17)

        # Labyrinth
        self.labyrinth.get_cell_at(21, 21).goes_to = (self.labyrinth_shop, 5, 12)
        self.labyrinth_shop.get_cell_at(5, 13).goes_to = (self.labyrinth, 21, 22)

        # Banyaeng
        self.banyaeng.get_cell_at(17, 49).goes_to = (self.banyaeng_house_1, 5, 12)
        self.banyaeng_house_1.get_cell_at(5, 13).goes_to = (self.banyaeng, 17, 50)
        self.banyaeng.get_cell_at(20, 55).goes_to = (self.banyaeng_house_2, 5, 12)
        self.banyaeng_house_2.get_cell_at(5, 13).goes_to = (self.banyaeng, 20, 56)
        self.banyaeng.get_cell_at(41, 12).goes_to = (self.banyaeng_school, 13, 24)
        self.banyaeng_school.get_cell_at(13, 25).goes_to = (self.banyaeng, 41, 13)
        self.banyaeng.get_cell_at(37, 6).goes_to = (self.banyaeng_temple, 13, 24)
        self.banyaeng_temple.get_cell_at(13, 25).goes_to = (self.banyaeng, 37, 7)
        self.banyaeng.get_cell_at(39, 5).goes_to = (self.banyaeng_temple, 17, 21)
        self.banyaeng_temple.get_cell_at(18, 21).goes_to = (self.banyaeng, 40, 5)
        self.banyaeng.get_cell_at(31, 9).goes_to = (self.banyaeng_house_3, 5, 12)
        self.banyaeng_house_3.get_cell_at(5, 13).goes_to = (self.banyaeng, 31, 10)

        self.chumphae_kasetsombum_cave.get_cell_at(18, 14).goes_to = (self.kasetsombum, 34, 15)
        self.kasetsombum.get_cell_at(34, 14).goes_to = (self.chumphae_kasetsombum_cave, 18, 13)




