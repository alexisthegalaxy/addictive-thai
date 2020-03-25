from datetime import datetime
import os
import random
from dataclasses import dataclass
from typing import List, Optional

import pygame

from derive_from_mothermap import mothermap
from direction import Direction
# from event import execute_event
from lexicon.items import Word, Letter
from lexicon.test_services import pick_a_test_for_word, pick_a_test_for_letter
from npc.npc import Npc

PATH_COLOR = (176, 246, 176)
GRASS_COLOR = (100, 200, 100)
TREE_COLOR = (85, 107, 47)
WALL_COLOR = (50, 50, 50)
ROOF_COLOR = (123, 9, 9)
WATER_COLOR = (57, 62, 255)
MOUNTAIN_PATH_COLOR = (210, 185, 184)
MOUNTAIN_WALL_COLOR = (108, 75, 75)
VOID_COLOR = (0, 0, 0)


class CellType(object):
    def __init__(self, letter, name, color, walkable, encounter_rate, postcolor):
        self.letter = letter
        self.name = name
        self.color = color
        self.walkable = walkable
        self.encounter_rate = encounter_rate
        self.postcolor = (
            postcolor
        )  # the color used for transforming the map into the postmap


class CellTypes:
    grass = CellType("草", "_grass", (100, 200, 100), True, 0.05, GRASS_COLOR)
    hole_in_grass = CellType("坑", "hole_in_grass", (0, 50, 0), True, 0, GRASS_COLOR)
    tree = CellType("树", "tree", (85, 107, 47), False, 0, TREE_COLOR)
    ground = CellType("土", "ground", (176, 246, 176), True, 0, PATH_COLOR)
    tall_grass = CellType("稂", "_tall_grass", (0, 128, 0), True, 0.1, GRASS_COLOR)
    path = CellType("道", "path", (200, 200, 200), True, 0, PATH_COLOR)
    road = CellType("路", "road", (154, 154, 154), True, 0, PATH_COLOR)
    wall = CellType("壁", "wall", (22, 22, 22), False, 0, WALL_COLOR)
    sign = CellType("標", "sign", (71, 71, 71), False, 0, WALL_COLOR)
    water = CellType("水", "water", (57, 62, 255), False, 0.05, WATER_COLOR)
    cave_water = CellType("湿", "cave_water", (24, 24, 58), False, 0.05, WATER_COLOR)
    decoration = CellType("飾", "decoration", (123, 9, 9), False, 0, ROOF_COLOR)
    flower_4 = CellType("萓", "flower_4", (231, 148, 191), True, 0, PATH_COLOR)
    flower_3 = CellType("菫", "flower_3", (231, 148, 192), True, 0, PATH_COLOR)
    flower_1 = CellType("花", "_flower_1", (231, 148, 193), True, 0, PATH_COLOR)
    flower_2 = CellType("李", "_flower_2", (231, 148, 194), True, 0, PATH_COLOR)
    nenuphar = CellType("华", "nenuphar", (189, 176, 246), True, 0, WATER_COLOR)
    door = CellType("门", "door", (255, 0, 204), True, 0, WALL_COLOR)
    inn_floor = CellType("床", "inn_floor", (117, 199, 242), True, 0, PATH_COLOR)
    inn_sign = CellType("館", "inn_sign", (255, 152, 234), False, 0, WALL_COLOR)
    inn_map = CellType("図", "inn_map", (99, 122, 80), False, 0, WALL_COLOR)
    temple_floor = CellType("寺", "temple_floor", (183, 183, 183), True, 0, PATH_COLOR)
    field_spirit_house = CellType(
        "社", "field_spirit_house", (193, 200, 129), False, 0, PATH_COLOR
    )
    stairs_up = CellType("上", "stairs_up", (255, 192, 192), True, 0, PATH_COLOR)
    stairs_down = CellType("下", "stairs_down", (192, 255, 248), True, 0, PATH_COLOR)
    # Cave
    cave_floor = CellType(
        "穴", "cave_floor", (159, 122, 120), True, 0.05, MOUNTAIN_PATH_COLOR
    )
    cave_rock_pillar_1 = CellType(
        "鍾", "cave_rock_pillar_1", (54, 14, 14), False, 0, MOUNTAIN_WALL_COLOR
    )
    boulder_2 = CellType("岩", "boulder_2", (53, 14, 14), False, 0, MOUNTAIN_WALL_COLOR)
    rock = CellType("石", "rock", (94, 37, 37), False, 0, MOUNTAIN_WALL_COLOR)
    rocky_ground = CellType(
        "嶝", "rocky_path", (210, 185, 184), True, 0.05, MOUNTAIN_PATH_COLOR
    )
    boulder = CellType("砾", "boulder", (172, 92, 113), False, 0, MOUNTAIN_WALL_COLOR)
    entrance = CellType("入", "entrance", (227, 25, 77), True, 0, MOUNTAIN_PATH_COLOR)
    cave_0010 = CellType(
        "┏", "cave_0010", (63, 222, 141), False, 0, MOUNTAIN_WALL_COLOR
    )
    cave_0110 = CellType(
        "┣", "cave_0110", (63, 201, 222), False, 0, MOUNTAIN_WALL_COLOR
    )
    cave_0100 = CellType(
        "┗", "cave_0100", (63, 104, 222), False, 0, MOUNTAIN_WALL_COLOR
    )
    cave_1100 = CellType(
        "┻", "cave_1100", (149, 63, 222), False, 0, MOUNTAIN_WALL_COLOR
    )
    cave_1000 = CellType(
        "┛", "cave_1000", (209, 63, 222), False, 0, MOUNTAIN_WALL_COLOR
    )
    cave_1001 = CellType(
        "┫", "cave_1001", (222, 63, 104), False, 0, MOUNTAIN_WALL_COLOR
    )
    cave_0001 = CellType(
        "┓", "cave_0001", (222, 100, 63), False, 0, MOUNTAIN_WALL_COLOR
    )
    cave_0011 = CellType("┳", "cave_0011", (183, 222, 63), True, 0, MOUNTAIN_WALL_COLOR)
    cave_1110 = CellType("┐", "cave_1110", (80, 95, 138), False, 0, MOUNTAIN_WALL_COLOR)
    cave_1101 = CellType(
        "┌", "cave_1101", (122, 95, 124), False, 0, MOUNTAIN_WALL_COLOR
    )
    cave_entrance_down = CellType(
        "u", "cave_entrance_down", (25, 227, 58), True, 0, MOUNTAIN_PATH_COLOR
    )
    cave_stairs_1100 = CellType(
        "║", "cave_stairs_1100", (138, 0, 255), True, 0, MOUNTAIN_PATH_COLOR
    )
    cave_stairs_0110 = CellType(
        "═", "cave_stairs_0110", (77, 178, 193), True, 0, MOUNTAIN_PATH_COLOR
    )
    cave_stairs_1001 = CellType(
        "─", "cave_stairs_1001", (177, 85, 109), True, 0, MOUNTAIN_PATH_COLOR
    )
    cave_stairs_0011 = CellType(
        "│", "cave_stairs_0011", (161, 186, 87), True, 0.05, MOUNTAIN_PATH_COLOR
    )
    cave_0010_over_edge = CellType(
        "┲", "cave_0010_over_edge", (121, 222, 103), False, 0, MOUNTAIN_WALL_COLOR
    )
    cave_0001_over_edge = CellType(
        "┱", "cave_0001_over_edge", (203, 159, 63), False, 0, MOUNTAIN_WALL_COLOR
    )

    fruit_tree = CellType("果", "fruit_tree", (192, 255, 81), False, 0, TREE_COLOR)
    waterfall = CellType("滝", "_waterfall", (57, 150, 255), True, 0.1, WATER_COLOR)
    bridge_hor = CellType("橋", "bridge_hor", (163, 165, 255), True, 0, WATER_COLOR)
    bridge_ver = CellType("圯", "bridge_ver", (163, 164, 255), True, 0, WATER_COLOR)
    fence = CellType("垣", "fence", (102, 102, 102), False, 0, WALL_COLOR)
    arena_sign = CellType("競", "arena_sign", (255, 192, 0), False, 0, WALL_COLOR)
    school_sign = CellType("学", "school_sign", (103, 229, 216), False, 0, WALL_COLOR)
    palm_tree = CellType("椰", "palm_tree", (131, 148, 102), False, 0, TREE_COLOR)
    shop_sign = CellType("買", "shop_sign", (65, 71, 193), False, 0, WALL_COLOR)
    field = CellType("畑", "field", (225, 232, 168), True, 0.4, PATH_COLOR)
    sand = CellType("砂", "sand", (255, 218, 105), True, 0, PATH_COLOR)
    buddha_statue = CellType("仏", "buddha_statue", (255, 215, 54), False, 0, WALL_COLOR)
    none = CellType("無", "none", (0, 0, 0), False, 0, (0, 0, 0))


