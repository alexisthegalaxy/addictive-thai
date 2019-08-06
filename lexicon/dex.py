import pygame

from db import get_db_cursor
from lexicon.items import Word


class Dex(object):
    def __init__(self, al):
        self.actualized = False
        self.active = False
        self.al = al
        self.offset = 0
        self.words_to_show = []
        self.word_count = len(self.words_to_show)
        self.max_items_to_show = 15

    def select_words_from_db(self):
        if not self.actualized:
            words_db = list(get_db_cursor().execute(
                f"SELECT w.id, w.split_form, w.thai, w.english, w.tones, w.pos, uw.total_xp "
                f"FROM words w "
                f"JOIN user_word uw ON uw.word_id = w.id "
                f"JOIN users u ON u.id = uw.user_id "
                f"WHERE u.is_playing "
                f"AND uw.total_xp > 0 "
                f"ORDER BY uw.total_xp DESC "
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
            self.offset = self.offset + 1
            self.actualized = False
        if self.al.ui.up:
            self.offset = max(0, self.offset - 1)
            self.actualized = False

    def draw(self):
        if not self.actualized:
            self.select_words_from_db()
        # TODO Alexis
        ui = self.al.ui
        g16 = ui.fonts.garuda16
        x = ui.percent_width(0.1)
        y = ui.percent_height(0.1)
        height = ui.percent_height(0.81)
        width = ui.percent_width(0.8)

        screen = ui.screen
        pygame.draw.rect(screen, (150, 150, 150), (x, y, width, height))
        pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)

        # Draw header
        y = ui.percent_height(0.11)
        x = ui.percent_width(0.12)
        screen.blit(g16.render("Thai", True, (0, 0, 0)), (x, y))
        x = ui.percent_width(0.28)
        screen.blit(g16.render("English", True, (0, 0, 0)), (x, y))
        x = ui.percent_width(0.65)
        screen.blit(g16.render("Level", True, (0, 0, 0)), (x, y))
        x = ui.percent_width(0.78)
        screen.blit(g16.render("Experience", True, (0, 0, 0)), (x, y))

        y = ui.percent_height(0.15)
        for i, word in enumerate(self.words_to_show):
            # if 0 <= i - self.offset < self.max_items_to_show:
            x = ui.percent_width(0.12)
            screen.blit(g16.render(word.thai, True, (0, 0, 0)), (x, y))
            x = ui.percent_width(0.28)
            screen.blit(g16.render(word.english, True, (0, 0, 0)), (x, y))
            x = ui.percent_width(0.65)
            screen.blit(g16.render(str(word.level), True, (0, 0, 0)), (x, y))
            x = ui.percent_width(0.78)
            screen.blit(g16.render(str(word.total_xp), True, (0, 0, 0)), (x, y))
            y += ui.percent_width(0.03)
