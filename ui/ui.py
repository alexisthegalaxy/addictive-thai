import time
import pygame

from lexicon.items import Words
from mechanics.minimap import Minimap, want_to_launch_map


class Fonts(object):
    def __init__(self):
        self.garuda64 = pygame.font.Font("../fonts/Garuda.ttf", 64)
        self.garuda48 = pygame.font.Font("../fonts/Garuda.ttf", 48)
        self.garuda32 = pygame.font.Font("../fonts/Garuda.ttf", 32)
        self.garuda16 = pygame.font.Font("../fonts/Garuda.ttf", 16)
        self.garuda24 = pygame.font.Font("../fonts/Garuda.ttf", 24)
        self.garuda28 = pygame.font.Font("../fonts/Garuda.ttf", 28)
        self.setha64 = pygame.font.Font("../fonts/JS-Setha-Normal.ttf", 64)
        self.setha32 = pygame.font.Font("../fonts/JS-Setha-Normal.ttf", 32)
        self.setha16 = pygame.font.Font("../fonts/JS-Setha-Normal.ttf", 16)


def npc_sprites():
    # TODO Alexis
    # This should be done automatically
    return {
        "sign": pygame.image.load("../npc/sprites/sign.png"),
        "bed": pygame.image.load("../npc/sprites/bed.png"),
        "mom_up": pygame.image.load("../npc/sprites/mom_up.png"),
        "mom_down": pygame.image.load("../npc/sprites/mom_down.png"),
        "dad_down": pygame.image.load("../npc/sprites/dad_down.png"),
        "dad_up": pygame.image.load("../npc/sprites/dad_up.png"),
        "dad_right": pygame.image.load("../npc/sprites/dad_right.png"),
        "dad_left": pygame.image.load("../npc/sprites/dad_left.png"),
        "mom_right": pygame.image.load("../npc/sprites/mom_right.png"),
        "mom_left": pygame.image.load("../npc/sprites/mom_left.png"),
        "mali_down": pygame.image.load("../npc/sprites/mali_down.png"),
        "old_man_left": pygame.image.load("../npc/sprites/old_man_left.png"),
        "old_man_right": pygame.image.load("../npc/sprites/old_man_right.png"),
        "old_man_down": pygame.image.load("../npc/sprites/old_man_down.png"),
        "old_man_up": pygame.image.load("../npc/sprites/old_man_up.png"),
        "old_woman_left": pygame.image.load("../npc/sprites/old_woman_left.png"),
        "old_woman_right": pygame.image.load("../npc/sprites/old_woman_right.png"),
        "old_woman_down": pygame.image.load("../npc/sprites/old_woman_down.png"),
        "old_woman_up": pygame.image.load("../npc/sprites/old_woman_up.png"),
        "fat_vendor_down": pygame.image.load("../npc/sprites/fat_vendor_down.png"),
        "vendor_down": pygame.image.load("../npc/sprites/vendor_down.png"),
        "vendor_up": pygame.image.load("../npc/sprites/vendor_up.png"),
        "vendor_right": pygame.image.load("../npc/sprites/vendor_right.png"),
        "vendor_left": pygame.image.load("../npc/sprites/vendor_left.png"),
        "cat_up": pygame.image.load("../npc/sprites/cat_up.png"),
        "cat_down": pygame.image.load("../npc/sprites/cat_down.png"),
        "cat_right": pygame.image.load("../npc/sprites/cat_right.png"),
        "cat_left": pygame.image.load("../npc/sprites/cat_left.png"),
        "celine_down": pygame.image.load("../npc/sprites/celine_down.png"),
        "celine_up": pygame.image.load("../npc/sprites/celine_up.png"),
        "celine_right": pygame.image.load("../npc/sprites/celine_right.png"),
        "celine_left": pygame.image.load("../npc/sprites/celine_left.png"),
        "alexis_down": pygame.image.load("../npc/sprites/alexis_down.png"),
        "alexis_up": pygame.image.load("../npc/sprites/alexis_up.png"),
        "alexis_right": pygame.image.load("../npc/sprites/alexis_right.png"),
        "alexis_left": pygame.image.load("../npc/sprites/alexis_left.png"),
        "kid_up": pygame.image.load("../npc/sprites/kid_up.png"),
        "kid_down": pygame.image.load("../npc/sprites/kid_down.png"),
        "kid_right": pygame.image.load("../npc/sprites/kid_right.png"),
        "kid_left": pygame.image.load("../npc/sprites/kid_left.png"),
        "lass_up": pygame.image.load("../npc/sprites/lass_up.png"),
        "ghost_down": pygame.image.load("../npc/sprites/ghost_down.png"),
        "lass_down": pygame.image.load("../npc/sprites/lass_down.png"),
        "lass_right": pygame.image.load("../npc/sprites/lass_right.png"),
        "lass_left": pygame.image.load("../npc/sprites/lass_left.png"),
        "dog_up": pygame.image.load("../npc/sprites/dog_up.png"),
        "dog_down": pygame.image.load("../npc/sprites/dog_down.png"),
        "dog_right": pygame.image.load("../npc/sprites/dog_right.png"),
        "dog_left": pygame.image.load("../npc/sprites/dog_left.png"),
        "clown_fish_left": pygame.image.load("../npc/sprites/clown_fish_left.png"),
        "clown_fish_right": pygame.image.load("../npc/sprites/clown_fish_right.png"),
        "nurse_down": pygame.image.load("../npc/sprites/nurse_down.png"),
        "monk_down": pygame.image.load("../npc/sprites/monk_down.png"),
        "monk_up": pygame.image.load("../npc/sprites/monk_up.png"),
        "gecko_down": pygame.image.load("../npc/sprites/gecko_down.png"),
        "gecko_up": pygame.image.load("../npc/sprites/gecko_up.png"),
        "gecko_right": pygame.image.load("../npc/sprites/gecko_right.png"),
        "gecko_left": pygame.image.load("../npc/sprites/gecko_left.png"),
        "crocodile_down": pygame.image.load("../npc/sprites/crocodile_down.png"),
        "crocodile_up": pygame.image.load("../npc/sprites/crocodile_up.png"),
        "crocodile_right": pygame.image.load("../npc/sprites/crocodile_right.png"),
        "crocodile_left": pygame.image.load("../npc/sprites/crocodile_left.png"),
        "rich_woman_left": pygame.image.load("../npc/sprites/rich_woman_left.png"),
        "rich_woman_right": pygame.image.load("../npc/sprites/rich_woman_right.png"),
        "rich_woman_up": pygame.image.load("../npc/sprites/rich_woman_up.png"),
        "rich_woman_down": pygame.image.load("../npc/sprites/rich_woman_down.png"),
        "woman_left": pygame.image.load("../npc/sprites/woman_left.png"),
        "woman_right": pygame.image.load("../npc/sprites/woman_right.png"),
        "woman_up": pygame.image.load("../npc/sprites/woman_up.png"),
        "woman_down": pygame.image.load("../npc/sprites/woman_down.png"),
    }


