import time
import pygame

from lexicon.items import Words
from mechanics.minimap import Minimap, want_to_launch_map

import os

from profile.profile import save

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)


def npc_sprites():
    # TODO Alexis
    # This should be done automatically
    return {
        "sign": pygame.image.load(f"{dir_path}/../npc/sprites/sign.png"),
        "seed": pygame.image.load(f"{dir_path}/../npc/sprites/seed.png"),
        "bed": pygame.image.load(f"{dir_path}/../npc/sprites/bed.png"),
        "mom_up": pygame.image.load(f"{dir_path}/../npc/sprites/mom_up.png"),
        "mom_down": pygame.image.load(f"{dir_path}/../npc/sprites/mom_down.png"),
        "dad_down": pygame.image.load(f"{dir_path}/../npc/sprites/dad_down.png"),
        "dad_up": pygame.image.load(f"{dir_path}/../npc/sprites/dad_up.png"),
        "dad_right": pygame.image.load(f"{dir_path}/../npc/sprites/dad_right.png"),
        "dad_left": pygame.image.load(f"{dir_path}/../npc/sprites/dad_left.png"),
        "mom_right": pygame.image.load(f"{dir_path}/../npc/sprites/mom_right.png"),
        "mom_left": pygame.image.load(f"{dir_path}/../npc/sprites/mom_left.png"),
        "mali_down": pygame.image.load(f"{dir_path}/../npc/sprites/mali_down.png"),
        "mali_up": pygame.image.load(f"{dir_path}/../npc/sprites/mali_up.png"),
        "mali_right": pygame.image.load(f"{dir_path}/../npc/sprites/mali_right.png"),
        "mali_left": pygame.image.load(f"{dir_path}/../npc/sprites/mali_left.png"),
        "policeman_down": pygame.image.load(f"{dir_path}/../npc/sprites/policeman_down.png"),
        # "policeman_up": pygame.image.load(f"{dir_path}/../npc/sprites/policeman_up.png"),
        "policeman_right": pygame.image.load(f"{dir_path}/../npc/sprites/policeman_right.png"),
        "policeman_left": pygame.image.load(f"{dir_path}/../npc/sprites/policeman_left.png"),
        "old_man_left": pygame.image.load(
            f"{dir_path}/../npc/sprites/old_man_left.png"
        ),
        "old_man_right": pygame.image.load(
            f"{dir_path}/../npc/sprites/old_man_right.png"
        ),
        "old_man_down": pygame.image.load(
            f"{dir_path}/../npc/sprites/old_man_down.png"
        ),
        "old_man_up": pygame.image.load(f"{dir_path}/../npc/sprites/old_man_up.png"),
        "old_woman_left": pygame.image.load(
            f"{dir_path}/../npc/sprites/old_woman_left.png"
        ),
        "old_woman_right": pygame.image.load(
            f"{dir_path}/../npc/sprites/old_woman_right.png"
        ),
        "old_woman_down": pygame.image.load(
            f"{dir_path}/../npc/sprites/old_woman_down.png"
        ),
        "old_woman_up": pygame.image.load(
            f"{dir_path}/../npc/sprites/old_woman_up.png"
        ),
        "fat_vendor_down": pygame.image.load(
            f"{dir_path}/../npc/sprites/fat_vendor_down.png"
        ),
        "vendor_down": pygame.image.load(f"{dir_path}/../npc/sprites/vendor_down.png"),
        "vendor_up": pygame.image.load(f"{dir_path}/../npc/sprites/vendor_up.png"),
        "vendor_right": pygame.image.load(
            f"{dir_path}/../npc/sprites/vendor_right.png"
        ),
        "vendor_left": pygame.image.load(f"{dir_path}/../npc/sprites/vendor_left.png"),
        "cat_up": pygame.image.load(f"{dir_path}/../npc/sprites/cat_up.png"),
        "cat_down": pygame.image.load(f"{dir_path}/../npc/sprites/cat_down.png"),
        "cat_right": pygame.image.load(f"{dir_path}/../npc/sprites/cat_right.png"),
        "cat_left": pygame.image.load(f"{dir_path}/../npc/sprites/cat_left.png"),
        "celine_down": pygame.image.load(f"{dir_path}/../npc/sprites/celine_down.png"),
        "celine_up": pygame.image.load(f"{dir_path}/../npc/sprites/celine_up.png"),
        "celine_right": pygame.image.load(
            f"{dir_path}/../npc/sprites/celine_right.png"
        ),
        "celine_left": pygame.image.load(f"{dir_path}/../npc/sprites/celine_left.png"),
        "alexis_down": pygame.image.load(f"{dir_path}/../npc/sprites/alexis_down.png"),
        "alexis_up": pygame.image.load(f"{dir_path}/../npc/sprites/alexis_up.png"),
        "alexis_right": pygame.image.load(
            f"{dir_path}/../npc/sprites/alexis_right.png"
        ),
        "alexis_left": pygame.image.load(f"{dir_path}/../npc/sprites/alexis_left.png"),
        "rob_down": pygame.image.load(f"{dir_path}/../npc/sprites/rob_down.png"),
        "rob_up": pygame.image.load(f"{dir_path}/../npc/sprites/rob_up.png"),
        "rob_right": pygame.image.load(f"{dir_path}/../npc/sprites/rob_right.png"),
        "rob_left": pygame.image.load(f"{dir_path}/../npc/sprites/rob_left.png"),
        "ed_down": pygame.image.load(f"{dir_path}/../npc/sprites/ed_down.png"),
        "ed_up": pygame.image.load(f"{dir_path}/../npc/sprites/ed_up.png"),
        "ed_right": pygame.image.load(f"{dir_path}/../npc/sprites/ed_right.png"),
        "ed_left": pygame.image.load(f"{dir_path}/../npc/sprites/ed_left.png"),
        "kid_up": pygame.image.load(f"{dir_path}/../npc/sprites/kid_up.png"),
        "kid_down": pygame.image.load(f"{dir_path}/../npc/sprites/kid_down.png"),
        "kid_right": pygame.image.load(f"{dir_path}/../npc/sprites/kid_right.png"),
        "kid_left": pygame.image.load(f"{dir_path}/../npc/sprites/kid_left.png"),
        "lass_up": pygame.image.load(f"{dir_path}/../npc/sprites/lass_up.png"),
        "ghost_down": pygame.image.load(f"{dir_path}/../npc/sprites/ghost_down.png"),
        "lass_down": pygame.image.load(f"{dir_path}/../npc/sprites/lass_down.png"),
        "lass_right": pygame.image.load(f"{dir_path}/../npc/sprites/lass_right.png"),
        "lass_left": pygame.image.load(f"{dir_path}/../npc/sprites/lass_left.png"),
        "dog_up": pygame.image.load(f"{dir_path}/../npc/sprites/dog_up.png"),
        "dog_down": pygame.image.load(f"{dir_path}/../npc/sprites/dog_down.png"),
        "dog_right": pygame.image.load(f"{dir_path}/../npc/sprites/dog_right.png"),
        "dog_left": pygame.image.load(f"{dir_path}/../npc/sprites/dog_left.png"),
        "clown_fish_left": pygame.image.load(
            f"{dir_path}/../npc/sprites/clown_fish_left.png"
        ),
        "clown_fish_right": pygame.image.load(
            f"{dir_path}/../npc/sprites/clown_fish_right.png"
        ),
        "nurse_down": pygame.image.load(f"{dir_path}/../npc/sprites/nurse_down.png"),
        "monk_down": pygame.image.load(f"{dir_path}/../npc/sprites/monk_down.png"),
        "monk_up": pygame.image.load(f"{dir_path}/../npc/sprites/monk_up.png"),
        "monk_right": pygame.image.load(f"{dir_path}/../npc/sprites/monk_right.png"),
        "monk_left": pygame.image.load(f"{dir_path}/../npc/sprites/monk_left.png"),
        "fisherman_down": pygame.image.load(f"{dir_path}/../npc/sprites/fisherman_down.png"),
        "fisherman_up": pygame.image.load(f"{dir_path}/../npc/sprites/fisherman_up.png"),
        "fisherman_right": pygame.image.load(f"{dir_path}/../npc/sprites/fisherman_right.png"),
        "fisherman_left": pygame.image.load(f"{dir_path}/../npc/sprites/fisherman_left.png"),
        "fishing_boat_down": pygame.image.load(f"{dir_path}/../npc/sprites/fishing_boat_down.png"),
        "fishing_boat_up": pygame.image.load(f"{dir_path}/../npc/sprites/fishing_boat_up.png"),
        "fishing_boat_right": pygame.image.load(f"{dir_path}/../npc/sprites/fishing_boat_right.png"),
        "fishing_boat_left": pygame.image.load(f"{dir_path}/../npc/sprites/fishing_boat_left.png"),
        "small_fishing_boat_down": pygame.image.load(f"{dir_path}/../npc/sprites/small_fishing_boat_down.png"),
        "small_fishing_boat_up": pygame.image.load(f"{dir_path}/../npc/sprites/small_fishing_boat_up.png"),
        "small_fishing_boat_right": pygame.image.load(f"{dir_path}/../npc/sprites/small_fishing_boat_right.png"),
        "small_fishing_boat_left": pygame.image.load(f"{dir_path}/../npc/sprites/small_fishing_boat_left.png"),
        "monk_levitating_up": pygame.image.load(
            f"{dir_path}/../npc/sprites/monk_levitating_up.png"
        ),
        "monk_levitating_right": pygame.image.load(
            f"{dir_path}/../npc/sprites/monk_levitating_right.png"
        ),
        "monk_levitating_left": pygame.image.load(
            f"{dir_path}/../npc/sprites/monk_levitating_left.png"
        ),
        "monk_levitating_down": pygame.image.load(
            f"{dir_path}/../npc/sprites/monk_levitating_down.png"
        ),
        "monkey_down": pygame.image.load(f"{dir_path}/../npc/sprites/monkey_down.png"),
        "monkey_up": pygame.image.load(f"{dir_path}/../npc/sprites/monkey_up.png"),
        "monkey_right": pygame.image.load(
            f"{dir_path}/../npc/sprites/monkey_right.png"
        ),
        "monkey_left": pygame.image.load(f"{dir_path}/../npc/sprites/monkey_left.png"),
        "gecko_down": pygame.image.load(f"{dir_path}/../npc/sprites/gecko_down.png"),
        "gecko_up": pygame.image.load(f"{dir_path}/../npc/sprites/gecko_up.png"),
        "gecko_right": pygame.image.load(f"{dir_path}/../npc/sprites/gecko_right.png"),
        "gecko_left": pygame.image.load(f"{dir_path}/../npc/sprites/gecko_left.png"),
        "leopard_gecko_down": pygame.image.load(
            f"{dir_path}/../npc/sprites/leopard_gecko_down.png"
        ),
        "leopard_gecko_up": pygame.image.load(
            f"{dir_path}/../npc/sprites/leopard_gecko_up.png"
        ),
        "leopard_gecko_right": pygame.image.load(
            f"{dir_path}/../npc/sprites/leopard_gecko_right.png"
        ),
        "leopard_gecko_left": pygame.image.load(
            f"{dir_path}/../npc/sprites/leopard_gecko_left.png"
        ),
        "hawk_down": pygame.image.load(f"{dir_path}/../npc/sprites/hawk_down.png"),
        "hawk_up": pygame.image.load(f"{dir_path}/../npc/sprites/hawk_up.png"),
        "hawk_right": pygame.image.load(f"{dir_path}/../npc/sprites/hawk_right.png"),
        "hawk_left": pygame.image.load(f"{dir_path}/../npc/sprites/hawk_left.png"),
        "jetski_down": pygame.image.load(f"{dir_path}/../npc/sprites/jetski_down.png"),
        "jetski_up": pygame.image.load(f"{dir_path}/../npc/sprites/jetski_up.png"),
        "nun_down": pygame.image.load(f"{dir_path}/../npc/sprites/nun_down.png"),
        "nun_up": pygame.image.load(f"{dir_path}/../npc/sprites/nun_up.png"),
        "jetski_right": pygame.image.load(
            f"{dir_path}/../npc/sprites/jetski_right.png"
        ),
        "jetski_left": pygame.image.load(f"{dir_path}/../npc/sprites/jetski_left.png"),
        "crocodile_down": pygame.image.load(
            f"{dir_path}/../npc/sprites/crocodile_down.png"
        ),
        "crocodile_up": pygame.image.load(
            f"{dir_path}/../npc/sprites/crocodile_up.png"
        ),
        "crocodile_right": pygame.image.load(
            f"{dir_path}/../npc/sprites/crocodile_right.png"
        ),
        "crocodile_left": pygame.image.load(
            f"{dir_path}/../npc/sprites/crocodile_left.png"
        ),
        "rich_woman_left": pygame.image.load(
            f"{dir_path}/../npc/sprites/rich_woman_left.png"
        ),
        "rich_woman_right": pygame.image.load(
            f"{dir_path}/../npc/sprites/rich_woman_right.png"
        ),
        "rich_woman_up": pygame.image.load(
            f"{dir_path}/../npc/sprites/rich_woman_up.png"
        ),
        "rich_woman_down": pygame.image.load(
            f"{dir_path}/../npc/sprites/rich_woman_down.png"
        ),
        "woman_left": pygame.image.load(f"{dir_path}/../npc/sprites/woman_left.png"),
        "woman_right": pygame.image.load(f"{dir_path}/../npc/sprites/woman_right.png"),
        "woman_up": pygame.image.load(f"{dir_path}/../npc/sprites/woman_up.png"),
        "woman_down": pygame.image.load(f"{dir_path}/../npc/sprites/woman_down.png"),
        "boat": pygame.image.load(f"{dir_path}/../npc/sprites/boat.png"),
        "chest_closed": pygame.image.load(
            f"{dir_path}/../npc/sprites/chest_closed_down.png"
        ),
        "chest_open": pygame.image.load(
            f"{dir_path}/../npc/sprites/chest_open_down.png"
        ),
        "black_spell": pygame.image.load(f"{dir_path}/../npc/sprites/black_spell.png"),
        "white_spell": pygame.image.load(f"{dir_path}/../npc/sprites/white_spell.png"),
        "red_spell": pygame.image.load(f"{dir_path}/../npc/sprites/red_spell.png"),
        "green_spell": pygame.image.load(f"{dir_path}/../npc/sprites/green_spell.png"),
        "grey_spell": pygame.image.load(f"{dir_path}/../npc/sprites/grey_spell.png"),
        "yellow_spell": pygame.image.load(f"{dir_path}/../npc/sprites/yellow_spell.png"),
        "purple_spell": pygame.image.load(f"{dir_path}/../npc/sprites/purple_spell.png"),
        "teal_spell": pygame.image.load(f"{dir_path}/../npc/sprites/teal_spell.png"),
        "blue_spell": pygame.image.load(f"{dir_path}/../npc/sprites/blue_spell.png"),
        "spell_blue_half": pygame.image.load(f"{dir_path}/../npc/sprites/spell_blue_half.png"),
        "spirit_bird": pygame.image.load(f"{dir_path}/../npc/sprites/spirit_bird.png"),
        "spirit_bird_invisible": pygame.image.load(f"{dir_path}/../npc/sprites/spirit_bird_invisible.png"),
        "spirit_gecko": pygame.image.load(f"{dir_path}/../npc/sprites/spirit_gecko.png"),
        "spirit_gecko_invisible": pygame.image.load(f"{dir_path}/../npc/sprites/spirit_gecko_invisible.png"),
        "garbage_0": pygame.image.load(f"{dir_path}/../npc/sprites/garbage_0.png"),
        "garbage_1": pygame.image.load(f"{dir_path}/../npc/sprites/garbage_1.png"),
        "garbage_2": pygame.image.load(f"{dir_path}/../npc/sprites/garbage_2.png"),
        "garbage_3": pygame.image.load(f"{dir_path}/../npc/sprites/garbage_3.png"),
        "television_off": pygame.image.load(
            f"{dir_path}/../npc/sprites/television_off.png"
        ),
        "_television_on_1": pygame.image.load(
            f"{dir_path}/../npc/sprites/television_on_1.png"
        ),
        "_television_on_2": pygame.image.load(
            f"{dir_path}/../npc/sprites/television_on_2.png"
        ),
        "_television_on_3": pygame.image.load(
            f"{dir_path}/../npc/sprites/television_on_3.png"
        ),
        "_television_on_4": pygame.image.load(
            f"{dir_path}/../npc/sprites/television_on_4.png"
        ),
        "_crashed_plane_1": pygame.image.load(
            f"{dir_path}/../npc/sprites/crashed_plane_0.png"
        ),
        "_crashed_plane_2": pygame.image.load(
            f"{dir_path}/../npc/sprites/crashed_plane_1.png"
        ),
        "_crashed_plane_3": pygame.image.load(
            f"{dir_path}/../npc/sprites/crashed_plane_2.png"
        ),
        "_crashed_plane_4": pygame.image.load(
            f"{dir_path}/../npc/sprites/crashed_plane_3.png"
        ),
        "nim_down": pygame.image.load(f"{dir_path}/../npc/sprites/nim_down.png"),
        "nim_up": pygame.image.load(f"{dir_path}/../npc/sprites/nim_up.png"),
        "nim_right": pygame.image.load(f"{dir_path}/../npc/sprites/nim_right.png"),
        "nim_left": pygame.image.load(f"{dir_path}/../npc/sprites/nim_left.png"),
    }


