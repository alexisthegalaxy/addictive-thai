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
    "house_learner_f2",
    "house_learner_f1",
    "house_rival_f2",
    "house_rival_f1",
    "lover_house",
    "chaiyaphum_house_1",
    "plane",
    "chaiyaphum_house_2",
    "house4",
    "house5",
    "normal_inn",
    "inn_ko_kut",
    "ko_kut_cave_1",
    "banyaeng_cave",
    "phetchabun_school",
    "buengsamphan_cave",
    "buengsamphan_chaiyaphum_cave",
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
    "lomsak_house_1",
    "lomsak_house_2",
    "lomsak_house_3",
    "lomsak_house_4",
    "lomsak_school",
    "lomsak_gym",
    "lomsak_temple",
    "question_cave",
    "non_muang_house_1",
    "bat_cave",
    "cat_cave",
    "cat_cave_2",
    "cat_cove_house",
    "cat_cove_house_2",
    "cat_cove_hidden_shop",
    "phetchabun_mountain_house_1",
    "phetchabun_mountain_house_2",
    "phetchabun_farm",
    "nakhon_sawan_aquarium",
    "phitsanulok_underground",
    "phetchabun_cave",
    "lomsak_labyrinth_house_1",
    "lomsak_labyrinth_house_2",
    "phetchabun_house_1",
    "phetchabun_house_2",
    "phetchabun_gym",
    "phetchabun_temple",
    "banyaeng_house_1",
    "banyaeng_house_2",
    "banyaeng_house_3",
    "banyaeng_school",
    "banyaeng_temple",
    "phetchabun_shop",
    "labyrinth_shop",
    "lomsak_labyrinth_shop",
    "chumphae_kasetsombum_cave",
    "kasetsombum_cave",
    "mystery_cave",
    "inn_banyaeng",
    "inn_bua_yai",
    "inn_kasetsombum",
    "inn_phitsanulok",
    "inn_phitsanulok_2",
    "inn_chatturat",
    "kasetsombum_house1",
    "kasetsombum_house2",
    "kasetsombum_house3",
    "kasetsombum_temple_temple",
    "kasetsombum_shop",
    "kasetsombum_school",
    "phitsanulok_maths_school_123",
    "phitsanulok_maths_school_456",
    "phitsanulok_maths_school_789",
    "phitsanulok_maths_school_1011",
    "ko_kut_house_1",
    "ko_kut_house_2",
]

for item in to_convert:
    convert_bmp_to_text(item)
