import os
from typing import List

from PIL import Image

from overworld import CellType

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def generate_postmap():
    from overworld import CellTypes
    cell_type_names = [a for a in dir(CellTypes) if not a.startswith("__")]
    cells: List[CellType] = [getattr(CellTypes, name) for name in cell_type_names]
    input_file = DIR_PATH + "/map_image_files/full_map.bmp"
    original_map = Image.open(input_file)
    # pix = im.load()

    t = ""
    postmap = original_map.copy()
    pix = postmap.load()

    # This method will show image in any image viewer

    width, height = postmap.size
    for x in range(height):
        for y in range(width):
            for cell in cells:
                if pix[y, x] == cell.color:
                    pix[y, x] = cell.postcolor
    postmap.save(f'{DIR_PATH}/map_image_files/postmap.bmp')
    postmap.show()
    # color_found = False
    # for cell_type_name in cell_type_names:
    #     cell_type = getattr(CellTypes, cell_type_name)
    #     if color == cell_type.color:
    #         color_found = True
    #         t += cell_type.letter
    # if not color_found:
    #     t += CellTypes.none.letter
    # t += "\n"
    # t = t[:-1]
    # return t


generate_postmap()