def random_images():
    return {
        "check_mark": pygame.image.load(f"{dir_path}/../images/check_mark.png"),
        "selection_arrow": pygame.image.load(
            f"{dir_path}/../images/selection_arrow.png"
        ),
        "heart_0": pygame.image.load(f"{dir_path}/../images/heart_0.png"),
        "heart_1": pygame.image.load(f"{dir_path}/../images/heart_1.png"),
        "heart_2": pygame.image.load(f"{dir_path}/../images/heart_2.png"),
        "heart_3": pygame.image.load(f"{dir_path}/../images/heart_3.png"),
        "heart_4": pygame.image.load(f"{dir_path}/../images/heart_4.png"),
        "heart_5": pygame.image.load(f"{dir_path}/../images/heart_5.png"),
        "heart_6": pygame.image.load(f"{dir_path}/../images/heart_6.png"),
        "heart_7": pygame.image.load(f"{dir_path}/../images/heart_7.png"),
        "heart_8": pygame.image.load(f"{dir_path}/../images/heart_8.png"),
        "sound_icon": pygame.image.load(f"{dir_path}/../images/sound_icon.png"),
        "sound_icon_green": pygame.image.load(
            f"{dir_path}/../images/sound_icon_green.png"
        ),
        "exclamation_mark": pygame.image.load(
            f"{dir_path}/../images/exclamation_mark.png"
        ),
        "learning_mark": pygame.image.load(f"{dir_path}/../images/learning_mark.png"),
        "brain_0": pygame.image.load(f"{dir_path}/../images/brain_0.png"),
        "brain_1": pygame.image.load(f"{dir_path}/../images/brain_1.png"),
        "brain_2": pygame.image.load(f"{dir_path}/../images/brain_2.png"),
        "brain_3": pygame.image.load(f"{dir_path}/../images/brain_3.png"),
        "brain_4": pygame.image.load(f"{dir_path}/../images/brain_4.png"),
        "brain_5": pygame.image.load(f"{dir_path}/../images/brain_5.png"),
        "brain_6": pygame.image.load(f"{dir_path}/../images/brain_6.png"),
        "rain_drop_0": pygame.image.load(f"{dir_path}/../images/rain_drop_0.png"),
        "rain_drop_1": pygame.image.load(f"{dir_path}/../images/rain_drop_1.png"),
        "rain_drop_2": pygame.image.load(f"{dir_path}/../images/rain_drop_2.png"),
        "rain_drop_3": pygame.image.load(f"{dir_path}/../images/rain_drop_3.png"),
        "rising": pygame.image.load(f"{dir_path}/../images/rising.png"),
        "mid": pygame.image.load(f"{dir_path}/../images/mid.png"),
        "low": pygame.image.load(f"{dir_path}/../images/low.png"),
        "falling": pygame.image.load(f"{dir_path}/../images/falling.png"),
        "high": pygame.image.load(f"{dir_path}/../images/high.png"),
        "lightning_strike_0": pygame.image.load(f"{dir_path}/../images/lightning_strike_0.png"),
        "lightning_strike_1": pygame.image.load(f"{dir_path}/../images/lightning_strike_1.png"),
        "lightning_strike_2": pygame.image.load(f"{dir_path}/../images/lightning_strike_2.png"),
        "shift_keyboard": pygame.image.load(f"{dir_path}/../images/shift_keyboard.png"),
        "default_keyboard": pygame.image.load(f"{dir_path}/../images/default_keyboard.png"),
    }


