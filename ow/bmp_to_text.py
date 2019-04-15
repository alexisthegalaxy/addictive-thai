from PIL import Image

from overworld import CellTypes


def convert_bmp_to_text(file_name: str):
    import os

    dir_path = os.path.dirname(os.path.realpath(__file__))

    cell_type_names = [a for a in dir(CellTypes) if not a.startswith("__")]
    input_file = dir_path + "/map_image_files/" + file_name + ".bmp"
    output_file = dir_path + "/map_text_files/" + file_name
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
    f = open(output_file, "w+")
    f.write(t)
    print(f"Converted {file_name}!")
    return t


to_convert = [
    "house1",
    "house2",
    "house3",
    "house4",
    "lab",
    "inn1",
    "inn2",
    "inn3",
    "inn4",
    "inn5",
    "chaiyaphum",
    "chumphae",
    "chumphae_khonkaen",
    "chumphae_khonkaen_house_1",
    "chumphae_khonkaen_house_2",
    "chumphae_khonkaen_house_3",
    "chumphae_khonkaen_house_4",
    "chumphae_school",
    "chumphae_house1",
    "chumphae_house2",
    "chumphae_house3",
    "chumphae_lomsak_house1",
    "chumphae_lomsak_house2",
    "chumphae_lomsak_house3",
    "lomsak",
    "lomsak_house_1",
    "lomsak_house_2",
    "lomsak_school",
    "lomsak_gym",
    "non_muang_house_1",
    "phetchabun",
]

for item in to_convert:
    convert_bmp_to_text(item)
