# We must first get rid of pickling entirely!
#
# class CellType(object):
#     def __init__(self, letter, name, color, walkable, encounter_rate):
#         self.letter = letter
#         self.name = name
#         self.color = color
#         self.walkable = walkable
#         self.encounter_rate = encounter_rate
#
#
# class CellTypes:
#     grass = CellType('草', 'grass', (100, 200, 100), True, 0.05)
#     tree = CellType('树', 'tree', (85, 107, 47), False, 0)
#     ground = CellType('土', 'ground', (176, 246, 176), True, 0)
#     tall_grass = CellType('稂', 'tall_grass', (0, 128, 0), True, 0.1)
#     path = CellType('道', 'path', (200, 200, 200), True, 0)
#     road = CellType('路', 'road', (154, 154, 154), True, 0)
#     wall = CellType('壁', 'wall', (22, 22, 22), False, 0)
#     sign = CellType('標', 'sign', (71, 71, 71), False, 0)
#     water = CellType('水', 'water', (57, 62, 255), False, 0.05)
#     cave_water = CellType('湿', 'cave_water', (24, 24, 58), False, 0.05)
#     decoration = CellType('飾', 'decoration', (123, 9, 9), False, 0)
#     flower = CellType('花', 'flower', (231, 148, 193), True, 0)
#     flower_2 = CellType('李', 'flower_2', (231, 148, 194), True, 0)
#     nenuphar = CellType('华', 'nenuphar', (189, 176, 246), True, 0)
#     door = CellType('门', 'door', (255, 0, 204), True, 0)
#     inn_floor = CellType('床', 'inn_floor', (117, 199, 242), True, 0)
#     inn_sign = CellType('館', 'inn_sign', (255, 152, 234), False, 0)
#     inn_map = CellType('図', 'inn_map', (99, 122, 80), False, 0)
#     temple_floor = CellType('寺', 'temple_floor', (183, 183, 183), True, 0)
#
#     # Cave
#     cave_floor = CellType('穴', 'cave_floor', (159, 122, 120), True, 0.05)  # should be 0.05
#     boulder_2 = CellType('岩', 'boulder_2', (53, 14, 14), False, 0)
#     rock = CellType('石', 'rock', (94, 37, 37), False, 0)
#     rocky_ground = CellType('嶝', 'rocky_path', (210, 185, 184), True, 0.05)  # should be 0.05
#     boulder = CellType('砾', 'boulder', (172, 92, 113), False, 0)
#     entrance = CellType('入', 'entrance', (227, 25, 77), True, 0)
#     cave_0010 = CellType('┏', 'cave_0010', (63, 222, 141), False, 0)
#     cave_0110 = CellType('┣', 'cave_0110', (63, 201, 222), False, 0)
#     cave_0100 = CellType('┗', 'cave_0100', (63, 104, 222), False, 0)
#     cave_1100 = CellType('┻', 'cave_1100', (149, 63, 222), False, 0)
#     cave_1000 = CellType('┛', 'cave_1000', (209, 63, 222), False, 0)
#     cave_1001 = CellType('┫', 'cave_1001', (222, 63, 104), False, 0)
#     cave_0001 = CellType('┓', 'cave_0001', (222, 100, 63), False, 0)
#     cave_0011 = CellType('┳', 'cave_0011', (183, 222, 63), True, 0)
#     cave_1110 = CellType('┐', 'cave_1110', (80, 95, 138), False, 0)
#     cave_1101 = CellType('┌', 'cave_1101', (122, 95, 124), False, 0)
#     cave_entrance_down = CellType('u', 'cave_entrance_down', (25, 227, 58), True, 0)
#     cave_stairs_1100 = CellType('║', 'cave_stairs_1100', (138, 0, 255), True, 0)
#     cave_stairs_0110 = CellType('═', 'cave_stairs_0110', (77, 178, 193), True, 0)
#     cave_stairs_1001 = CellType('─', 'cave_stairs_1001', (177, 85, 109), True, 0)
#     cave_stairs_0011 = CellType('│', 'cave_stairs_0011', (161, 186, 87), True, 0.05)
#     cave_0010_over_edge = CellType('┲', 'cave_0010_over_edge', (121, 222, 103), False, 0)
#     cave_0001_over_edge = CellType('┱', 'cave_0001_over_edge', (203, 159, 63), False, 0)
#
#     fruit_tree = CellType('果', 'fruit_tree', (192, 255, 81), False, 0)
#     waterfall = CellType('滝', 'waterfall', (57, 150, 255), True, 0.1)
#     bridge_hor = CellType('橋', 'bridge_hor', (163, 165, 255), True, 0)
#     bridge_ver = CellType('圯', 'bridge_ver', (163, 164, 255), True, 0)
#     fence = CellType('垣', 'fence', (102, 102, 102), False, 0)
#     arena_sign = CellType('競', 'arena_sign', (255, 192, 0), False, 0)
#     school_sign = CellType('学', 'school_sign', (103, 229, 216), False, 0)
#     shop_sign = CellType('買', 'shop_sign', (65, 71, 193), False, 0)
#     field = CellType('畑', 'field', (225, 232, 168), True, 0.04)
#     sand = CellType('砂', 'sand', (255, 218, 105), True, 0)
#     buddha_statue = CellType('仏', 'buddha_statue', (255, 215, 54), False, 0)
#     none = CellType('無', 'none', (0, 0, 0), False, 0)
#
#
# class Cell(object):
#     def __init__(self, x, y, typ: CellType):
#         self.x = x
#         self.y = y
#         self.typ: CellType = typ
#         self.goes_to = None  # can be a tuple (Map, x, y)
#
#     def walkable(self) -> bool:
#         return self.typ.walkable