@dataclass
class Trigger:
    event: str
    npcs: Optional[List[str]]


class Cell(object):
    def __init__(self, x, y, typ: CellType):
        self.x = x
        self.y = y
        self.typ: CellType = typ
        self.goes_to = None  # can be a tuple (Map, x, y)
        self.trigger = None  # Can be a tuple ('event', None) or ('event')

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
            letter = " L " in line
            if letter:
                elements = line.split(" L ")
            else:
                elements = line.split(" ")
            weight = int(elements[0])
            # TODO Alexis do it so that it fetches word by id rather than by thai to avoid confusions
            if letter:
                letter = Letter.get_by_thai(elements[1])
                self.candidates.append(letter)
            else:
                word = Word.get_by_split_form(elements[1])
                self.candidates.append(word)
            total_weight += weight
            self.rates.append(weight)
        self.rates = [rate / total_weight for rate in self.rates]


def get_cell_type_dictionary():
    """
    Produce a dictionary, that given the letter, return the cell type
    """
    cell_type_names = [a for a in dir(CellTypes) if not a.startswith("__")]
    cells: List[CellType] = [getattr(CellTypes, name) for name in cell_type_names]
    return {cell.letter: cell for cell in cells}


def get_cell_type_dictionary_by_color():
    """
    Produce a dictionary, that given the letter, return the cell type
    """
    cell_type_names = [a for a in dir(CellTypes) if not a.startswith("__")]
    cells: List[CellType] = [getattr(CellTypes, name) for name in cell_type_names]
    return {cell.color: cell for cell in cells}