def random_images():
    return {
        "full_heart": pygame.image.load("../images/full_heart.png"),
        "check_mark": pygame.image.load("../images/check_mark.png"),
        "selection_arrow": pygame.image.load("../images/selection_arrow.png"),
        "empty_heart": pygame.image.load("../images/empty_heart.png"),
        "sound_icon": pygame.image.load("../images/sound_icon.png"),
        "sound_icon_green": pygame.image.load("../images/sound_icon_green.png"),
        "exclamation_mark": pygame.image.load("../images/exclamation_mark.png"),
        "learning_mark": pygame.image.load("../images/learning_mark.png"),
        "brain_0": pygame.image.load("../images/brain_0.png"),
        "brain_1": pygame.image.load("../images/brain_1.png"),
        "brain_2": pygame.image.load("../images/brain_2.png"),
        "brain_3": pygame.image.load("../images/brain_3.png"),
        "brain_4": pygame.image.load("../images/brain_4.png"),
        "brain_5": pygame.image.load("../images/brain_5.png"),
        "brain_6": pygame.image.load("../images/brain_6.png"),
        "rising": pygame.image.load("../images/rising.png"),
        "mid": pygame.image.load("../images/mid.png"),
        "low": pygame.image.load("../images/low.png"),
        "falling": pygame.image.load("../images/falling.png"),
        "high": pygame.image.load("../images/high.png"),
    }


