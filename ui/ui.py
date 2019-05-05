import time
import pygame


class Fonts(object):
    def __init__(self):
        self.garuda64 = pygame.font.Font("../fonts/Garuda.ttf", 64)
        self.garuda32 = pygame.font.Font("../fonts/Garuda.ttf", 32)
        self.garuda16 = pygame.font.Font("../fonts/Garuda.ttf", 16)
        self.garuda24 = pygame.font.Font("../fonts/Garuda.ttf", 24)
        self.setha64 = pygame.font.Font("../fonts/JS-Setha-Normal.ttf", 64)
        self.setha32 = pygame.font.Font("../fonts/JS-Setha-Normal.ttf", 32)
        self.setha16 = pygame.font.Font("../fonts/JS-Setha-Normal.ttf", 16)


def npc_sprites():
    # TODO Alexis
    # This should be done automatically
    return {
        "sign": pygame.image.load("../npc/sprites/sign.png"),
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
        "fat_vendor_down": pygame.image.load("../npc/sprites/fat_vendor_down.png"),
        "vendor_down": pygame.image.load("../npc/sprites/vendor_down.png"),
        "vendor_up": pygame.image.load("../npc/sprites/vendor_up.png"),
        "vendor_right": pygame.image.load("../npc/sprites/vendor_right.png"),
        "vendor_left": pygame.image.load("../npc/sprites/vendor_left.png"),
        "kid_up": pygame.image.load("../npc/sprites/kid_up.png"),
        "nurse_down": pygame.image.load("../npc/sprites/nurse_down.png"),
        "monk_down": pygame.image.load("../npc/sprites/monk_down.png"),
    }


def random_images():
    return {
        "full_heart": pygame.image.load("../images/full_heart.png"),
        "selection_arrow": pygame.image.load("../images/selection_arrow.png"),
        "empty_heart": pygame.image.load("../images/empty_heart.png"),
        "sound_icon": pygame.image.load("../images/sound_icon.png"),
        "sound_icon_green": pygame.image.load("../images/sound_icon_green.png"),
    }


class Ui(object):
    def __init__(self):
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        logo = pygame.image.load("../images/thai.png")
        pygame.init()
        pygame.font.init()
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Learn Thai!")
        self.width = 1200
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.fonts = Fonts()
        self.sprites = {
            "grass": pygame.image.load("../ow/sprites/grass.bmp"),
            "path": pygame.image.load("../ow/sprites/path.bmp"),
            "tree": pygame.image.load("../ow/sprites/tree.bmp"),
            "flower": pygame.image.load("../ow/sprites/flower.bmp"),
            "door": pygame.image.load("../ow/sprites/door.bmp"),
            "inn_floor": pygame.image.load("../ow/sprites/inn_floor.bmp"),
            "inn_map": pygame.image.load("../ow/sprites/inn_map.bmp"),
            "fruit_tree": pygame.image.load("../ow/sprites/fruit_tree.bmp"),
            "water": pygame.image.load("../ow/sprites/water.bmp"),
            "ground": pygame.image.load("../ow/sprites/ground.bmp"),
            "tall_grass": pygame.image.load("../ow/sprites/tall_grass.bmp"),
        }
        self.images = random_images()
        self.npc_sprites = npc_sprites()
        self.clock = pygame.time.Clock()
        self.cell_size = 80
        self.draw_tick = 0.03
        self.last_draw_tick = 0

        self.click = None  # looks like (x, y)
        self.hover = None  # looks like (x, y)

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.space = False
        self.backspace = False
        self.w = False

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
                if event.key == pygame.K_o:
                    al.learner.open()
                if event.key == pygame.K_r:
                    al.words.reset_words(al)
                    al.learner.money = 0
                    al.learner.hp = 5
                    al.learner.max_hp = 5
                if event.key == pygame.K_t:
                    al.words.reset_words(al, xp=100)
                if event.key == pygame.K_BACKSPACE:
                    al.ui.backspace = True
                if event.key == pygame.K_SPACE:
                    al.ui.space = True
                if event.key == pygame.K_w:
                    al.dex.w()
                if event.key == pygame.K_RETURN:
                    al.ui.space = True
                if event.key == pygame.K_p:
                    al.learner.print_location()
                if event.key == pygame.K_ESCAPE:
                    if al.active_test:
                        al.active_test = None
                    elif al.active_learning:
                        al.active_learning = None
                    elif al.active_npc:
                        al.active_npc = None
                    elif al.dex.active:
                        al.dex.active = False
                    elif al.active_battle:
                        al.active_battle = None
                    elif al.active_sale:
                        al.active_sale = None
                    else:
                        self.running = False
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
            elif event.type == pygame.MOUSEMOTION:
                al.ui.hover = pygame.mouse.get_pos()