def _get_time_type():
    """
    Returns 1, 2, 3 or 4
    """
    now = datetime.now().microsecond
    if now < 250_000:
        return 1
    if now < 500_000:
        return 2
    if now < 750_000:
        return 3
    return 4


class Ma(object):
    def __init__(
        self, filename, mas, x_shift=-1, y_shift=-1, parent=None, trigger_tiles=None
    ):
        self.filename = filename
        self.mas: Mas = mas
        self.parent = parent
        self.ma = []
        x, y = (0, 0)
        file = open(
            f"{os.path.dirname(os.path.realpath(__file__))}/map_text_files/{filename}",
            "r",
        )
        cell_dictionary = get_cell_type_dictionary()
        for i, line in enumerate(file):
            y += 1
            x = 0
            new_line = []
            for j, character in enumerate(line):
                try:
                    cell_type = cell_dictionary[character]
                except:
                    cell_type = CellTypes.none
                new_line.append(Cell(x=j, y=i, typ=cell_type))
            self.ma.append(new_line)
        self.width = x
        self.height = y
        self.occ = Occurrence(self)
        self.npcs: List[Npc] = []
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.trigger_tiles = trigger_tiles or []

    def draw(self, al):
        learner_x = al.learner.x
        learner_y = al.learner.y
        offset_x = -al.ui.cell_size * (learner_x - 7)
        offset_y = -al.ui.cell_size * (learner_y - 4)

        if (not al.learner.can_move()) and al.learner.movement:
            al.learner.movement.update()
            movement_offset_x, movement_offset_y = al.learner.movement.get_offset()
            offset_x += movement_offset_x * al.ui.cell_size
            offset_y += movement_offset_y * al.ui.cell_size
        time_type = _get_time_type()
        for cell_y in range(learner_y - 5, learner_y + 6):
            for cell_x in range(learner_x - 8, learner_x + 9):
                cell = self.get_cell_at(cell_x, cell_y)
                x = cell.x * al.ui.cell_size + offset_x
                y = cell.y * al.ui.cell_size + offset_y
                if al.ui.can_draw_cell(x, y):
                    name = cell.typ.name
                    if name[0] == "_":
                        name = f"{name}_{time_type}"
                    if name in al.ui.sprites:
                        al.ui.screen.blit(al.ui.sprites[name], [x, y])
                    else:
                        pygame.draw.rect(
                            al.ui.screen,
                            cell.typ.color,
                            pygame.Rect(x, y, al.ui.cell_size, al.ui.cell_size),
                        )

    def get_cell_at(self, x, y) -> Cell:
        try:
            return self.ma[y][x]
        except:
            print("The map", self.filename)
            print(f" only has dimensions ({len(self.ma)}, {len(self.ma[0])})")
            print(f" and the cell requested is ({x}, {y})")

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

        # 2 - Test for Word or Letter encounter
        if learner.free_steps <= 0:
            rate = cell.typ.encounter_rate
            rand = random.uniform(0, 1)
            if rand < rate:
                if len(self.occ.candidates) > 0:
                    chosen_candidate = random.choices(
                        population=self.occ.candidates, weights=self.occ.rates, k=1
                    )[0]
                    if isinstance(chosen_candidate, Word):
                        pick_a_test_for_word(self.mas.al, chosen_candidate)
                    elif isinstance(chosen_candidate, Letter):
                        pick_a_test_for_letter(self.mas.al, chosen_candidate)
                    learner.free_steps = learner.max_free_steps
                else:
                    print(
                        f"ERROR: You didn't specify the encounter rate for {self.filename}"
                    )


