from PIL import Image
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class Minimap(object):
    """
    Only contains the minimal information:
    a name, coordinates and size.
    It is not used throughout the game, it is only in the first step to build the text files of the maps
    """
    def __init__(self, name, x, y, x2, y2):
        self.name = name
        # the x and y are the coordinates pixels in the top right corner of the map
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.width = x2 - x
        self.height = y2 - y


def _get_text_from_mothermap():
    from overworld import CellTypes
    cell_type_names = [a for a in dir(CellTypes) if not a.startswith("__")]
    input_file = DIR_PATH + "/map_image_files/full_map.bmp"
    im = Image.open(input_file)
    pix = im.load()

    t = ""

    width, height = im.size
    for x in range(height):
        for y in range(width):
            color = pix[y, x]
            color_found = False
            for cell_type_name in cell_type_names:
                cell_type = getattr(CellTypes, cell_type_name)
                if color == cell_type.color:
                    color_found = True
                    t += cell_type.letter
            if not color_found:
                t += CellTypes.none.letter
        t += "\n"
    t = t[:-1]
    return t


class Mothermap(object):
    def __init__(self):
        self.minimaps = {
            'chaiyaphum': Minimap('chaiyaphum', x=780, y=629, x2=850, y2=747),
            'chumphae': Minimap('chumphae', x=699, y=563, x2=846, y2=654),
            'chumphae_khonkaen': Minimap('chumphae_khonkaen', x=824, y=551, x2=918, y2=647),
            'cat_cove': Minimap('cat_cove', x=710, y=616, x2=744, y2=650),
            'lomsak': Minimap('lomsak', x=676-6, y=543, x2=721, y2=590),
            'lomsak_labyrinth': Minimap('lomsak_labyrinth', x=620, y=548, x2=691, y2=592),
            'labyrinth': Minimap('labyrinth', x=586, y=545, x2=635, y2=597),
            'phetchabun': Minimap('phetchabun', x=639, y=572, x2=712, y2=657),
            'phitsalunok': Minimap('phitsalunok', x=530, y=545, x2=601, y2=614),
            'banyaeng': Minimap('banyaeng', x=599, y=578, x2=655, y2=650),
            'phetchabun_buengsamphan': Minimap('phetchabun_buengsamphan', x=647, y=639, x2=713, y2=715),
            'buengsamphan_chaiyaphum': Minimap('buengsamphan_chaiyaphum', x=719, y=689, x2=801, y2=732),
            'buengsamphan': Minimap('buengsamphan', x=650, y=702, x2=734, y2=738),
            'buengsamphan_mountain': Minimap('buengsamphan_mountain', x=697, y=689, x2=748, y2=711),
            'taphan_hin': Minimap('taphan_hin', x=537, y=594, x2=589, y2=671),
            'buengsamphan_chumsaeng': Minimap('buengsamphan_chumsaeng', x=569, y=664, x2=665, y2=728),
            'thapkhlo': Minimap('thapkhlo', x=578, y=648, x2=650, y2=676),
            'thapkhlo_phitsalunok': Minimap('thapkhlo_phitsalunok', x=572, y=596, x2=605, y2=660),
            'chumsaeng': Minimap('chumsaeng', x=537, y=660, x2=598, y2=727),
            'khonkaen': Minimap('khonkaen', x=897, y=611, x2=951, y2=655),
            'nakhon_sawan': Minimap('nakhon_sawan', x=502, y=703, x2=566, y2=745),
            'kasetsombum': Minimap('kasetsombum', x=761, y=635, x2=802, y2=663),
            # Rerun 'derive_from_mothermap' after modifications to that file.'
        }

    def write_text_files(self):
        """
        Opens the main map, makes a huge in-memory text file
        Then, cut from it the smaller maps.
        """
        t = _get_text_from_mothermap()
        text_for_each_map = {}  # { map_name: map_text }
        for minimap in self.minimaps.values():
            text_for_each_map[minimap.name] = ""
        for line_index, line in enumerate(t.split('\n')):
            for char_index, char in enumerate(line):
                for minimap in self.minimaps.values():
                    if minimap.x <= char_index <= minimap.x2 and minimap.y <= line_index <= minimap.y2:
                        text_for_each_map[minimap.name] += char
                        if char_index == minimap.x2 and line_index != minimap.y2:
                            text_for_each_map[minimap.name] += '\n'
            # Write in the text file
            # pass

        for minimap in self.minimaps.values():
            output_file_name = DIR_PATH + "/map_text_files/" + minimap.name
            f = open(output_file_name, "w+")
            f.write(text_for_each_map[minimap.name])
        print('done')


mothermap = Mothermap()


if __name__ == "__main__":
    mothermap.write_text_files()


# print(DIR_PATH + "/map_text_files/" + 'yo')
# print(DIR_PATH + "/map_text_files/" + 'yo')
# print(DIR_PATH + "/map_text_files/" + 'yo')
# print(DIR_PATH + "/map_text_files/" + 'yo')
# print(DIR_PATH + "/map_text_files/" + 'yo')
# #
#
# def convert_bmp_to_text(file_name: str):
#     import os
#
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#
#     cell_type_names = [a for a in dir(CellTypes) if not a.startswith("__")]
#     input_file = dir_path + "/map_image_files/" + file_name + ".bmp"
#     output_file = dir_path + "/map_text_files/" + file_name
#     im = Image.open(input_file)
#     pix = im.load()
#
#     t = ""
#
#     width, height = im.size
#     for x in range(height):
#         for y in range(width):
#             color = pix[y, x]
#             color_found = False
#             for cell_type_name in cell_type_names:
#                 cell_type = getattr(CellTypes, cell_type_name)
#                 if color == cell_type.color:
#                     color_found = True
#                     t += cell_type.letter
#             if not color_found:
#                 t += CellTypes.none.letter
#         t += "\n"
#     t = t[:-1]
#     f = open(output_file, "w+")
#     f.write(t)
#     print(f"Converted {file_name}!")
#     return t
#
#
#
