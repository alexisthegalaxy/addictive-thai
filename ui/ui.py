import time
import pygame

from mechanics.minimap import want_to_launch_map

import os

from profile.profile import save
from ui.fonts import Fonts
from ui.import_images_and_fonts import get_sprites, random_images, npc_sprites

dir_path = os.path.dirname(os.path.realpath(__file__))


class Ui(object):
    def __init__(self):
        logo = pygame.image.load(f"{dir_path}/../images/thai.png")
        pygame.init()
        pygame.font.init()
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Once upon a Thai!")
        self.width = 1200
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.fonts = Fonts()
        self.sprites = get_sprites()
        self.images = random_images()
        self.npc_sprites = npc_sprites()
        self.clock = pygame.time.Clock()
        self.cell_size = 80
        self.draw_tick = 0.03
        self.last_draw_tick = 0

        self.click = None  # looks like (x, y)
        self.click_up = None  # looks like (x, y)
        self.hover = None  # looks like (x, y)

        # keyboard
        self.escape = False
        # row 1
        self.plusminus = False
        self.one = False
        self.two = False
        self.three = False
        self.four = False
        self.five = False
        self.six = False
        self.seven = False
        self.eight = False
        self.nine = False
        self.zero = False
        self.minus = False
        self.plus = False
        self.backspace = False
        # row 2
        self.q = False
        self.w = False
        self.e = False
        self.r = False
        self.t = False
        self.y = False
        self.u = False
        self.i = False
        self.o = False
        self.p = False
        self.left_bracket = False
        self.right_bracket = False
        # row 3
        self.a = False
        self.s = False
        self.d = False
        self.f = False
        self.g = False
        self.h = False
        self.j = False
        self.k = False
        self.l = False
        self.semicolon = False
        self.quote = False
        self.backslash = False
        # row 4
        self.right_shift = False
        self.backtick = False
        self.z = False
        self.x = False
        self.c = False
        self.v = False
        self.b = False
        self.n = False
        self.m = False
        self.comma = False
        self.period = False
        self.slash = False
        self.left_shift = False

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.space = False
        self.enter = False

    def can_draw_cell(self, x: int, y: int, cell_is_special=False):
        if not cell_is_special:
            min_x = -self.cell_size
            min_y = -self.cell_size
            return min_x <= x <= self.width and min_y <= y <= self.height
        min_x = -self.cell_size * 4
        min_y = -self.cell_size * 4
        result = min_x <= x <= self.width * 3 and min_y <= y <= self.height * 3
        return result

    def is_shift(self):
        return self.right_shift or self.left_shift

    def nothing_is_active(self, al):
        return (
            al.active_test is None
            and al.active_sale is None
            and al.active_npc is None
            and al.active_learning is None
            and al.active_spell_identification is None
            and al.active_presentation is None
            and al.active_naming is None
            and al.active_fight is None
            and al.active_tablet is None
            and al.active_minimap is None
            and al.active_consonant_race is None
            and al.active_sale is None
            and al.active_gardening is None
            and not al.learner.in_portal_world
            and not al.dex.active
            and not al.lex.active
        )

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
                # Row 1:
                if event.key == 160:
                    al.ui.plusminus = True
                if event.key == pygame.K_1:
                    al.ui.one = True
                if event.key == pygame.K_2:
                    al.ui.two = True
                if event.key == pygame.K_3:
                    al.ui.three = True
                if event.key == pygame.K_4:
                    al.ui.four = True
                if event.key == pygame.K_5:
                    al.ui.five = True
                if event.key == pygame.K_6:
                    al.ui.six = True
                if event.key == pygame.K_7:
                    al.ui.seven = True
                if event.key == pygame.K_8:
                    al.ui.eight = True
                if event.key == pygame.K_9:
                    al.ui.nine = True
                if event.key == pygame.K_0:
                    al.ui.zero = True
                if event.key == pygame.K_MINUS:
                    al.ui.minus = True
                if event.key == pygame.K_EQUALS:
                    al.ui.plus = True
                if event.key == pygame.K_BACKSPACE:
                    al.ui.backspace = True
                # Row 2
                if event.key == pygame.K_q:
                    al.ui.q = True
                if event.key == pygame.K_w:
                    if self.nothing_is_active(al):
                        al.dex.w()
                    else:
                        al.ui.w = True
                if event.key == pygame.K_e:
                    al.ui.e = True
                if event.key == pygame.K_r:
                    if self.nothing_is_active(al):
                        al.learner.hp = 5
                        al.learner.max_hp = 5
                        # Words.reset_words(xp=0)
                        # al.learner.money = 3
                    else:
                        al.ui.r = True
                if event.key == pygame.K_t:
                    if self.nothing_is_active(al):
                        from mechanics.consonant_race.tablet.tablet import Tablet
                        al.active_tablet = Tablet(al)
                    else:
                        al.ui.t = True
                if event.key == pygame.K_y:
                    al.ui.y = True
                if event.key == pygame.K_u:
                    al.ui.u = True
                if event.key == pygame.K_i:
                    al.ui.i = True
                if event.key == pygame.K_o:
                    if self.nothing_is_active(al):
                        al.learner.open()
                    else:
                        al.ui.o = True
                if event.key == pygame.K_p:
                    if self.nothing_is_active(al):
                        al.learner.print_location()
                    else:
                        al.ui.p = True
                if event.key == pygame.K_LEFTBRACKET:
                    al.ui.left_bracket = True
                if event.key == pygame.K_RIGHTBRACKET:
                    al.ui.right_bracket = True
                # Row 3:
                if event.key == pygame.K_a:
                    al.ui.a = True
                if event.key == pygame.K_s:
                    if al.active_test:
                        al.ui.s = True
                    if self.nothing_is_active(al):
                        save(al)
                if event.key == pygame.K_d:
                    al.ui.d = True
                if event.key == pygame.K_f:
                    al.ui.f = True
                if event.key == pygame.K_g:
                    al.ui.g = True
                if event.key == pygame.K_h:
                    al.ui.h = True
                if event.key == pygame.K_j:
                    al.ui.j = True
                if event.key == pygame.K_k:
                    al.ui.k = True
                if event.key == pygame.K_l:
                    if al.active_test:
                        al.ui.l = True
                    if self.nothing_is_active(al):
                        al.lex.l()
                if event.key == pygame.K_SEMICOLON:
                    al.ui.semicolon = True
                if event.key == pygame.K_QUOTE:
                    al.ui.quote = True
                if event.key == pygame.K_BACKSLASH:
                    al.ui.backslash = True
                # Row 4:
                if event.key == pygame.K_LSHIFT:
                    al.ui.left_shift = True
                if event.key == pygame.K_BACKQUOTE:
                    al.ui.backtick = True
                if event.key == pygame.K_z:
                    al.ui.z = True
                if event.key == pygame.K_x:
                    al.ui.x = True
                if event.key == pygame.K_c:
                    al.ui.c = True
                if event.key == pygame.K_v:
                    al.ui.v = True
                if event.key == pygame.K_b:
                    al.ui.b = True
                if event.key == pygame.K_n:
                    al.ui.n = True
                if event.key == pygame.K_m:
                    if al.active_presentation or al.active_test:
                        al.ui.m = True
                    if al.active_minimap:
                        al.active_minimap = None
                    elif self.nothing_is_active(al):
                        want_to_launch_map(al, show_learner=True)
                if event.key == pygame.K_COMMA:
                    al.ui.comma = True
                if event.key == pygame.K_PERIOD:
                    al.ui.period = True
                if event.key == pygame.K_SLASH:
                    al.ui.slash = True
                if event.key == pygame.K_RSHIFT:
                    al.ui.right_shift = True
                if event.key == pygame.K_u:
                    if self.nothing_is_active(al):
                        al.learner.hp = max(al.learner.hp - 1 / 8, 0)
                        # Words.reset_words(xp=100)
                if event.key == pygame.K_SPACE:
                    al.ui.space = True
                if event.key == pygame.K_RETURN:
                    al.ui.enter = True
                if event.key == pygame.K_ESCAPE:
                    # TODO All of this should be processed after all the al.interact
                    #  so that each component can have its own way of dealing with the escape key
                    #  eg Dex closing the presentation page.
                    al.ui.escape = True
                    if al.active_test:
                        al.active_test = None
                        al.ui.escape = False
                    if al.active_learning:
                        al.active_learning = None
                        al.ui.escape = False
                    elif al.active_minimap:
                        al.active_minimap = None
                        al.ui.escape = False
                    elif al.active_tablet:
                        al.active_tablet = None
                        al.ui.escape = False
                    elif al.active_npc:
                        al.active_npc = None
                        al.ui.escape = False
                    elif al.active_naming:
                        al.active_naming.end_naming()
                        al.ui.escape = False
                    elif al.active_fight:
                        al.active_fight.end_fight()
                        al.ui.escape = False
                    elif al.active_consonant_race:
                        al.active_consonant_race.end()
                        al.ui.escape = False
                    elif al.active_sale:
                        al.active_sale = None
                        al.ui.escape = False
                    elif al.active_spell_identification:
                        al.active_spell_identification = None
                        al.ui.escape = False
                # else:
                #     print('event.key', event.key)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    al.ui.up = False
                if event.key == pygame.K_DOWN:
                    al.ui.down = False
                if event.key == pygame.K_RIGHT:
                    al.ui.right = False
                if event.key == pygame.K_LEFT:
                    al.ui.left = False
                if event.key == pygame.K_RSHIFT:
                    al.ui.right_shift = False
                if event.key == pygame.K_LSHIFT:
                    al.ui.left_shift = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                al.ui.click = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                al.ui.click_up = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEMOTION:
                al.ui.hover = pygame.mouse.get_pos()