class Mas(object):
    def __init__(self):
        # Main maps:
        # these maps are real overworld, not houses
        self.chaiyaphum = Ma(filename="chaiyaphum", mas=self, x_shift=780, y_shift=629)
        self.chumphae = Ma(filename="chumphae", mas=self, x_shift=699, y_shift=563)
        self.chumphae_khonkaen = Ma(
            filename="chumphae_khonkaen", mas=self, x_shift=824, y_shift=551
        )
        self.phetchabun_buengsamphan = Ma(
            filename="phetchabun_buengsamphan", mas=self, x_shift=647, y_shift=640
        )
        self.buengsamphan = Ma(
            filename="buengsamphan", mas=self, x_shift=650, y_shift=704
        )
        self.taphan_hin = Ma(filename="taphan_hin", mas=self, x_shift=537, y_shift=597)
        self.buengsamphan_chumsaeng = Ma(
            filename="buengsamphan_chumsaeng", mas=self, x_shift=569, y_shift=664
        )
        self.thapkhlo = Ma(filename="thapkhlo", mas=self, x_shift=578, y_shift=648)
        self.nakhon_sawan = Ma(
            filename="nakhon_sawan", mas=self, x_shift=502, y_shift=703
        )
        self.chumsaeng = Ma(filename="chumsaeng", mas=self, x_shift=537, y_shift=660)
        self.thapkhlo_phitsanulok = Ma(
            filename="thapkhlo_phitsanulok", mas=self, x_shift=572, y_shift=596
        )
        self.khonkaen = Ma(filename="khonkaen", mas=self, x_shift=897, y_shift=611)
        self.buengsamphan_chaiyaphum = Ma(
            filename="buengsamphan_chaiyaphum", mas=self, x_shift=697, y_shift=689
        )
        self.buengsamphan_mountain = Ma(
            filename="buengsamphan_mountain", mas=self, x_shift=719, y_shift=689
        )
        self.lomsak = Ma(filename="lomsak", mas=self, x_shift=676, y_shift=543)
        self.cat_cove = Ma(filename="cat_cove", mas=self, x_shift=710, y_shift=616)
        self.cat_cove_hidden_house = Ma(
            filename="cat_cove_hidden_house", mas=self, x_shift=720, y_shift=611
        )
        self.cat_cove_hidden_shop = Ma(
            filename="cat_cove_hidden_shop", mas=self,
        )
        self.kasetsombum = Ma(
            filename="kasetsombum", mas=self, x_shift=761, y_shift=635
        )
        self.phetchabun = Ma(filename="phetchabun", mas=self, x_shift=639, y_shift=572)
        self.banyaeng = Ma(filename="banyaeng", mas=self, x_shift=599, y_shift=578)
        self.labyrinth = Ma(filename="labyrinth", mas=self, x_shift=586, y_shift=545)
        self.phitsanulok = Ma(
            filename="phitsanulok", mas=self, x_shift=530, y_shift=545
        )
        self.lomsak_labyrinth = Ma(
            filename="lomsak_labyrinth", mas=self, x_shift=620, y_shift=548
        )
        self.phitsanulok_sukhothai = Ma(
            filename="phitsanulok_sukhothai", mas=self, x_shift=493, y_shift=540
        )
        self.sukhothai = Ma(filename="sukhothai", mas=self, x_shift=468, y_shift=513)
        self.old_sukhothai = Ma(
            filename="old_sukhothai", mas=self, x_shift=429, y_shift=514
        )
        self.bua_yai = Ma(filename="bua_yai", mas=self, x_shift=795, y_shift=699)
        self.phon = Ma(filename="phon", mas=self, x_shift=865, y_shift=644)
        self.chaiyaphum_chatturat = Ma(
            filename="chaiyaphum_chatturat", mas=self, x_shift=750, y_shift=715
        )
        self.chatturat_sikhiu = Ma(
            filename="chatturat_sikhiu", mas=self, x_shift=716, y_shift=790
        )
        self.sikhiu = Ma(
            filename="sikhiu", mas=self, x_shift=704, y_shift=837
        )
        self.chatturat = Ma(filename="chatturat", mas=self, x_shift=704, y_shift=762)
        self.ko_kut = Ma(filename="ko_kut", mas=self, x_shift=806, y_shift=1303)
        self.ko_mak = Ma(filename="ko_mak", mas=self, x_shift=816, y_shift=1305)
        self.ko_klum = Ma(filename="ko_klum", mas=self, x_shift=811, y_shift=1297)
        self.ko_chang = Ma(filename="ko_chang", mas=self, x_shift=802, y_shift=1263)

        # inns
        self.inn1 = Ma(filename="inn1", mas=self, parent=self.chumphae)
        self.inn2 = Ma(filename="inn2", mas=self, parent=self.lomsak)
        self.inn_khonkaen = Ma(filename="inn_khonkaen", mas=self, parent=self.khonkaen)
        self.inn_buengsamphan = Ma(
            filename="inn_buengsamphan", mas=self, parent=self.buengsamphan
        )
        self.inn_banyaeng = Ma(filename="inn_banyaeng", mas=self)
        self.inn_nakhon_sawan = Ma(filename="inn_nakhon_sawan", mas=self)
        self.inn_chumsaeng = Ma(filename="inn_chumsaeng", mas=self)
        self.inn_phetchabun = Ma(filename="inn_phetchabun", mas=self)
        self.inn_phitsanulok = Ma(filename="inn_phitsanulok", mas=self)
        self.inn_phitsanulok_2 = Ma(filename="inn_phitsanulok_2", mas=self)
        self.inn_bua_yai = Ma(filename="inn_bua_yai", mas=self)
        self.inn_chatturat = Ma(filename="inn_chatturat", mas=self)
        self.inn_ko_kut = Ma(filename="inn_ko_kut", mas=self)

        self.house_learner_f2 = Ma(
            filename="house_learner_f2", mas=self, parent=self.chaiyaphum
        )
        self.house_learner_f1 = Ma(
            filename="house_learner_f1", mas=self, parent=self.chaiyaphum
        )
        self.house_rival_f1 = Ma(
            filename="house_rival_f1", mas=self, parent=self.chaiyaphum
        )
        self.house_rival_f2 = Ma(
            filename="house_rival_f2", mas=self, parent=self.chaiyaphum
        )
        self.chaiyaphum_house_1 = Ma(
            filename="chaiyaphum_house_1", mas=self, parent=self.chaiyaphum
        )
        self.chaiyaphum_house_2 = Ma(
            filename="chaiyaphum_house_2", mas=self, parent=self.chaiyaphum
        )
        self.lover_house = Ma(filename="lover_house", mas=self, parent=self.chaiyaphum)
        self.house4 = Ma(filename="house4", mas=self, parent=self.chaiyaphum)
        self.house5 = Ma(filename="house5", mas=self, parent=self.chaiyaphum)

        self.chumphae_khonkaen_house_1 = Ma(
            filename="chumphae_khonkaen_house_1",
            mas=self,
            parent=self.chumphae_khonkaen,
        )
        self.chumphae_khonkaen_house_2 = Ma(
            filename="chumphae_khonkaen_house_2",
            mas=self,
            parent=self.chumphae_khonkaen,
        )
        self.chumphae_khonkaen_house_3 = Ma(
            filename="chumphae_khonkaen_house_3",
            mas=self,
            parent=self.chumphae_khonkaen,
        )
        self.chumphae_khonkaen_house_4 = Ma(
            filename="chumphae_khonkaen_house_4",
            mas=self,
            parent=self.chumphae_khonkaen,
        )

        self.chumphae_school = Ma(
            filename="chumphae_school", mas=self, parent=self.chumphae
        )
        self.chumphae_house1 = Ma(
            filename="chumphae_house1", mas=self, parent=self.chumphae
        )
        self.chumphae_house2 = Ma(
            filename="chumphae_house2", mas=self, parent=self.chumphae
        )
        self.chumphae_house3 = Ma(
            filename="chumphae_house3", mas=self, parent=self.chumphae
        )
        self.non_muang_house_1 = Ma(filename="non_muang_house_1", mas=self)
        self.chumphae_lomsak_house1 = Ma(
            filename="chumphae_lomsak_house1", mas=self, parent=self.chumphae
        )
        self.chumphae_lomsak_house2 = Ma(
            filename="chumphae_lomsak_house2", mas=self, parent=self.chumphae
        )
        self.chumphae_lomsak_house3 = Ma(
            filename="chumphae_lomsak_house3", mas=self, parent=self.chumphae
        )

        self.lomsak_house_1 = Ma(
            filename="lomsak_house_1", mas=self, parent=self.lomsak
        )
        self.lomsak_house_2 = Ma(
            filename="lomsak_house_2", mas=self, parent=self.lomsak
        )
        self.lomsak_house_3 = Ma(
            filename="lomsak_house_3", mas=self, parent=self.lomsak
        )
        self.lomsak_house_4 = Ma(
            filename="lomsak_house_4", mas=self, parent=self.lomsak
        )
        self.lomsak_school = Ma(filename="lomsak_school", mas=self, parent=self.lomsak)
        self.lomsak_gym = Ma(filename="lomsak_gym", mas=self, parent=self.lomsak)
        self.lomsak_temple = Ma(filename="lomsak_temple", mas=self, parent=self.lomsak)

        self.question_cave = Ma(filename="question_cave", mas=self)
        self.cat_cave = Ma(filename="cat_cave", mas=self, parent=self.phetchabun)
        self.cat_cave_2 = Ma(
            filename="cat_cave_2", mas=self, parent=self.cat_cove_hidden_house
        )
        self.bat_cave = Ma(filename="bat_cave", mas=self, parent=self.banyaeng)
        self.mystery_cave = Ma(
            filename="mystery_cave", mas=self, parent=self.chaiyaphum
        )
        self.cat_cove_house = Ma(filename="cat_cove_house", mas=self)
        self.cat_cove_house_2 = Ma(filename="cat_cove_house_2", mas=self)
        self.phetchabun_mountain_house_1 = Ma(
            filename="phetchabun_mountain_house_1", mas=self
        )
        self.phetchabun_mountain_house_2 = Ma(
            filename="phetchabun_mountain_house_2", mas=self
        )
        self.phetchabun_farm = Ma(filename="phetchabun_farm", mas=self)

        self.buengsamphan_cave = Ma(filename="buengsamphan_cave", mas=self)
        self.buengsamphan_chaiyaphum_cave = Ma(filename="buengsamphan_chaiyaphum_cave", mas=self)
        self.nakhon_sawan_aquarium = Ma(filename="nakhon_sawan_aquarium", mas=self)
        self.banyaeng_cave = Ma(filename="banyaeng_cave", mas=self)
        self.phetchabun_school = Ma(filename="phetchabun_school", mas=self)
        self.phetchabun_cave = Ma(filename="phetchabun_cave", mas=self)
        self.phetchabun_house_1 = Ma(filename="phetchabun_house_1", mas=self)
        self.phetchabun_house_2 = Ma(filename="phetchabun_house_2", mas=self)
        self.phitsanulok_underground = Ma(filename="phitsanulok_underground", mas=self)
        self.lomsak_labyrinth_house_1 = Ma(
            filename="lomsak_labyrinth_house_1", mas=self
        )
        self.lomsak_labyrinth_house_2 = Ma(
            filename="lomsak_labyrinth_house_2", mas=self
        )
        self.phetchabun_temple = Ma(filename="phetchabun_temple", mas=self)
        self.phetchabun_gym = Ma(filename="phetchabun_gym", mas=self)
        self.banyaeng_house_1 = Ma(
            filename="banyaeng_house_1", mas=self, parent=self.banyaeng
        )
        self.banyaeng_house_2 = Ma(
            filename="banyaeng_house_2", mas=self, parent=self.banyaeng
        )
        self.banyaeng_school = Ma(
            filename="banyaeng_school", mas=self, parent=self.banyaeng
        )
        self.banyaeng_temple = Ma(
            filename="banyaeng_temple", mas=self, parent=self.banyaeng
        )
        self.banyaeng_house_3 = Ma(
            filename="banyaeng_house_3", mas=self, parent=self.banyaeng
        )
        self.phetchabun_shop = Ma(
            filename="phetchabun_shop", mas=self, parent=self.phetchabun
        )
        self.lomsak_labyrinth_shop = Ma(
            filename="lomsak_labyrinth_shop", mas=self, parent=self.lomsak_labyrinth
        )
        self.chumphae_kasetsombum_cave = Ma(
            filename="chumphae_kasetsombum_cave", mas=self
        )
        self.kasetsombum_cave = Ma(filename="kasetsombum_cave", mas=self)
        self.labyrinth_shop = Ma(filename="labyrinth_shop", mas=self)
        self.kasetsombum_temple = Ma(
            filename="kasetsombum_temple",
            mas=self,
            parent=self.kasetsombum,
            x_shift=748,
            y_shift=624,
        )
        self.inn_kasetsombum = Ma(
            filename="inn_kasetsombum", mas=self, parent=self.kasetsombum
        )
        self.kasetsombum_temple_temple = Ma(
            filename="kasetsombum_temple_temple", mas=self, parent=self.kasetsombum
        )
        self.kasetsombum_house1 = Ma(
            filename="kasetsombum_house1", mas=self, parent=self.kasetsombum
        )
        self.kasetsombum_house2 = Ma(
            filename="kasetsombum_house2", mas=self, parent=self.kasetsombum
        )
        self.kasetsombum_house3 = Ma(
            filename="kasetsombum_house3", mas=self, parent=self.kasetsombum
        )
        self.kasetsombum_shop = Ma(
            filename="kasetsombum_shop", mas=self, parent=self.kasetsombum
        )
        self.kasetsombum_school = Ma(
            filename="kasetsombum_school", mas=self, parent=self.kasetsombum
        )
        self.phitsanulok_maths_school_123 = Ma(
            filename="phitsanulok_maths_school_123", mas=self, parent=self.phitsanulok
        )
        self.phitsanulok_maths_school_456 = Ma(
            filename="phitsanulok_maths_school_456", mas=self, parent=self.phitsanulok
        )
        self.phitsanulok_maths_school_789 = Ma(
            filename="phitsanulok_maths_school_789", mas=self, parent=self.phitsanulok
        )
        self.phitsanulok_maths_school_1011 = Ma(
            filename="phitsanulok_maths_school_1011", mas=self, parent=self.phitsanulok
        )
        self.ko_kut_cave_1 = Ma(filename="ko_kut_cave_1", mas=self, parent=self.ko_kut)
        self.current_map: Ma = self.chaiyaphum
        self.add_trigger_tiles()

    def add_trigger_tiles(self):
        pass
        # self.chaiyaphum.get_cell_at(20, 86).trigger = Trigger(event='lover_disappears', npcs=['Lover'])

    def get_map_from_name(self, name):
        return getattr(self, name)
