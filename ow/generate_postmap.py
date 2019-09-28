import os
from typing import List

from PIL import Image


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def generate_postmap():
    from overworld import get_cell_type_dictionary_by_color
    cell_dictionary = get_cell_type_dictionary_by_color()
    input_file = DIR_PATH + "/map_image_files/full_map.bmp"
    original_map = Image.open(input_file)
    postmap = original_map.copy()
    pix = postmap.load()
    _200200200 = cell_dictionary[(200, 200, 200)]
    # This method will show image in any image viewer
    postmap_text = ""
    width, height = postmap.size
    for x in range(width):
        for y in range(height):
            try:
                cell = cell_dictionary[pix[x, y]]
                color = cell.postcolor
                letter = cell.letter
                pix[x, y] = cell.postcolor
            except:
                color = pix[x, y]
                letter = "無"
            postmap_text += letter
            pix[x, y] = color
        postmap_text += "\n"
    postmap_text = postmap_text[:-1]
    # print(postmap_text)
    postmap.save(f'{DIR_PATH}/map_image_files/postmap.bmp')

    text_file_path = f'{DIR_PATH}/map_text_files/postmap'
    with open(text_file_path, "w") as f:
        f.write(postmap_text)
    # postmap.show()


if __name__ == "__main__":
    generate_postmap()
