from PIL import Image
import os


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class Daughtermap(object):
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
    from overworld import CellTypes, get_cell_type_dictionary_by_color
    input_file = DIR_PATH + "/map_image_files/full_map.bmp"
    im = Image.open(input_file)
    pix = im.load()
    cell_dictionary = get_cell_type_dictionary_by_color()
    t = ""

    width, height = im.size
    for x in range(height):
        for y in range(width):
            try:
                cell = cell_dictionary[pix[y, x]]
                letter = cell.letter
            except:
                letter = CellTypes.none.letter
            t += letter
        t += "\n"
    t = t[:-1]
    return t


class Mothermap(object):
    def __init__(self):
        self.daughtermaps = {
            'chaiyaphum': Daughtermap('chaiyaphum', x=780, y=629, x2=850, y2=747),
            'chumphae': Daughtermap('chumphae', x=699, y=563, x2=846, y2=654),
            'chumphae_khonkaen': Daughtermap('chumphae_khonkaen', x=824, y=551, x2=918, y2=647),
            'cat_cove': Daughtermap('cat_cove', x=710, y=616, x2=744, y2=650),
            'lomsak': Daughtermap('lomsak', x=676-6, y=543, x2=721, y2=590),
            'lomsak_labyrinth': Daughtermap('lomsak_labyrinth', x=620, y=548, x2=691, y2=592),
            'labyrinth': Daughtermap('labyrinth', x=586, y=545, x2=635, y2=597),
            'phetchabun': Daughtermap('phetchabun', x=639, y=572, x2=712, y2=657),
            'phitsanulok': Daughtermap('phitsanulok', x=530, y=545, x2=601, y2=614),
            'banyaeng': Daughtermap('banyaeng', x=599, y=578, x2=655, y2=650),
            'phetchabun_buengsamphan': Daughtermap('phetchabun_buengsamphan', x=647, y=639, x2=713, y2=715),
            'buengsamphan_chaiyaphum': Daughtermap('buengsamphan_chaiyaphum', x=719, y=689, x2=801, y2=732),
            'buengsamphan': Daughtermap('buengsamphan', x=650, y=702, x2=734, y2=738),
            'buengsamphan_mountain': Daughtermap('buengsamphan_mountain', x=697, y=689, x2=748, y2=711),
            'taphan_hin': Daughtermap('taphan_hin', x=537, y=594, x2=589, y2=671),
            'buengsamphan_chumsaeng': Daughtermap('buengsamphan_chumsaeng', x=569, y=664, x2=665, y2=728),
            'thapkhlo': Daughtermap('thapkhlo', x=578, y=648, x2=650, y2=676),
            'thapkhlo_phitsanulok': Daughtermap('thapkhlo_phitsanulok', x=572, y=596, x2=605, y2=660),
            'chumsaeng': Daughtermap('chumsaeng', x=537, y=660, x2=598, y2=727),
            'khonkaen': Daughtermap('khonkaen', x=897, y=611, x2=951, y2=656),
            'nakhon_sawan': Daughtermap('nakhon_sawan', x=502, y=703, x2=566, y2=745),
            'kasetsombum': Daughtermap('kasetsombum', x=761, y=635, x2=802, y2=663),
            'kasetsombum_temple': Daughtermap('kasetsombum_temple', x=748, y=624, x2=790, y2=650),
            'phitsanulok_sukhothai': Daughtermap('phitsanulok_sukhothai', x=493, y=540, x2=546, y2=584),
            'sukhothai': Daughtermap('sukhothai', x=468, y=513, x2=513, y2=549),
            'old_sukhothai': Daughtermap('old_sukhothai', x=429, y=514, x2=482, y2=549),
            'bua_yai': Daughtermap('bua_yai', x=795, y=699, x2=880, y2=769),
            'phon': Daughtermap('phon', x=865, y=644, x2=931, y2=760),
            'chaiyaphum_chatturat': Daughtermap('chaiyaphum_chatturat', x=750, y=715, x2=809, y2=774),
            'chatturat': Daughtermap('chatturat', x=704, y=762, x2=799, y2=805),
            # Islands
            'ko_kut': Daughtermap('ko_kut', x=806, y=1303, x2=871, y2=1367),
            # Rerun 'derive_from_mothermap' after modifications to that file.'
        }

    def old_write_text_files(self):  # Works!
        """
        Opens the main map, makes a huge in-memory text file
        Then, cut from it the smaller maps.
        """
        t = _get_text_from_mothermap()
        text_for_each_map = {}  # { map_name: map_text }
        for daughtermap in self.daughtermaps.values():
            text_for_each_map[daughtermap.name] = ""
        for line_index, line in enumerate(t.split('\n')):
            for char_index, char in enumerate(line):
                for daughtermap in self.daughtermaps.values():
                    if daughtermap.x <= char_index <= daughtermap.x2 and daughtermap.y <= line_index <= daughtermap.y2:
                        text_for_each_map[daughtermap.name] += char
                        if char_index == daughtermap.x2 and line_index != daughtermap.y2:
                            text_for_each_map[daughtermap.name] += '\n'

        for daughtermap in self.daughtermaps.values():
            output_file_name = DIR_PATH + "/map_text_files/" + daughtermap.name
            f = open(output_file_name, "w+")
            f.write(text_for_each_map[daughtermap.name])
        print('done')

    def write_text_files(self):
        """
        Opens the main map, makes a huge in-memory text file
        Then, cut from it the smaller maps.
        """
        t = _get_text_from_mothermap()
        text_for_each_map = {}  # { map_name: map_text }
        for daughtermap in self.daughtermaps.values():
            text_for_each_map[daughtermap.name] = ""
            for line_index, line in enumerate(t.split('\n')[daughtermap.y:daughtermap.y2 + 1]):
                for char_index, char in enumerate(line[daughtermap.x:daughtermap.x2 + 1]):
                    text_for_each_map[daughtermap.name] += char
                # if char_index == daughtermap.x2 and line_index != daughtermap.y2:
                text_for_each_map[daughtermap.name] += '\n'

        for daughtermap in self.daughtermaps.values():
            output_file_name = DIR_PATH + "/map_text_files/" + daughtermap.name
            f = open(output_file_name, "w+")
            f.write(text_for_each_map[daughtermap.name])


mothermap = Mothermap()  # is outside main so that files importing it can use it


if __name__ == "__main__":
    from generate_postmap import generate_postmap
    mothermap.write_text_files()
    generate_postmap()
    print('done')


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
