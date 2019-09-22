import pygame

from db import get_db_cursor
from lexicon.items import Word


def draw_square(screen, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)


class Dex(object):
    def __init__(self, al):
        self.actualized = False
        self.active = False
        self.al = al
        self.offset = 0
        self.words_to_show = []
        self.word_count = len(self.words_to_show)
        # Drawing
        self.words_per_line = 7
        self.number_of_lines = 6
        self.max_items_to_show = self.words_per_line * self.number_of_lines

    def select_words_from_db(self):
        if not self.actualized:
            words_db = list(get_db_cursor().execute(
                f"SELECT w.id, w.split_form, w.thai, w.english, w.tones, w.pos, uw.total_xp "
                f"FROM words w "
                f"JOIN user_word uw ON uw.word_id = w.id "
                f"JOIN users u ON u.id = uw.user_id "
                f"WHERE w.teaching_order > 0 "
                # f"WHERE u.is_playing "
                # f"AND uw.total_xp > 0 "
                f"ORDER BY w.teaching_order DESC "
                f"LIMIT {self.max_items_to_show} OFFSET {self.offset};"
            ))
            self.words_to_show = [Word(
                id=id,
                split_form=split_form,
                thai=thai,
                english=english,
                tones=tones,
                pos=pos,
                xp=xp,
            ) for (id, split_form, thai, english, tones, pos, xp) in words_db]
            self.actualized = True

    def w(self):
        self.actualized = False
        self.active = not self.active
        self.word_count = len(self.words_to_show)

    def interact(self):
        if self.al.ui.down:
            self.offset = self.offset + self.words_per_line
            self.actualized = False
        if self.al.ui.up:
            self.offset = max(0, self.offset - self.words_per_line)
            self.actualized = False

    def draw(self):
        if not self.actualized:
            self.select_words_from_db()
        # TODO Alexis
        """
        # 1 - draw background
        # 2 - draw squares for each word
            7 * 5
        # 3 - 
        """

        # 1 - draw background
        ui = self.al.ui
        g24 = ui.fonts.garuda24
        screen = ui.screen
        draw_square(screen, (150, 150, 150), ui.percent_width(0.05), ui.percent_height(0.05), ui.percent_width(0.90), ui.percent_height(0.90))
        # # Draw header
        # y = ui.percent_height(0.11)
        # x = ui.percent_width(0.12)
        # screen.blit(g16.render("Thai", True, (0, 0, 0)), (x, y))
        # x = ui.percent_width(0.28)
        # screen.blit(g16.render("English", True, (0, 0, 0)), (x, y))
        # x = ui.percent_width(0.65)
        # screen.blit(g16.render("Level", True, (0, 0, 0)), (x, y))
        # x = ui.percent_width(0.78)
        # screen.blit(g16.render("Experience", True, (0, 0, 0)), (x, y))
        square_width = ui.percent_width(0.10)
        square_height = ui.percent_height(0.15)
        for column in range(self.words_per_line):  # 0, ..., 6
            for line in range(self.number_of_lines):  # 0, ..., 4
                x = ui.percent_width(0.15) + column * square_width
                y = ui.percent_height(0.05) + line * square_height
                try:
                    word = self.words_to_show[line * self.words_per_line + column]
                    if word.total_xp > 0:
                        draw_square(screen, (220, 220, 220), x, y, square_width, square_height)
                    else:
                        draw_square(screen, (170, 170, 170), x, y, square_width, square_height)
                except IndexError:
                    pass
        for column in range(self.words_per_line):  # 0, ..., 6
            for line in range(self.number_of_lines):  # 0, ..., 4
                x = ui.percent_width(0.15) + column * square_width
                y = ui.percent_height(0.05) + line * square_height
                try:
                    word = self.words_to_show[line * self.words_per_line + column]
                    if word.total_xp > 0:
                        screen.blit(ui.images["check_mark"], [x + 80, y - 10])
                        screen.blit(g24.render(word.thai, True, (0, 0, 0)), (x + 10, y + 20))
                    else:
                        screen.blit(g24.render(word.thai, True, (100, 100, 100)), (x + 10, y + 20))
                except IndexError:
                    pass

        # y = ui.percent_height(0.15)
        # for i, word in enumerate(self.words_to_show):
        #     # if 0 <= i - self.offset < self.max_items_to_show:
        #     x = ui.percent_width(0.12)
        #     screen.blit(g16.render(word.thai, True, (0, 0, 0)), (x, y))
        #     x = ui.percent_width(0.28)
        #     screen.blit(g16.render(word.english, True, (0, 0, 0)), (x, y))
        #     x = ui.percent_width(0.65)
        #     screen.blit(g16.render(str(word.level), True, (0, 0, 0)), (x, y))
        #     x = ui.percent_width(0.78)
        #     screen.blit(g16.render(str(word.total_xp), True, (0, 0, 0)), (x, y))
        #     y += ui.percent_width(0.03)