class Ui(object):
    def __init__(self):
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        logo = pygame.image.load("../images/thai.png")
        pygame.init()
        pygame.font.init()
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Once upon a Thai!")
        self.width = 1200
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.fonts = Fonts()
        self.sprites = {
            "grass": pygame.image.load("../ow/sprites/grass.bmp"),
            "path": pygame.image.load("../ow/sprites/path.bmp"),
            "tree": pygame.image.load("../ow/sprites/tree.bmp"),
            "waterfall": pygame.image.load("../ow/sprites/waterfall1.bmp"),
            "bridge_hor": pygame.image.load("../ow/sprites/bridge_hor.bmp"),
            "bridge_ver": pygame.image.load("../ow/sprites/bridge_ver.bmp"),
            "flower": pygame.image.load("../ow/sprites/flower.bmp"),
            "flower_2": pygame.image.load("../ow/sprites/flower_2.bmp"),
            "nenuphar": pygame.image.load("../ow/sprites/nenuphar.bmp"),
            "door": pygame.image.load("../ow/sprites/door.bmp"),
            "inn_floor": pygame.image.load("../ow/sprites/inn_floor.bmp"),
            "temple_floor": pygame.image.load("../ow/sprites/temple_floor.bmp"),
            "cave_floor": pygame.image.load("../ow/sprites/cave_floor.bmp"),
            "boulder_2": pygame.image.load("../ow/sprites/boulder_2.bmp"),
            "field_spirit_house": pygame.image.load("../ow/sprites/field_spirit_house.bmp"),

            'cave_0010': pygame.image.load("../ow/sprites/cave_0010.bmp"),
            'cave_0110': pygame.image.load("../ow/sprites/cave_0110.bmp"),
            'cave_0100': pygame.image.load("../ow/sprites/cave_0100.bmp"),
            'cave_1100': pygame.image.load("../ow/sprites/cave_1100.bmp"),
            'cave_1000': pygame.image.load("../ow/sprites/cave_1000.bmp"),
            'cave_1001': pygame.image.load("../ow/sprites/cave_1001.bmp"),
            'cave_0001': pygame.image.load("../ow/sprites/cave_0001.bmp"),
            'cave_0011': pygame.image.load("../ow/sprites/cave_0011.bmp"),
            'cave_1110': pygame.image.load("../ow/sprites/cave_1110.bmp"),
            'cave_1101': pygame.image.load("../ow/sprites/cave_1101.bmp"),
            'cave_entrance_down': pygame.image.load("../ow/sprites/cave_entrance_down.bmp"),
            'cave_stairs_1100': pygame.image.load("../ow/sprites/cave_stairs_1100.bmp"),
            'cave_stairs_0110': pygame.image.load("../ow/sprites/cave_stairs_0110.bmp"),
            'cave_stairs_1001': pygame.image.load("../ow/sprites/cave_stairs_1001.bmp"),
            'cave_stairs_0011': pygame.image.load("../ow/sprites/cave_stairs_0011.bmp"),
            'cave_0001_over_edge': pygame.image.load("../ow/sprites/cave_0001_over_edge.bmp"),
            'cave_0010_over_edge': pygame.image.load("../ow/sprites/cave_0010_over_edge.bmp"),

            "rock": pygame.image.load("../ow/sprites/rock.bmp"),
            "entrance": pygame.image.load("../ow/sprites/cave_entrance.bmp"),
            "inn_map": pygame.image.load("../ow/sprites/inn_map.bmp"),
            "fruit_tree": pygame.image.load("../ow/sprites/fruit_tree.bmp"),
            "water": pygame.image.load("../ow/sprites/water.bmp"),
            "cave_water": pygame.image.load("../ow/sprites/cave_water.bmp"),
            "ground": pygame.image.load("../ow/sprites/ground.bmp"),
            "tall_grass": pygame.image.load("../ow/sprites/tall_grass.bmp"),
            "buddha_statue": pygame.image.load("../ow/sprites/buddha_statue.bmp"),
            "inn_sign": pygame.image.load("../ow/sprites/inn_sign.bmp"),
            "school_sign": pygame.image.load("../ow/sprites/school_sign.bmp"),
            "arena_sign": pygame.image.load("../ow/sprites/arena_sign.bmp"),
            "shop_sign": pygame.image.load("../ow/sprites/shop_sign.bmp"),
            "field": pygame.image.load("../ow/sprites/field.bmp"),
        }
        self.images = random_images()
        self.npc_sprites = npc_sprites()
        self.clock = pygame.time.Clock()
        self.cell_size = 80
        self.draw_tick = 0.03
        self.last_draw_tick = 0

        self.click = None  # looks like (x, y)
        self.click_up = None  # looks like (x, y)
        self.hover = None  # looks like (x, y)

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.space = False
        self.backspace = False
        self.plus = False
        self.minus = False
        self.w = False
        self.m = False
        self.escape = False

    def can_draw_cell(self, x: int, y: int):
        min_x = -self.cell_size
        min_y = -self.cell_size
        return min_x <= x <= self.width and min_y <= y <= self.height

    def percent_height(self, ratio):
        return int(ratio * self.height)

    def percent_width(self, ratio):
        return int(ratio * self.width)

    def lapsed_tick(self) -> bool:
        return time.time() - self.last_draw_tick > self.draw_tick

    def tick(self) -> None:
        self.last_draw_tick = time.time()

    def listen_event(self, al):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    al.ui.up = True
                if event.key == pygame.K_DOWN:
                    al.ui.down = True
                if event.key == pygame.K_RIGHT:
                    al.ui.right = True
                if event.key == pygame.K_LEFT:
                    al.ui.left = True
                if event.key == 61:  # PLUS
                    al.ui.plus = True
                if event.key == pygame.K_MINUS:
                    al.ui.minus = True
                if event.key == pygame.K_o:
                    al.learner.open()
                if event.key == pygame.K_r:
                    Words.reset_words(xp=0)
                    al.learner.money = 3
                    al.learner.hp = 5
                    al.learner.max_hp = 5
                if event.key == pygame.K_t:
                    Words.reset_words(xp=100)
                if event.key == pygame.K_BACKSPACE:
                    al.ui.backspace = True
                if event.key == pygame.K_SPACE:
                    al.ui.space = True
                if event.key == pygame.K_w:
                    al.dex.w()
                if event.key == pygame.K_m:
                    if not al.active_presentation:
                        if al.active_minimap:
                            al.active_minimap = None
                        else:
                            want_to_launch_map(al, show_learner=True)
                    else:
                        al.ui.m = True
                if event.key == pygame.K_RETURN:
                    al.ui.space = True
                if event.key == pygame.K_p:
                    al.learner.print_location()
                if event.key == pygame.K_ESCAPE:
                    # TODO All of this should be processed after all the al.interact
                    #  so that each component can have its own way of dealing with the escape key
                    #  eg Dex closing the presentation page.
                    al.ui.escape = True
                    if al.active_test:
                        al.active_test = None
                        al.ui.escape = False
                    elif al.active_minimap:
                        al.active_minimap = None
                        al.ui.escape = False
                    elif al.active_npc:
                        al.active_npc = None
                        al.ui.escape = False
                    elif al.active_battle:
                        al.active_battle.end_battle()
                        al.ui.escape = False
                    elif al.active_sale:
                        al.active_sale = None
                        al.ui.escape = False
                if event.key == pygame.K_s:
                    al.profiles.current_profile.save(al)
                if event.key == pygame.K_l:
                    al.profiles.current_profile.load(al)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    al.ui.up = False
                if event.key == pygame.K_DOWN:
                    al.ui.down = False
                if event.key == pygame.K_RIGHT:
                    al.ui.right = False
                if event.key == pygame.K_LEFT:
                    al.ui.left = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                al.ui.click = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                al.ui.click_up = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEMOTION:
                al.ui.hover = pygame.mouse.get_pos()