def get_sprites():
    return {
        "_grass_1": pygame.image.load(f"{dir_path}/../ow/sprites/grass_1.bmp"),
        "_grass_2": pygame.image.load(f"{dir_path}/../ow/sprites/grass_2.bmp"),
        "_grass_3": pygame.image.load(f"{dir_path}/../ow/sprites/grass_1.bmp"),
        "_grass_4": pygame.image.load(f"{dir_path}/../ow/sprites/grass_4.bmp"),
        "path": pygame.image.load(f"{dir_path}/../ow/sprites/path.bmp"),
        "tree": pygame.image.load(f"{dir_path}/../ow/sprites/tree.bmp"),
        "big_tree": pygame.image.load(f"{dir_path}/../ow/sprites/big_tree.bmp"),
        "_waterfall_1": pygame.image.load(f"{dir_path}/../ow/sprites/waterfall1.bmp"),
        "_waterfall_2": pygame.image.load(f"{dir_path}/../ow/sprites/waterfall2.bmp"),
        "_waterfall_3": pygame.image.load(f"{dir_path}/../ow/sprites/waterfall3.bmp"),
        "_waterfall_4": pygame.image.load(f"{dir_path}/../ow/sprites/waterfall2.bmp"),
        "bridge_hor": pygame.image.load(f"{dir_path}/../ow/sprites/bridge_hor.bmp"),
        "bridge_ver": pygame.image.load(f"{dir_path}/../ow/sprites/bridge_ver.bmp"),
        "flower_3": pygame.image.load(f"{dir_path}/../ow/sprites/flower_3.bmp"),
        "flower_4": pygame.image.load(f"{dir_path}/../ow/sprites/flower_4.bmp"),
        "_flower_1_1": pygame.image.load(f"{dir_path}/../ow/sprites/flower_1_1.bmp"),
        "_flower_1_2": pygame.image.load(f"{dir_path}/../ow/sprites/flower_1_2.bmp"),
        "_flower_1_3": pygame.image.load(f"{dir_path}/../ow/sprites/flower_1_3.bmp"),
        "_flower_1_4": pygame.image.load(f"{dir_path}/../ow/sprites/flower_1_2.bmp"),
        "_flower_2_1": pygame.image.load(f"{dir_path}/../ow/sprites/flower_2_1.bmp"),
        "_flower_2_2": pygame.image.load(f"{dir_path}/../ow/sprites/flower_2_1.bmp"),
        "_flower_2_3": pygame.image.load(f"{dir_path}/../ow/sprites/flower_2_2.bmp"),
        "_flower_2_4": pygame.image.load(f"{dir_path}/../ow/sprites/flower_2_2.bmp"),
        "nenuphar": pygame.image.load(f"{dir_path}/../ow/sprites/nenuphar.bmp"),
        "door": pygame.image.load(f"{dir_path}/../ow/sprites/door.bmp"),
        "inn_floor": pygame.image.load(f"{dir_path}/../ow/sprites/inn_floor.bmp"),
        "temple_floor": pygame.image.load(f"{dir_path}/../ow/sprites/temple_floor.bmp"),
        "cave_floor": pygame.image.load(f"{dir_path}/../ow/sprites/cave_floor.bmp"),
        "cave_rock_pillar_1": pygame.image.load(
            f"{dir_path}/../ow/sprites/cave_rock_pillar_1.bmp"
        ),
        "boulder_2": pygame.image.load(f"{dir_path}/../ow/sprites/boulder_2.bmp"),
        "field_spirit_house": pygame.image.load(
            f"{dir_path}/../ow/sprites/field_spirit_house.bmp"
        ),
        "stairs_up": pygame.image.load(f"{dir_path}/../ow/sprites/stairs_up.bmp"),
        "stairs_down": pygame.image.load(f"{dir_path}/../ow/sprites/stairs_down.bmp"),
        "cave_0010": pygame.image.load(f"{dir_path}/../ow/sprites/cave_0010.bmp"),
        "cave_0110": pygame.image.load(f"{dir_path}/../ow/sprites/cave_0110.bmp"),
        "cave_0100": pygame.image.load(f"{dir_path}/../ow/sprites/cave_0100.bmp"),
        "cave_1100": pygame.image.load(f"{dir_path}/../ow/sprites/cave_1100.bmp"),
        "cave_1000": pygame.image.load(f"{dir_path}/../ow/sprites/cave_1000.bmp"),
        "cave_1001": pygame.image.load(f"{dir_path}/../ow/sprites/cave_1001.bmp"),
        "cave_0001": pygame.image.load(f"{dir_path}/../ow/sprites/cave_0001.bmp"),
        "cave_0011": pygame.image.load(f"{dir_path}/../ow/sprites/cave_0011.bmp"),
        "cave_1110": pygame.image.load(f"{dir_path}/../ow/sprites/cave_1110.bmp"),
        "cave_1101": pygame.image.load(f"{dir_path}/../ow/sprites/cave_1101.bmp"),
        "cave_entrance_down": pygame.image.load(
            f"{dir_path}/../ow/sprites/cave_entrance_down.bmp"
        ),
        "cave_stairs_1100": pygame.image.load(
            f"{dir_path}/../ow/sprites/cave_stairs_1100.bmp"
        ),
        "cave_stairs_0110": pygame.image.load(
            f"{dir_path}/../ow/sprites/cave_stairs_0110.bmp"
        ),
        "cave_stairs_1001": pygame.image.load(
            f"{dir_path}/../ow/sprites/cave_stairs_1001.bmp"
        ),
        "cave_stairs_0011": pygame.image.load(
            f"{dir_path}/../ow/sprites/cave_stairs_0011.bmp"
        ),
        "cave_0001_over_edge": pygame.image.load(
            f"{dir_path}/../ow/sprites/cave_0001_over_edge.bmp"
        ),
        "cave_0010_over_edge": pygame.image.load(
            f"{dir_path}/../ow/sprites/cave_0010_over_edge.bmp"
        ),
        "rock": pygame.image.load(f"{dir_path}/../ow/sprites/rock.bmp"),
        "entrance": pygame.image.load(f"{dir_path}/../ow/sprites/cave_entrance.bmp"),
        "inn_map": pygame.image.load(f"{dir_path}/../ow/sprites/inn_map.bmp"),
        "fruit_tree": pygame.image.load(f"{dir_path}/../ow/sprites/fruit_tree.bmp"),
        "water": pygame.image.load(f"{dir_path}/../ow/sprites/water.bmp"),
        "sea": pygame.image.load(f"{dir_path}/../ow/sprites/sea.bmp"),
        "cave_water": pygame.image.load(f"{dir_path}/../ow/sprites/cave_water.bmp"),
        "soil": pygame.image.load(f"{dir_path}/../ow/sprites/soil.bmp"),
        "ground": pygame.image.load(f"{dir_path}/../ow/sprites/ground.bmp"),
        "_tall_grass_1": pygame.image.load(
            f"{dir_path}/../ow/sprites/tall_grass_1.bmp"
        ),
        "_tall_grass_2": pygame.image.load(
            f"{dir_path}/../ow/sprites/tall_grass_2.bmp"
        ),
        "_tall_grass_3": pygame.image.load(
            f"{dir_path}/../ow/sprites/tall_grass_1.bmp"
        ),
        "_tall_grass_4": pygame.image.load(
            f"{dir_path}/../ow/sprites/tall_grass_4.bmp"
        ),
        "hole_in_grass": pygame.image.load(
            f"{dir_path}/../ow/sprites/hole_in_grass.bmp"
        ),
        "buddha_statue": pygame.image.load(
            f"{dir_path}/../ow/sprites/buddha_statue.bmp"
        ),
        "inn_sign": pygame.image.load(f"{dir_path}/../ow/sprites/inn_sign.bmp"),
        "school_sign": pygame.image.load(f"{dir_path}/../ow/sprites/school_sign.bmp"),
        "palm_tree": pygame.image.load(f"{dir_path}/../ow/sprites/palm_tree.bmp"),
        "jungle_tree": pygame.image.load(f"{dir_path}/../ow/sprites/jungle_tree.bmp"),
        "sand": pygame.image.load(f"{dir_path}/../ow/sprites/sand.bmp"),
        "arena_sign": pygame.image.load(f"{dir_path}/../ow/sprites/arena_sign.bmp"),
        "shop_sign": pygame.image.load(f"{dir_path}/../ow/sprites/shop_sign.bmp"),
        "field": pygame.image.load(f"{dir_path}/../ow/sprites/field.bmp"),
        "plane_seat": pygame.image.load(f"{dir_path}/../ow/sprites/plane_seat.bmp"),
        "plane_floor": pygame.image.load(f"{dir_path}/../ow/sprites/plane_floor.bmp"),
        "house_4x4": pygame.image.load(f"{dir_path}/../ow/sprites/house_4x4.png"),
        "portal_3x4": pygame.image.load(f"{dir_path}/../ow/sprites/portal_3x4.png"),
        "low_house_4x3": pygame.image.load(f"{dir_path}/../ow/sprites/low_house_4x3.png"),
        "tree_gate_3x3": pygame.image.load(f"{dir_path}/../ow/sprites/tree_gate_3x3.png"),
    }
