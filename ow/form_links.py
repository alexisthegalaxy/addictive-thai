from derive_from_mothermap import mothermap
from direction import Direction


def form_links(mas):
    """
    In this function we define the 'links' (for example, a door leading to the
    inside of a house, i.e. to another map)
    """
    # ko_kut
    mas.ko_kut.get_cell_at(54, 34).goes_to = (mas.ko_kut_house_1, 5, 12)
    mas.ko_kut_house_1.get_cell_at(5, 13).goes_to = (mas.ko_kut, 54, 35)
    mas.ko_kut.get_cell_at(48, 27).goes_to = (mas.ko_kut_house_2, 5, 12)
    mas.ko_kut_house_2.get_cell_at(5, 13).goes_to = (mas.ko_kut, 48, 28)

    # ko_mak
    mas.ko_kut_cave_1.get_cell_at(15, 7).goes_to = (mas.ko_mak, 32, 10)
    mas.ko_mak.get_cell_at(32, 9).goes_to = (mas.ko_kut_cave_1, 15, 6)

    mas.ko_mak.get_cell_at(8, 14).goes_to = (mas.ko_klum, 8, 8)
    mas.ko_klum.get_cell_at(7, 8).goes_to = (mas.ko_mak, 8, 15)

    mas.ko_klum.get_cell_at(24, 12).goes_to = (mas.ko_chang, 44, 37)
    mas.ko_chang.get_cell_at(45, 37).goes_to = (mas.ko_klum, 23, 12)

    # chaiyaphum - chumphae
    mas.chaiyaphum.get_cell_at(42, 14).goes_to = (mas.chumphae, 123, 80)
    mas.chaiyaphum.get_cell_at(43, 14).goes_to = (mas.chumphae, 124, 80)
    mas.chumphae.get_cell_at(123, 81).goes_to = (mas.chaiyaphum, 42, 15)
    mas.chumphae.get_cell_at(124, 81).goes_to = (mas.chaiyaphum, 43, 15)
    # chaiyaphum
    mas.chaiyaphum.get_cell_at(28, 101).goes_to = (mas.house_learner_f1, 5, 12)
    mas.house_learner_f1.get_cell_at(5, 13).goes_to = (mas.chaiyaphum, 28, 102)
    mas.house_learner_f1.get_cell_at(2, 9).goes_to = (
        mas.house_learner_f2,
        2,
        8,
        Direction.UP,
    )
    mas.house_learner_f2.get_cell_at(2, 9).goes_to = (
        mas.house_learner_f1,
        2,
        10,
        Direction.DOWN,
    )
    mas.chaiyaphum.get_cell_at(20, 89).goes_to = (mas.lover_house, 5, 12)
    mas.lover_house.get_cell_at(5, 13).goes_to = (mas.chaiyaphum, 20, 90)
    mas.chaiyaphum.get_cell_at(20, 86).goes_to = (mas.lover_house, 8, 8)
    mas.lover_house.get_cell_at(8, 7).goes_to = (mas.chaiyaphum, 20, 85)
    mas.chaiyaphum.get_cell_at(32, 91).goes_to = (mas.house_rival_f1, 5, 12)
    mas.house_rival_f1.get_cell_at(5, 13).goes_to = (mas.chaiyaphum, 32, 92)
    mas.house_rival_f1.get_cell_at(8, 7).goes_to = (
        mas.house_rival_f2,
        8,
        8,
        Direction.DOWN,
    )
    mas.house_rival_f2.get_cell_at(8, 7).goes_to = (
        mas.house_rival_f1,
        8,
        8,
        Direction.DOWN,
    )
    mas.chaiyaphum.get_cell_at(25, 99).goes_to = (mas.chaiyaphum_house_1, 5, 12)
    mas.chaiyaphum_house_1.get_cell_at(5, 13).goes_to = (mas.chaiyaphum, 25, 100)
    mas.chaiyaphum.get_cell_at(34, 97).goes_to = (mas.chaiyaphum_house_2, 4, 12)
    mas.bua_yai.get_cell_at(22, 27).goes_to = (mas.chaiyaphum_house_2, 10, 12)
    mas.chaiyaphum_house_2.get_cell_at(4, 13).goes_to = (mas.chaiyaphum, 34, 98)
    mas.chaiyaphum_house_2.get_cell_at(10, 13).goes_to = (mas.bua_yai, 22, 28)
    mas.chaiyaphum.get_cell_at(30, 39).goes_to = (mas.house4, 5, 12)
    mas.house4.get_cell_at(5, 13).goes_to = (mas.chaiyaphum, 30, 40)
    mas.chaiyaphum.get_cell_at(53, 10).goes_to = (mas.house5, 5, 12)
    mas.house5.get_cell_at(5, 13).goes_to = (mas.chaiyaphum, 53, 11)
    mas.chaiyaphum.get_cell_at(37, 90).goes_to = (mas.mystery_cave, 9, 11)
    mas.mystery_cave.get_cell_at(9, 12).goes_to = (mas.chaiyaphum, 37, 91)
    mas.mystery_cave.get_cell_at(15, 10).goes_to = (mas.ko_kut, 49, 53)
    mas.ko_kut.get_cell_at(49, 52).goes_to = (mas.mystery_cave, 15, 9)

    # bua yai
    mas.bua_yai.get_cell_at(59, 50).goes_to = (mas.inn_bua_yai, 4, 7)
    mas.inn_bua_yai.get_cell_at(4, 8).goes_to = (mas.bua_yai, 59, 51)
    mas.bua_yai.get_cell_at(78, 51).goes_to = (mas.phon, 8, 106)
    mas.bua_yai.get_cell_at(78, 52).goes_to = (mas.phon, 8, 107)
    mas.phon.get_cell_at(7, 106).goes_to = (mas.bua_yai, 77, 51)
    mas.phon.get_cell_at(7, 107).goes_to = (mas.bua_yai, 77, 52)

    # phon
    mas.phon.get_cell_at(58, 7).goes_to = (mas.khonkaen, 26, 40)
    mas.phon.get_cell_at(59, 7).goes_to = (mas.khonkaen, 27, 40)
    mas.khonkaen.get_cell_at(26, 41).goes_to = (mas.phon, 58, 8)
    mas.khonkaen.get_cell_at(27, 41).goes_to = (mas.phon, 59, 8)

    # chumphae
    mas.chumphae.get_cell_at(126, 74).goes_to = (mas.inn1, 4, 7)
    mas.inn1.get_cell_at(4, 8).goes_to = (mas.chumphae, 126, 75)
    mas.chumphae_school.get_cell_at(13, 25).goes_to = (mas.chumphae, 123, 61)
    mas.chumphae.get_cell_at(123, 60).goes_to = (mas.chumphae_school, 13, 24)
    mas.chumphae_house2.get_cell_at(5, 13).goes_to = (mas.chumphae, 117, 64)
    mas.chumphae.get_cell_at(117, 63).goes_to = (mas.chumphae_house2, 5, 12)
    mas.chumphae_house1.get_cell_at(5, 13).goes_to = (mas.chumphae, 127, 62)
    mas.chumphae.get_cell_at(127, 61).goes_to = (mas.chumphae_house1, 5, 12)
    mas.chumphae_house3.get_cell_at(7, 13).goes_to = (mas.chumphae, 118, 74)
    mas.chumphae.get_cell_at(118, 73).goes_to = (mas.chumphae_house3, 7, 12)

    mas.chumphae.get_cell_at(97, 77).goes_to = (
        mas.chumphae_kasetsombum_cave,
        19,
        4,
    )
    mas.chumphae_kasetsombum_cave.get_cell_at(19, 5).goes_to = (
        mas.chumphae,
        97,
        78,
    )

    mas.non_muang_house_1.get_cell_at(7, 13).goes_to = (mas.chumphae, 113, 76)
    mas.chumphae.get_cell_at(113, 75).goes_to = (mas.non_muang_house_1, 7, 12)
    # chumphae_khonkaen
    mas.chumphae_khonkaen.get_cell_at(12, 78).goes_to = (mas.chumphae, 137, 66)
    mas.chumphae_khonkaen.get_cell_at(12, 79).goes_to = (mas.chumphae, 137, 67)
    mas.chumphae.get_cell_at(138, 66).goes_to = (mas.chumphae_khonkaen, 13, 78)
    mas.chumphae.get_cell_at(138, 67).goes_to = (mas.chumphae_khonkaen, 13, 79)
    mas.chumphae_khonkaen.get_cell_at(18, 76).goes_to = (
        mas.chumphae_khonkaen_house_1,
        5,
        12,
    )
    mas.chumphae_khonkaen_house_1.get_cell_at(5, 13).goes_to = (
        mas.chumphae_khonkaen,
        18,
        77,
    )
    mas.chumphae_khonkaen.get_cell_at(29, 71).goes_to = (
        mas.chumphae_khonkaen_house_2,
        5,
        12,
    )
    mas.chumphae_khonkaen_house_2.get_cell_at(5, 13).goes_to = (
        mas.chumphae_khonkaen,
        29,
        72,
    )
    mas.chumphae_khonkaen.get_cell_at(34, 83).goes_to = (
        mas.chumphae_khonkaen_house_3,
        5,
        12,
    )
    mas.chumphae_khonkaen_house_3.get_cell_at(5, 13).goes_to = (
        mas.chumphae_khonkaen,
        34,
        84,
    )
    mas.chumphae_khonkaen.get_cell_at(43, 69).goes_to = (
        mas.chumphae_khonkaen_house_4,
        7,
        12,
    )
    mas.chumphae_khonkaen_house_4.get_cell_at(7, 13).goes_to = (
        mas.chumphae_khonkaen,
        43,
        70,
    )
    # chumphae_lomsak
    mas.chumphae.get_cell_at(104, 42).goes_to = (
        mas.chumphae_lomsak_house1,
        5,
        12,
    )
    mas.chumphae_lomsak_house1.get_cell_at(5, 13).goes_to = (
        mas.chumphae,
        104,
        43,
    )
    mas.chumphae.get_cell_at(87, 36).goes_to = (mas.chumphae_lomsak_house2, 5, 12)
    mas.chumphae_lomsak_house2.get_cell_at(5, 13).goes_to = (mas.chumphae, 87, 37)
    mas.chumphae.get_cell_at(37, 34).goes_to = (mas.chumphae_lomsak_house3, 5, 12)
    mas.chumphae_lomsak_house3.get_cell_at(5, 13).goes_to = (mas.chumphae, 37, 35)
    # lomsak
    mas.chumphae.get_cell_at(13, 19).goes_to = (mas.lomsak, 36 + 6, 39)
    mas.chumphae.get_cell_at(13, 20).goes_to = (mas.lomsak, 36 + 6, 40)
    mas.lomsak.get_cell_at(37 + 6, 39).goes_to = (mas.chumphae, 14, 19)
    mas.lomsak.get_cell_at(37 + 6, 40).goes_to = (mas.chumphae, 14, 20)
    mas.lomsak.get_cell_at(29 + 6, 32).goes_to = (mas.inn2, 4, 7)
    mas.inn2.get_cell_at(4, 8).goes_to = (mas.lomsak, 29 + 6, 33)
    mas.lomsak.get_cell_at(19 + 6, 36).goes_to = (mas.lomsak_house_1, 5, 12)
    mas.lomsak_house_1.get_cell_at(5, 13).goes_to = (mas.lomsak, 19 + 6, 37)
    mas.lomsak.get_cell_at(13, 24).goes_to = (mas.lomsak_house_2, 5, 12)
    mas.lomsak_house_2.get_cell_at(5, 13).goes_to = (mas.lomsak, 13, 25)
    mas.lomsak.get_cell_at(28 + 6, 24).goes_to = (mas.lomsak_school, 13, 24)
    mas.lomsak_school.get_cell_at(13, 25).goes_to = (mas.lomsak, 28 + 6, 25)
    mas.lomsak.get_cell_at(31 + 6, 23).goes_to = (mas.lomsak_school, 19, 16)
    mas.lomsak_school.get_cell_at(20, 16).goes_to = (mas.lomsak, 37, 22)
    mas.lomsak.get_cell_at(16 + 6, 24).goes_to = (mas.lomsak_gym, 13, 24)
    mas.lomsak_gym.get_cell_at(13, 25).goes_to = (mas.lomsak, 16 + 6, 25)
    mas.lomsak.get_cell_at(21 + 6, 12).goes_to = (mas.lomsak_temple, 13, 24)
    mas.lomsak_temple.get_cell_at(13, 25).goes_to = (mas.lomsak, 21 + 6, 13)

    # cat cove
    mas.cat_cave.get_cell_at(13, 3).goes_to = (mas.cat_cove, 19, 29)
    mas.cat_cove.get_cell_at(19, 30).goes_to = (mas.cat_cave, 13, 4)
    mas.cat_cove.get_cell_at(11, 6).goes_to = (mas.cat_cove_house, 5, 12)
    mas.cat_cove_house.get_cell_at(5, 13).goes_to = (mas.cat_cove, 11, 7)

    mas.cat_cove_hidden_house.get_cell_at(21, 17).goes_to = (mas.cat_cove_house_2, 5, 12)
    mas.cat_cove_house_2.get_cell_at(5, 13).goes_to = (mas.cat_cove_hidden_house, 21, 18)

    mas.cat_cove_hidden_house.get_cell_at(40, 10).goes_to = (mas.cat_cove_hidden_shop, 13, 24)
    mas.cat_cove_hidden_shop.get_cell_at(13, 25).goes_to = (mas.cat_cove_hidden_house, 40, 11)

    mas.cat_cove.get_cell_at(25, 10).goes_to = (mas.cat_cave_2, 8, 17)
    mas.cat_cave_2.get_cell_at(54, 13).goes_to = (mas.kasetsombum_temple, 33, 5)
    mas.kasetsombum_temple.get_cell_at(33, 4).goes_to = (mas.cat_cave_2, 54, 12)
    mas.cat_cave_2.get_cell_at(43, 8).goes_to = (mas.cat_cave_2, 54, 8)
    mas.kasetsombum_temple.get_cell_at(18, 4).goes_to = (mas.cat_cave_2, 39, 19)
    mas.cat_cave_2.get_cell_at(27, 11).goes_to = (
        mas.cat_cove_hidden_house,
        34,
        11,
    )
    mas.cat_cove_hidden_house.get_cell_at(28, 11).goes_to = (
        mas.cat_cave_2,
        21,
        11,
    )
    mas.cat_cave_2.get_cell_at(21, 12).goes_to = (
        mas.cat_cove_hidden_house,
        28,
        12,
    )
    mas.cat_cove_hidden_house.get_cell_at(34, 10).goes_to = (
        mas.cat_cave_2,
        27,
        10,
    )

    mas.phetchabun.get_cell_at(49, 8).goes_to = (mas.lomsak, 12 + 6, 37)
    mas.lomsak.get_cell_at(12 + 6, 38).goes_to = (mas.phetchabun, 49, 9)
    mas.phetchabun.get_cell_at(50, 8).goes_to = (mas.lomsak, 13 + 6, 37)
    mas.lomsak.get_cell_at(13 + 6, 38).goes_to = (mas.phetchabun, 50, 9)

    # Banyaeng forest
    mas.banyaeng.get_cell_at(8, 10).goes_to = (mas.labyrinth, 21, 43)
    mas.banyaeng.get_cell_at(9, 10).goes_to = (mas.labyrinth, 22, 43)
    mas.labyrinth.get_cell_at(21, 44).goes_to = (mas.banyaeng, 8, 11)
    mas.labyrinth.get_cell_at(22, 44).goes_to = (mas.banyaeng, 9, 11)

    mas.labyrinth.get_cell_at(7, 16).goes_to = (mas.phitsanulok, 63, 16)
    mas.labyrinth.get_cell_at(8, 16).goes_to = (mas.phitsanulok, 64, 16)
    mas.phitsanulok.get_cell_at(63, 15).goes_to = (mas.labyrinth, 7, 15)
    mas.phitsanulok.get_cell_at(64, 15).goes_to = (mas.labyrinth, 8, 15)

    mas.labyrinth.get_cell_at(42, 9).goes_to = (mas.lomsak_labyrinth, 8, 6)
    mas.labyrinth.get_cell_at(42, 10).goes_to = (mas.lomsak_labyrinth, 8, 7)
    mas.lomsak_labyrinth.get_cell_at(7, 6).goes_to = (mas.labyrinth, 41, 9)
    mas.lomsak_labyrinth.get_cell_at(7, 7).goes_to = (mas.labyrinth, 41, 10)

    mas.lomsak.get_cell_at(
        677 - mothermap.daughtermaps["lomsak"].x,
        567 - mothermap.daughtermaps["lomsak"].y,
    ).goes_to = (
        mas.lomsak_labyrinth,
        677 - mothermap.daughtermaps["lomsak_labyrinth"].x,
        567 - mothermap.daughtermaps["lomsak_labyrinth"].y,
    )
    mas.lomsak.get_cell_at(
        677 - mothermap.daughtermaps["lomsak"].x,
        568 - mothermap.daughtermaps["lomsak"].y,
    ).goes_to = (
        mas.lomsak_labyrinth,
        677 - mothermap.daughtermaps["lomsak_labyrinth"].x,
        568 - mothermap.daughtermaps["lomsak_labyrinth"].y,
    )
    mas.lomsak_labyrinth.get_cell_at(
        677 + 1 - mothermap.daughtermaps["lomsak_labyrinth"].x,
        567 - mothermap.daughtermaps["lomsak_labyrinth"].y,
    ).goes_to = (
        mas.lomsak,
        677 + 1 - mothermap.daughtermaps["lomsak"].x,
        567 - mothermap.daughtermaps["lomsak"].y,
    )
    mas.lomsak_labyrinth.get_cell_at(
        677 + 1 - mothermap.daughtermaps["lomsak_labyrinth"].x,
        568 - mothermap.daughtermaps["lomsak_labyrinth"].y,
    ).goes_to = (
        mas.lomsak,
        677 + 1 - mothermap.daughtermaps["lomsak"].x,
        568 - mothermap.daughtermaps["lomsak"].y,
    )

    # Phetchabun
    mas.phetchabun.get_cell_at(8, 57).goes_to = (mas.banyaeng, 48, 51)
    mas.phetchabun.get_cell_at(8, 58).goes_to = (mas.banyaeng, 48, 52)
    mas.banyaeng.get_cell_at(49, 51).goes_to = (mas.phetchabun, 9, 57)
    mas.banyaeng.get_cell_at(49, 52).goes_to = (mas.phetchabun, 9, 58)
    mas.phetchabun.get_cell_at(17, 17).goes_to = (mas.question_cave, 24, 26)
    mas.question_cave.get_cell_at(24, 27).goes_to = (mas.phetchabun, 17, 18)
    mas.phetchabun.get_cell_at(11, 27).goes_to = (mas.question_cave, 18, 39)
    mas.question_cave.get_cell_at(18, 40).goes_to = (mas.phetchabun, 11, 28)

    mas.phetchabun.get_cell_at(24, 35).goes_to = (mas.question_cave, 31, 47)
    mas.question_cave.get_cell_at(31, 48).goes_to = (mas.phetchabun, 24, 36)
    mas.phetchabun.get_cell_at(10, 19).goes_to = (mas.question_cave, 18, 10)
    mas.question_cave.get_cell_at(18, 11).goes_to = (mas.phetchabun, 10, 20)

    mas.phetchabun.get_cell_at(36, 54).goes_to = (mas.cat_cave, 6, 12)
    mas.cat_cave.get_cell_at(6, 13).goes_to = (mas.phetchabun, 36, 55)
    mas.phetchabun.get_cell_at(26, 60).goes_to = (mas.phetchabun_house_1, 5, 12)
    mas.phetchabun_house_1.get_cell_at(5, 13).goes_to = (mas.phetchabun, 26, 61)
    mas.phetchabun.get_cell_at(21, 7).goes_to = (mas.lomsak_labyrinth, 40, 31)
    mas.phetchabun.get_cell_at(22, 7).goes_to = (mas.lomsak_labyrinth, 41, 31)
    mas.lomsak_labyrinth.get_cell_at(40, 32).goes_to = (mas.phetchabun, 21, 8)
    mas.lomsak_labyrinth.get_cell_at(41, 32).goes_to = (mas.phetchabun, 22, 8)
    mas.phetchabun.get_cell_at(42, 18).goes_to = (mas.lomsak_house_3, 13, 24)
    mas.lomsak_house_3.get_cell_at(13, 25).goes_to = (mas.phetchabun, 42, 19)
    mas.phetchabun.get_cell_at(59, 13).goes_to = (mas.lomsak_house_4, 13, 24)
    mas.lomsak_house_4.get_cell_at(13, 25).goes_to = (mas.phetchabun, 59, 14)
    mas.phetchabun.get_cell_at(24, 10).goes_to = (
        mas.phetchabun_mountain_house_1,
        7,
        12,
    )
    mas.phetchabun_mountain_house_1.get_cell_at(7, 13).goes_to = (
        mas.phetchabun,
        24,
        11,
    )
    mas.phetchabun.get_cell_at(22, 24).goes_to = (
        mas.phetchabun_mountain_house_2,
        7,
        12,
    )
    mas.phetchabun_mountain_house_2.get_cell_at(7, 13).goes_to = (
        mas.phetchabun,
        22,
        25,
    )
    mas.phetchabun.get_cell_at(46, 62).goes_to = (mas.phetchabun_farm, 10, 24)
    mas.phetchabun_farm.get_cell_at(10, 25).goes_to = (mas.phetchabun, 46, 63)
    mas.phetchabun_farm.get_cell_at(16, 25).goes_to = (mas.phetchabun, 49, 63)
    mas.phetchabun.get_cell_at(49, 62).goes_to = (mas.phetchabun_farm, 16, 24)
    mas.phetchabun.get_cell_at(
        677 - mothermap.daughtermaps["phetchabun"].x,
        645 - mothermap.daughtermaps["phetchabun"].y,
    ).goes_to = (
        mas.phetchabun_buengsamphan,
        677 - mothermap.daughtermaps["phetchabun_buengsamphan"].x,
        645 - mothermap.daughtermaps["phetchabun_buengsamphan"].y,
    )
    mas.phetchabun.get_cell_at(
        678 - mothermap.daughtermaps["phetchabun"].x,
        645 - mothermap.daughtermaps["phetchabun"].y,
    ).goes_to = (
        mas.phetchabun_buengsamphan,
        678 - mothermap.daughtermaps["phetchabun_buengsamphan"].x,
        645 - mothermap.daughtermaps["phetchabun_buengsamphan"].y,
    )
    mas.phetchabun_buengsamphan.get_cell_at(
        677 - mothermap.daughtermaps["phetchabun_buengsamphan"].x,
        643 - mothermap.daughtermaps["phetchabun_buengsamphan"].y,
    ).goes_to = (
        mas.phetchabun,
        677 - mothermap.daughtermaps["phetchabun"].x,
        643 - mothermap.daughtermaps["phetchabun"].y,
    )
    mas.phetchabun_buengsamphan.get_cell_at(
        678 - mothermap.daughtermaps["phetchabun_buengsamphan"].x,
        643 - mothermap.daughtermaps["phetchabun_buengsamphan"].y,
    ).goes_to = (
        mas.phetchabun,
        678 - mothermap.daughtermaps["phetchabun"].x,
        643 - mothermap.daughtermaps["phetchabun"].y,
    )
    mas.phetchabun_buengsamphan.get_cell_at(21, 67).goes_to = (
        mas.buengsamphan,
        668 - mothermap.daughtermaps["buengsamphan"].x,
        706 - mothermap.daughtermaps["buengsamphan"].y,
    )
    mas.phetchabun_buengsamphan.get_cell_at(21, 68).goes_to = (
        mas.buengsamphan,
        668 - mothermap.daughtermaps["buengsamphan"].x,
        707 - mothermap.daughtermaps["buengsamphan"].y,
    )
    mas.buengsamphan.get_cell_at(19, 5).goes_to = (
        mas.phetchabun_buengsamphan,
        669 - mothermap.daughtermaps["phetchabun_buengsamphan"].x,
        707 - mothermap.daughtermaps["phetchabun_buengsamphan"].y,
    )
    mas.buengsamphan.get_cell_at(19, 4).goes_to = (
        mas.phetchabun_buengsamphan,
        669 - mothermap.daughtermaps["phetchabun_buengsamphan"].x,
        706 - mothermap.daughtermaps["phetchabun_buengsamphan"].y,
    )
    mas.phetchabun.get_cell_at(13, 52).goes_to = (mas.phetchabun_school, 13, 24)
    mas.phetchabun_school.get_cell_at(13, 25).goes_to = (mas.phetchabun, 13, 53)
    mas.phetchabun.get_cell_at(26, 52).goes_to = (mas.inn_phetchabun, 4, 7)
    mas.inn_phetchabun.get_cell_at(4, 8).goes_to = (mas.phetchabun, 26, 53)
    mas.phetchabun.get_cell_at(66, 22).goes_to = (mas.phetchabun_cave, 4, 1)
    mas.phetchabun_cave.get_cell_at(4, 2).goes_to = (mas.phetchabun, 66, 23)
    mas.phetchabun.get_cell_at(66, 34).goes_to = (mas.phetchabun_cave, 4, 13)
    mas.phetchabun_cave.get_cell_at(4, 14).goes_to = (mas.phetchabun, 66, 35)
    mas.phetchabun.get_cell_at(33, 62).goes_to = (mas.phetchabun_temple, 13, 24)
    mas.phetchabun_temple.get_cell_at(13, 25).goes_to = (mas.phetchabun, 33, 63)
    mas.phetchabun.get_cell_at(15, 62).goes_to = (mas.phetchabun_gym, 12, 24)
    mas.phetchabun_gym.get_cell_at(12, 25).goes_to = (mas.phetchabun, 15, 63)
    mas.phetchabun.get_cell_at(21, 50).goes_to = (mas.phetchabun_house_2, 5, 12)
    mas.phetchabun_house_2.get_cell_at(5, 13).goes_to = (mas.phetchabun, 21, 51)
    mas.phetchabun.get_cell_at(21, 56).goes_to = (mas.phetchabun_shop, 5, 12)
    mas.phetchabun_shop.get_cell_at(5, 13).goes_to = (mas.phetchabun, 21, 57)
    mas.phetchabun.get_cell_at(28, 79).goes_to = (
        mas.phetchabun_buengsamphan,
        20,
        12,
    )
    mas.phetchabun_buengsamphan.get_cell_at(20, 11).goes_to = (
        mas.phetchabun,
        28,
        78,
    )

    mas.buengsamphan.get_cell_at(7, 11).goes_to = (
        mas.buengsamphan_chumsaeng,
        657 - mothermap.daughtermaps["buengsamphan_chumsaeng"].x,
        713 - mothermap.daughtermaps["buengsamphan_chumsaeng"].y,
    )
    mas.buengsamphan.get_cell_at(7, 10).goes_to = (
        mas.buengsamphan_chumsaeng,
        657 - mothermap.daughtermaps["buengsamphan_chumsaeng"].x,
        712 - mothermap.daughtermaps["buengsamphan_chumsaeng"].y,
    )
    mas.buengsamphan_chumsaeng.get_cell_at(89, 48).goes_to = (
        mas.buengsamphan,
        658 - mothermap.daughtermaps["buengsamphan"].x,
        712 - mothermap.daughtermaps["buengsamphan"].y,
    )
    mas.buengsamphan_chumsaeng.get_cell_at(89, 49).goes_to = (
        mas.buengsamphan,
        658 - mothermap.daughtermaps["buengsamphan"].x,
        713 - mothermap.daughtermaps["buengsamphan"].y,
    )

    mas.buengsamphan_chumsaeng.get_cell_at(32, 6).goes_to = (
        mas.thapkhlo,
        601 - mothermap.daughtermaps["thapkhlo"].x,
        670 - mothermap.daughtermaps["thapkhlo"].y,
    )
    mas.buengsamphan_chumsaeng.get_cell_at(33, 6).goes_to = (
        mas.thapkhlo,
        602 - mothermap.daughtermaps["thapkhlo"].x,
        670 - mothermap.daughtermaps["thapkhlo"].y,
    )
    mas.thapkhlo.get_cell_at(23, 23).goes_to = (
        mas.buengsamphan_chumsaeng,
        601 - mothermap.daughtermaps["buengsamphan_chumsaeng"].x,
        671 - mothermap.daughtermaps["buengsamphan_chumsaeng"].y,
    )
    mas.thapkhlo.get_cell_at(24, 23).goes_to = (
        mas.buengsamphan_chumsaeng,
        602 - mothermap.daughtermaps["buengsamphan_chumsaeng"].x,
        671 - mothermap.daughtermaps["buengsamphan_chumsaeng"].y,
    )

    mas.thapkhlo.get_cell_at(7, 16).goes_to = (
        mas.chumsaeng,
        585 - mothermap.daughtermaps["chumsaeng"].x,
        664 - mothermap.daughtermaps["chumsaeng"].y,
    )
    mas.thapkhlo.get_cell_at(7, 17).goes_to = (
        mas.chumsaeng,
        585 - mothermap.daughtermaps["chumsaeng"].x,
        665 - mothermap.daughtermaps["chumsaeng"].y,
    )
    mas.chumsaeng.get_cell_at(49, 4).goes_to = (
        mas.thapkhlo,
        586 - mothermap.daughtermaps["thapkhlo"].x,
        664 - mothermap.daughtermaps["thapkhlo"].y,
    )
    mas.chumsaeng.get_cell_at(49, 5).goes_to = (
        mas.thapkhlo,
        586 - mothermap.daughtermaps["thapkhlo"].x,
        665 - mothermap.daughtermaps["thapkhlo"].y,
    )

    mas.taphan_hin.get_cell_at(23, 6).goes_to = (
        mas.phitsanulok,
        560 - mothermap.daughtermaps["phitsanulok"].x,
        600 - mothermap.daughtermaps["phitsanulok"].y,
    )
    mas.taphan_hin.get_cell_at(24, 6).goes_to = (
        mas.phitsanulok,
        561 - mothermap.daughtermaps["phitsanulok"].x,
        600 - mothermap.daughtermaps["phitsanulok"].y,
    )
    mas.phitsanulok.get_cell_at(30, 56).goes_to = (
        mas.taphan_hin,
        560 - mothermap.daughtermaps["taphan_hin"].x,
        601 - mothermap.daughtermaps["taphan_hin"].y,
    )
    mas.phitsanulok.get_cell_at(31, 56).goes_to = (
        mas.taphan_hin,
        561 - mothermap.daughtermaps["taphan_hin"].x,
        601 - mothermap.daughtermaps["taphan_hin"].y,
    )

    mas.phitsanulok.get_cell_at(21, 68).goes_to = (
        mas.taphan_hin,
        560 - mothermap.daughtermaps["taphan_hin"].x,
        601 - mothermap.daughtermaps["taphan_hin"].y,
    )
    mas.phitsanulok.get_cell_at(21, 68).goes_to = (
        mas.taphan_hin,
        561 - mothermap.daughtermaps["taphan_hin"].x,
        601 - mothermap.daughtermaps["taphan_hin"].y,
    )

    mas.thapkhlo.get_cell_at(
        597 - mothermap.daughtermaps["thapkhlo"].x,
        652 - mothermap.daughtermaps["thapkhlo"].y,
    ).goes_to = (
        mas.thapkhlo_phitsanulok,
        597 - mothermap.daughtermaps["thapkhlo_phitsanulok"].x,
        652 - mothermap.daughtermaps["thapkhlo_phitsanulok"].y,
    )
    mas.thapkhlo.get_cell_at(
        598 - mothermap.daughtermaps["thapkhlo"].x,
        652 - mothermap.daughtermaps["thapkhlo"].y,
    ).goes_to = (
        mas.thapkhlo_phitsanulok,
        598 - mothermap.daughtermaps["thapkhlo_phitsanulok"].x,
        652 - mothermap.daughtermaps["thapkhlo_phitsanulok"].y,
    )
    mas.thapkhlo_phitsanulok.get_cell_at(
        597 - mothermap.daughtermaps["thapkhlo_phitsanulok"].x,
        653 - mothermap.daughtermaps["thapkhlo_phitsanulok"].y,
    ).goes_to = (
        mas.thapkhlo,
        597 - mothermap.daughtermaps["thapkhlo"].x,
        653 - mothermap.daughtermaps["thapkhlo"].y,
    )
    mas.thapkhlo_phitsanulok.get_cell_at(
        598 - mothermap.daughtermaps["thapkhlo_phitsanulok"].x,
        653 - mothermap.daughtermaps["thapkhlo_phitsanulok"].y,
    ).goes_to = (
        mas.thapkhlo,
        598 - mothermap.daughtermaps["thapkhlo"].x,
        653 - mothermap.daughtermaps["thapkhlo"].y,
    )

    mas.thapkhlo_phitsanulok.get_cell_at(
        579 - mothermap.daughtermaps["thapkhlo_phitsanulok"].x,
        602 - mothermap.daughtermaps["thapkhlo_phitsanulok"].y,
    ).goes_to = (
        mas.phitsanulok,
        579 - mothermap.daughtermaps["phitsanulok"].x,
        602 - mothermap.daughtermaps["phitsanulok"].y,
    )
    mas.thapkhlo_phitsanulok.get_cell_at(
        579 - mothermap.daughtermaps["thapkhlo_phitsanulok"].x,
        603 - mothermap.daughtermaps["thapkhlo_phitsanulok"].y,
    ).goes_to = (
        mas.phitsanulok,
        579 - mothermap.daughtermaps["phitsanulok"].x,
        603 - mothermap.daughtermaps["phitsanulok"].y,
    )
    mas.phitsanulok.get_cell_at(
        580 - mothermap.daughtermaps["phitsanulok"].x,
        602 - mothermap.daughtermaps["phitsanulok"].y,
    ).goes_to = (
        mas.thapkhlo_phitsanulok,
        580 - mothermap.daughtermaps["thapkhlo_phitsanulok"].x,
        602 - mothermap.daughtermaps["thapkhlo_phitsanulok"].y,
    )
    mas.phitsanulok.get_cell_at(
        580 - mothermap.daughtermaps["phitsanulok"].x,
        603 - mothermap.daughtermaps["phitsanulok"].y,
    ).goes_to = (
        mas.thapkhlo_phitsanulok,
        580 - mothermap.daughtermaps["thapkhlo_phitsanulok"].x,
        603 - mothermap.daughtermaps["thapkhlo_phitsanulok"].y,
    )

    mas.taphan_hin.get_cell_at(22, 73).goes_to = (
        mas.chumsaeng,
        559 - mothermap.daughtermaps["chumsaeng"].x,
        667 - mothermap.daughtermaps["chumsaeng"].y,
    )
    mas.taphan_hin.get_cell_at(23, 73).goes_to = (
        mas.chumsaeng,
        560 - mothermap.daughtermaps["chumsaeng"].x,
        667 - mothermap.daughtermaps["chumsaeng"].y,
    )
    mas.chumsaeng.get_cell_at(22, 6).goes_to = (
        mas.taphan_hin,
        559 - mothermap.daughtermaps["taphan_hin"].x,
        666 - mothermap.daughtermaps["taphan_hin"].y,
    )
    mas.chumsaeng.get_cell_at(23, 6).goes_to = (
        mas.taphan_hin,
        560 - mothermap.daughtermaps["taphan_hin"].x,
        666 - mothermap.daughtermaps["taphan_hin"].y,
    )

    # Khonkaen
    mas.chumphae_khonkaen.get_cell_at(82, 80).goes_to = (
        mas.khonkaen,
        906 - mothermap.daughtermaps["khonkaen"].x,
        631 - mothermap.daughtermaps["khonkaen"].y,
    )
    mas.chumphae_khonkaen.get_cell_at(82, 81).goes_to = (
        mas.khonkaen,
        906 - mothermap.daughtermaps["khonkaen"].x,
        632 - mothermap.daughtermaps["khonkaen"].y,
    )
    mas.khonkaen.get_cell_at(8, 20).goes_to = (
        mas.chumphae_khonkaen,
        905 - mothermap.daughtermaps["chumphae_khonkaen"].x,
        631 - mothermap.daughtermaps["chumphae_khonkaen"].y,
    )
    mas.khonkaen.get_cell_at(8, 21).goes_to = (
        mas.chumphae_khonkaen,
        905 - mothermap.daughtermaps["chumphae_khonkaen"].x,
        632 - mothermap.daughtermaps["chumphae_khonkaen"].y,
    )
    mas.inn_khonkaen.get_cell_at(4, 8).goes_to = (
        mas.khonkaen,
        916 - mothermap.daughtermaps["khonkaen"].x,
        631 - mothermap.daughtermaps["khonkaen"].y,
    )
    mas.khonkaen.get_cell_at(
        916 - mothermap.daughtermaps["khonkaen"].x,
        630 - mothermap.daughtermaps["khonkaen"].y,
    ).goes_to = (mas.inn_khonkaen, 4, 7)

    # Buengsamphan
    mas.buengsamphan_chaiyaphum.get_cell_at(73, 32).goes_to = (
        mas.chaiyaphum,
        792 - mothermap.daughtermaps["chaiyaphum"].x,
        721 - mothermap.daughtermaps["chaiyaphum"].y,
    )
    mas.buengsamphan_chaiyaphum.get_cell_at(73, 33).goes_to = (
        mas.chaiyaphum,
        792 - mothermap.daughtermaps["chaiyaphum"].x,
        722 - mothermap.daughtermaps["chaiyaphum"].y,
    )
    mas.buengsamphan_chaiyaphum.get_cell_at(7, 32).goes_to = (
        mas.buengsamphan,
        726 - mothermap.daughtermaps["buengsamphan"].x,
        721 - mothermap.daughtermaps["buengsamphan"].y,
    )
    mas.buengsamphan_chaiyaphum.get_cell_at(7, 33).goes_to = (
        mas.buengsamphan,
        726 - mothermap.daughtermaps["buengsamphan"].x,
        722 - mothermap.daughtermaps["buengsamphan"].y,
    )


    mas.chaiyaphum.get_cell_at(12, 87).goes_to = (
        mas.buengsamphan_chaiyaphum_cave,
        15,
        14,
    )
    mas.buengsamphan_chaiyaphum_cave.get_cell_at(15, 15).goes_to = (
        mas.chaiyaphum,
        12,
        88,
    )
    mas.buengsamphan_chaiyaphum_cave.get_cell_at(8, 12).goes_to = (
        mas.buengsamphan_chaiyaphum,
        66,
        25,
    )
    mas.buengsamphan_chaiyaphum.get_cell_at(66, 24).goes_to = (
        mas.buengsamphan_chaiyaphum_cave,
        8,
        11,
    )




    mas.buengsamphan.get_cell_at(20, 22).goes_to = (mas.inn_buengsamphan, 4, 7)
    mas.inn_buengsamphan.get_cell_at(4, 8).goes_to = (
        mas.buengsamphan,
        670 - mothermap.daughtermaps["buengsamphan"].x,
        725 - mothermap.daughtermaps["buengsamphan"].y,
    )
    mas.buengsamphan.get_cell_at(61, 6).goes_to = (mas.buengsamphan_cave, 10, 21)
    mas.buengsamphan_cave.get_cell_at(10, 22).goes_to = (mas.buengsamphan, 61, 7)
    mas.buengsamphan_cave.get_cell_at(17, 17).goes_to = (
        mas.buengsamphan_mountain,
        718 - mothermap.daughtermaps["buengsamphan_mountain"].x,
        704 - mothermap.daughtermaps["buengsamphan_mountain"].y,
    )
    mas.buengsamphan_cave.get_cell_at(3, 10).goes_to = (
        mas.buengsamphan_mountain,
        704 - mothermap.daughtermaps["buengsamphan_mountain"].x,
        697 - mothermap.daughtermaps["buengsamphan_mountain"].y,
    )
    mas.buengsamphan_cave.get_cell_at(35, 10).goes_to = (
        mas.buengsamphan_mountain,
        736 - mothermap.daughtermaps["buengsamphan_mountain"].x,
        697 - mothermap.daughtermaps["buengsamphan_mountain"].y,
    )
    mas.buengsamphan_mountain.get_cell_at(7, 7).goes_to = (
        mas.buengsamphan_cave,
        3,
        9,
    )
    mas.buengsamphan_mountain.get_cell_at(21, 14).goes_to = (
        mas.buengsamphan_cave,
        17,
        16,
    )
    mas.buengsamphan_mountain.get_cell_at(39, 7).goes_to = (
        mas.buengsamphan_cave,
        35,
        9,
    )

    # Banyaeng
    mas.banyaeng.get_cell_at(45, 6).goes_to = (mas.bat_cave, 9, 15)
    mas.bat_cave.get_cell_at(9, 16).goes_to = (mas.banyaeng, 45, 7)
    mas.banyaeng.get_cell_at(36, 12).goes_to = (mas.inn_banyaeng, 4, 7)
    mas.inn_banyaeng.get_cell_at(4, 8).goes_to = (mas.banyaeng, 36, 13)

    mas.chumsaeng.get_cell_at(
        553 - mothermap.daughtermaps["chumsaeng"].x,
        714 - mothermap.daughtermaps["chumsaeng"].y,
    ).goes_to = (
        mas.nakhon_sawan,
        553 - mothermap.daughtermaps["nakhon_sawan"].x,
        714 - mothermap.daughtermaps["nakhon_sawan"].y,
    )
    mas.nakhon_sawan.get_cell_at(
        553 - mothermap.daughtermaps["nakhon_sawan"].x,
        713 - mothermap.daughtermaps["nakhon_sawan"].y,
    ).goes_to = (
        mas.chumsaeng,
        553 - mothermap.daughtermaps["chumsaeng"].x,
        713 - mothermap.daughtermaps["chumsaeng"].y,
    )

    mas.chumsaeng.get_cell_at(30, 27).goes_to = (mas.inn_chumsaeng, 4, 7)
    mas.inn_chumsaeng.get_cell_at(4, 8).goes_to = (mas.chumsaeng, 30, 28)

    # Phitsanulok
    mas.phitsanulok.get_cell_at(38, 17).goes_to = (mas.inn_phitsanulok, 4, 7)
    mas.inn_phitsanulok.get_cell_at(4, 8).goes_to = (mas.phitsanulok, 38, 18)
    mas.phitsanulok.get_cell_at(26, 28).goes_to = (
        mas.phitsanulok_underground,
        6,
        4,
    )
    mas.phitsanulok.get_cell_at(40, 42).goes_to = (
        mas.phitsanulok_underground,
        20,
        18,
    )
    mas.phitsanulok.get_cell_at(24, 40).goes_to = (
        mas.phitsanulok_underground,
        4,
        16,
    )
    mas.phitsanulok_underground.get_cell_at(20, 19).goes_to = (
        mas.phitsanulok,
        40,
        43,
    )
    mas.phitsanulok_underground.get_cell_at(6, 5).goes_to = (
        mas.phitsanulok,
        26,
        29,
    )
    mas.phitsanulok_underground.get_cell_at(4, 17).goes_to = (
        mas.phitsanulok,
        24,
        41,
    )

    mas.nakhon_sawan.get_cell_at(57, 19).goes_to = (
        mas.nakhon_sawan_aquarium,
        13,
        24,
    )
    mas.nakhon_sawan_aquarium.get_cell_at(13, 25).goes_to = (
        mas.nakhon_sawan,
        57,
        20,
    )
    mas.nakhon_sawan.get_cell_at(32, 20).goes_to = (mas.inn_nakhon_sawan, 4, 7)
    mas.inn_nakhon_sawan.get_cell_at(4, 8).goes_to = (mas.nakhon_sawan, 32, 21)
    mas.banyaeng.get_cell_at(37, 55).goes_to = (mas.banyaeng_cave, 16, 10)
    mas.banyaeng.get_cell_at(27, 51).goes_to = (mas.banyaeng_cave, 6, 6)
    mas.banyaeng_cave.get_cell_at(6, 7).goes_to = (mas.banyaeng, 27, 52)
    mas.banyaeng_cave.get_cell_at(16, 11).goes_to = (mas.banyaeng, 37, 56)

    # Lomsak Labyrinth
    mas.lomsak_labyrinth.get_cell_at(48, 12).goes_to = (
        mas.lomsak_labyrinth_house_1,
        5,
        12,
    )
    mas.lomsak_labyrinth_house_1.get_cell_at(5, 13).goes_to = (
        mas.lomsak_labyrinth,
        48,
        13,
    )
    mas.lomsak_labyrinth.get_cell_at(49, 11).goes_to = (
        mas.lomsak_labyrinth_house_1,
        8,
        3,
    )
    mas.lomsak_labyrinth_house_1.get_cell_at(8, 2).goes_to = (
        mas.lomsak_labyrinth,
        49,
        10,
    )
    mas.lomsak_labyrinth.get_cell_at(33, 12).goes_to = (
        mas.lomsak_labyrinth_house_2,
        13,
        24,
    )
    mas.lomsak_labyrinth_house_2.get_cell_at(13, 25).goes_to = (
        mas.lomsak_labyrinth,
        33,
        13,
    )
    mas.lomsak_labyrinth.get_cell_at(25, 16).goes_to = (
        mas.lomsak_labyrinth_shop,
        5,
        12,
    )
    mas.lomsak_labyrinth_shop.get_cell_at(5, 13).goes_to = (
        mas.lomsak_labyrinth,
        25,
        17,
    )

    # Labyrinth
    mas.labyrinth.get_cell_at(21, 21).goes_to = (mas.labyrinth_shop, 5, 12)
    mas.labyrinth_shop.get_cell_at(5, 13).goes_to = (mas.labyrinth, 21, 22)

    # Banyaeng
    mas.banyaeng.get_cell_at(17, 49).goes_to = (mas.banyaeng_house_1, 5, 12)
    mas.banyaeng_house_1.get_cell_at(5, 13).goes_to = (mas.banyaeng, 17, 50)
    mas.banyaeng.get_cell_at(20, 55).goes_to = (mas.banyaeng_house_2, 5, 12)
    mas.banyaeng_house_2.get_cell_at(5, 13).goes_to = (mas.banyaeng, 20, 56)
    mas.banyaeng.get_cell_at(41, 12).goes_to = (mas.banyaeng_school, 13, 24)
    mas.banyaeng_school.get_cell_at(13, 25).goes_to = (mas.banyaeng, 41, 13)
    mas.banyaeng.get_cell_at(37, 6).goes_to = (mas.banyaeng_temple, 13, 24)
    mas.banyaeng_temple.get_cell_at(13, 25).goes_to = (mas.banyaeng, 37, 7)
    mas.banyaeng.get_cell_at(39, 5).goes_to = (mas.banyaeng_temple, 17, 21)
    mas.banyaeng_temple.get_cell_at(18, 21).goes_to = (mas.banyaeng, 40, 5)
    mas.banyaeng.get_cell_at(31, 9).goes_to = (mas.banyaeng_house_3, 5, 12)
    mas.banyaeng_house_3.get_cell_at(5, 13).goes_to = (mas.banyaeng, 31, 10)

    mas.chumphae_kasetsombum_cave.get_cell_at(18, 14).goes_to = (
        mas.kasetsombum,
        34,
        15,
    )
    mas.kasetsombum.get_cell_at(34, 14).goes_to = (
        mas.chumphae_kasetsombum_cave,
        18,
        13,
    )
    mas.kasetsombum.get_cell_at(8, 8).goes_to = (mas.kasetsombum_cave, 15, 9)
    mas.kasetsombum_cave.get_cell_at(15, 10).goes_to = (mas.kasetsombum, 8, 9)
    mas.kasetsombum_cave.get_cell_at(5, 4).goes_to = (
        mas.kasetsombum_temple,
        11,
        14,
    )
    mas.kasetsombum_temple.get_cell_at(11, 13).goes_to = (
        mas.kasetsombum_cave,
        5,
        3,
    )
    mas.kasetsombum.get_cell_at(17, 19).goes_to = (mas.inn_kasetsombum, 4, 7)
    mas.inn_kasetsombum.get_cell_at(4, 8).goes_to = (mas.kasetsombum, 17, 20)
    mas.kasetsombum_temple.get_cell_at(30, 8).goes_to = (
        mas.kasetsombum_temple_temple,
        13,
        24,
    )
    mas.kasetsombum_temple_temple.get_cell_at(13, 25).goes_to = (
        mas.kasetsombum_temple,
        30,
        9,
    )

    mas.kasetsombum.get_cell_at(15, 10).goes_to = (mas.kasetsombum_house1, 7, 12)
    mas.kasetsombum_house1.get_cell_at(7, 13).goes_to = (mas.kasetsombum, 15, 11)
    mas.kasetsombum.get_cell_at(22, 20).goes_to = (mas.kasetsombum_house2, 7, 12)
    mas.kasetsombum_house2.get_cell_at(7, 13).goes_to = (mas.kasetsombum, 22, 21)
    mas.kasetsombum.get_cell_at(25, 15).goes_to = (mas.kasetsombum_house3, 5, 12)
    mas.kasetsombum_house3.get_cell_at(5, 13).goes_to = (mas.kasetsombum, 25, 16)
    mas.kasetsombum.get_cell_at(12, 18).goes_to = (mas.kasetsombum_school, 13, 24)
    mas.kasetsombum_school.get_cell_at(13, 25).goes_to = (mas.kasetsombum, 12, 19)
    mas.kasetsombum.get_cell_at(20, 14).goes_to = (mas.kasetsombum_shop, 5, 12)
    mas.kasetsombum_shop.get_cell_at(5, 13).goes_to = (mas.kasetsombum, 20, 15)

    mas.buengsamphan.get_cell_at(78, 19).goes_to = (
        mas.buengsamphan_chaiyaphum,
        728 - mothermap.daughtermaps["buengsamphan_chaiyaphum"].x,
        721 - mothermap.daughtermaps["buengsamphan_chaiyaphum"].y,
    )
    mas.buengsamphan.get_cell_at(78, 20).goes_to = (
        mas.buengsamphan_chaiyaphum,
        728 - mothermap.daughtermaps["buengsamphan_chaiyaphum"].x,
        722 - mothermap.daughtermaps["buengsamphan_chaiyaphum"].y,
    )
    mas.chaiyaphum.get_cell_at(11, 92).goes_to = (
        mas.buengsamphan_chaiyaphum,
        791 - mothermap.daughtermaps["buengsamphan_chaiyaphum"].x,
        721 - mothermap.daughtermaps["buengsamphan_chaiyaphum"].y,
    )
    mas.chaiyaphum.get_cell_at(11, 93).goes_to = (
        mas.buengsamphan_chaiyaphum,
        791 - mothermap.daughtermaps["buengsamphan_chaiyaphum"].x,
        722 - mothermap.daughtermaps["buengsamphan_chaiyaphum"].y,
    )

    mas.phitsanulok.get_cell_at(37, 49).goes_to = (
        mas.phitsanulok_maths_school_123,
        13,
        24,
    )
    mas.phitsanulok_maths_school_123.get_cell_at(13, 25).goes_to = (
        mas.phitsanulok,
        37,
        50,
    )
    mas.phitsanulok_maths_school_123.get_cell_at(13, 17).goes_to = (
        mas.phitsanulok_maths_school_123,
        3,
        9,
    )
    mas.phitsanulok_maths_school_123.get_cell_at(3, 10).goes_to = (
        mas.phitsanulok_maths_school_123,
        13,
        18,
    )
    mas.phitsanulok_maths_school_123.get_cell_at(3, 1).goes_to = (
        mas.phitsanulok_maths_school_123,
        14,
        9,
    )
    mas.phitsanulok_maths_school_123.get_cell_at(14, 10).goes_to = (
        mas.phitsanulok_maths_school_123,
        3,
        2,
    )

    mas.phitsanulok_maths_school_123.get_cell_at(25, 9).goes_to = (
        mas.phitsanulok_maths_school_456,
        18,
        25,
    )
    mas.phitsanulok_maths_school_456.get_cell_at(18, 27).goes_to = (
        mas.phitsanulok_maths_school_123,
        25,
        10,
    )

    mas.phitsanulok_maths_school_456.get_cell_at(31, 26).goes_to = (
        mas.phitsanulok_maths_school_456,
        10,
        22,
    )
    mas.phitsanulok_maths_school_456.get_cell_at(9, 22).goes_to = (
        mas.phitsanulok_maths_school_456,
        30,
        26,
    )
    mas.phitsanulok_maths_school_456.get_cell_at(22, 21).goes_to = (
        mas.phitsanulok_maths_school_456,
        5,
        9,
    )
    mas.phitsanulok_maths_school_456.get_cell_at(5, 10).goes_to = (
        mas.phitsanulok_maths_school_456,
        22,
        22,
    )
    mas.phitsanulok_maths_school_456.get_cell_at(5, 4).goes_to = (
        mas.phitsanulok_maths_school_456,
        35,
        12,
    )
    mas.phitsanulok_maths_school_456.get_cell_at(35, 13).goes_to = (
        mas.phitsanulok_maths_school_456,
        5,
        5,
    )

    mas.phitsanulok_maths_school_456.get_cell_at(35, 1).goes_to = (
        mas.phitsanulok_maths_school_789,
        18,
        26,
    )
    mas.phitsanulok_maths_school_789.get_cell_at(18, 27).goes_to = (
        mas.phitsanulok_maths_school_456,
        35,
        2,
    )

    mas.phitsanulok_maths_school_789.get_cell_at(18, 19).goes_to = (
        mas.phitsanulok_maths_school_789,
        7,
        11,
    )
    mas.phitsanulok_maths_school_789.get_cell_at(7, 12).goes_to = (
        mas.phitsanulok_maths_school_789,
        18,
        20,
    )

    mas.phitsanulok_maths_school_789.get_cell_at(7, 0).goes_to = (
        mas.phitsanulok_maths_school_789,
        35,
        11,
    )
    mas.phitsanulok_maths_school_789.get_cell_at(35, 12).goes_to = (
        mas.phitsanulok_maths_school_789,
        7,
        1,
    )

    mas.phitsanulok_maths_school_789.get_cell_at(29, 26).goes_to = (
        mas.phitsanulok_maths_school_789,
        8,
        26,
    )
    mas.phitsanulok_maths_school_789.get_cell_at(7, 26).goes_to = (
        mas.phitsanulok_maths_school_789,
        28,
        26,
    )
    mas.phitsanulok_maths_school_789.get_cell_at(29, 23).goes_to = (
        mas.phitsanulok_maths_school_789,
        8,
        23,
    )
    mas.phitsanulok_maths_school_789.get_cell_at(7, 23).goes_to = (
        mas.phitsanulok_maths_school_789,
        28,
        23,
    )
    mas.phitsanulok_maths_school_789.get_cell_at(29, 20).goes_to = (
        mas.phitsanulok_maths_school_789,
        8,
        20,
    )
    mas.phitsanulok_maths_school_789.get_cell_at(7, 20).goes_to = (
        mas.phitsanulok_maths_school_789,
        28,
        20,
    )

    mas.phitsanulok.get_cell_at(7, 10).goes_to = (
        mas.phitsanulok_sukhothai,
        537 - mothermap.daughtermaps["phitsanulok_sukhothai"].x,
        555 - mothermap.daughtermaps["phitsanulok_sukhothai"].y,
    )
    mas.phitsanulok.get_cell_at(7, 9).goes_to = (
        mas.phitsanulok_sukhothai,
        537 - mothermap.daughtermaps["phitsanulok_sukhothai"].x,
        554 - mothermap.daughtermaps["phitsanulok_sukhothai"].y,
    )
    mas.phitsanulok_sukhothai.get_cell_at(46, 15).goes_to = (
        mas.phitsanulok,
        9,
        10,
    )
    mas.phitsanulok_sukhothai.get_cell_at(46, 14).goes_to = (
        mas.phitsanulok,
        9,
        9,
    )

    mas.phitsanulok_sukhothai.get_cell_at(11, 4).goes_to = (
        mas.sukhothai,
        504 - mothermap.daughtermaps["sukhothai"].x,
        544 - mothermap.daughtermaps["sukhothai"].y,
    )
    mas.phitsanulok_sukhothai.get_cell_at(12, 4).goes_to = (
        mas.sukhothai,
        505 - mothermap.daughtermaps["sukhothai"].x,
        544 - mothermap.daughtermaps["sukhothai"].y,
    )
    mas.sukhothai.get_cell_at(36, 32).goes_to = (mas.phitsanulok_sukhothai, 11, 5)
    mas.sukhothai.get_cell_at(37, 32).goes_to = (mas.phitsanulok_sukhothai, 12, 5)

    mas.sukhothai.get_cell_at(7, 17).goes_to = (
        mas.old_sukhothai,
        475 - mothermap.daughtermaps["old_sukhothai"].x,
        530 - mothermap.daughtermaps["old_sukhothai"].y,
    )
    mas.sukhothai.get_cell_at(7, 18).goes_to = (
        mas.old_sukhothai,
        475 - mothermap.daughtermaps["old_sukhothai"].x,
        531 - mothermap.daughtermaps["old_sukhothai"].y,
    )
    mas.old_sukhothai.get_cell_at(47, 16).goes_to = (mas.sukhothai, 8, 17)
    mas.old_sukhothai.get_cell_at(47, 17).goes_to = (mas.sukhothai, 8, 18)

    mas.chumphae_khonkaen.get_cell_at(7, 37).goes_to = (mas.chumphae, 132, 25)
    mas.chumphae.get_cell_at(133, 25).goes_to = (mas.chumphae_khonkaen, 8, 37)

    # chatturat
    mas.buengsamphan_chaiyaphum.get_cell_at(66, 37).goes_to = (
        mas.chaiyaphum_chatturat,
        35,
        11,
    )
    mas.chaiyaphum_chatturat.get_cell_at(36, 11).goes_to = (
        mas.buengsamphan_chaiyaphum,
        67,
        37,
    )
    mas.chaiyaphum_chatturat.get_cell_at(24, 11).goes_to = (
        mas.buengsamphan_chaiyaphum,
        55,
        37,
    )
    mas.buengsamphan_chaiyaphum.get_cell_at(56, 37).goes_to = (
        mas.chaiyaphum_chatturat,
        25,
        11,
    )

    mas.chaiyaphum_chatturat.get_cell_at(28, 52).goes_to = (mas.chatturat, 74, 5)
    mas.chatturat.get_cell_at(74, 4).goes_to = (mas.chaiyaphum_chatturat, 28, 51)

    mas.chatturat.get_cell_at(66, 14).goes_to = (mas.inn_chatturat, 4, 7)
    mas.inn_chatturat.get_cell_at(4, 8).goes_to = (mas.chatturat, 66, 15)

    mas.chatturat.get_cell_at(67, 34).goes_to = (mas.chatturat_sikhiu, 55, 6)
    mas.chatturat.get_cell_at(68, 34).goes_to = (mas.chatturat_sikhiu, 56, 6)
    mas.chatturat_sikhiu.get_cell_at(55, 5).goes_to = (mas.chatturat, 67, 33)
    mas.chatturat_sikhiu.get_cell_at(56, 5).goes_to = (mas.chatturat, 68, 33)

    mas.chatturat_sikhiu.get_cell_at(32, 58).goes_to = (mas.sikhiu, 44, 11)
    mas.chatturat_sikhiu.get_cell_at(33, 58).goes_to = (mas.sikhiu, 45, 11)
    mas.sikhiu.get_cell_at(44, 10).goes_to = (mas.chatturat_sikhiu, 32, 57)
    mas.sikhiu.get_cell_at(45, 10).goes_to = (mas.chatturat_sikhiu, 33, 57)

    mas.ko_kut.get_cell_at(54, 57).goes_to = (mas.plane, 5, 5)
    mas.plane.get_cell_at(7, 0).goes_to = (mas.ko_kut, 56, 55)
