import pygame
import datetime
from db import get_db_cursor
from lexicon.items import Word
from lexicon.presentation import Presentation, WordPresentation


def draw_square(screen, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)


class WordBox(object):
    def __init__(self, x, y, width, height, word, blinking):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.word = word
        self.hovered = None  # contains (x, y) when hovered
        self.blinking = blinking

    def __contains__(self, item):
        if not self.word or not item:
            return False
        (x, y) = item
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    def draw_1(self, ui):
        if not self.word:
            return
        screen = ui.screen
        x = self.x
        y = self.y
        if self.word.total_xp and self.word.total_xp > 0:
            draw_square(screen, (220, 220, 220), x, y, self.width, self.height)
        else:
            if self.blinking and datetime.datetime.now().second % 2 == 0:
                draw_square(screen, (40, 170, 40), x, y, self.width, self.height)
            else:
                draw_square(screen, (170, 170, 170), x, y, self.width, self.height)

    def draw_2(self, ui):
        if not self.word or not self.hovered:
            return
        screen = ui.screen
        x = self.x
        y = self.y
        if self.word.total_xp and self.word.total_xp > 0:
            if self.hovered:
                pygame.draw.rect(screen, (0, 255, 0), [x, y, self.width, self.height], 3)
        else:
            if self.hovered:
                pygame.draw.rect(screen, (70, 70, 70), [x, y, self.width, self.height], 3)

    def draw_3(self, ui):
        if not self.word:
            return
        screen = ui.screen
        x = self.x
        y = self.y
        if self.word.total_xp and self.word.total_xp > 0:
            screen.blit(ui.images["check_mark"], [x + 80, y - 10])
            screen.blit(ui.fonts.garuda24.render(self.word.thai, True, (0, 0, 0)), (x + 10, y + 20))
        else:
            screen.blit(ui.fonts.garuda24.render(self.word.thai, True, (100, 100, 100)), (x + 10, y + 20))

    def draw_tooltip(self, ui):
        if not self.word or not self.blinking or not self.hovered:
            return
        (x, y) = self.hovered
        screen = ui.screen
        s = " The word is taught in the vicinity! "
        draw_square(screen, (210, 210, 210), x, y, 368, 50)
        screen.blit(ui.fonts.garuda24.render(s, True, (0, 0, 0)), (x, y))


class Dex(object):
    def __init__(self, al):
        self.actualized = False
        self.active = False
        self.al = al
        self.offset = 0
        self.word_boxes = []
        # Drawing
        self.words_per_line = 7
        self.number_of_lines = 6
        self.max_items_to_show = self.words_per_line * self.number_of_lines
        self.square_width = al.ui.percent_width(0.10)
        self.square_height = al.ui.percent_height(0.15)
        self.hovered_box = None
        self.location = self.get_broad_map_name()
        print(self.location)

    def select_words_from_db(self):
        if not self.actualized:
            words_db = list(get_db_cursor().execute(
                f" SELECT w.id, w.split_form, w.thai, w.english, w.tones, w.pos, uw.total_xp, w.location, w.location_x, w.location_y "
                f"FROM words w "
                f"LEFT JOIN user_word uw ON uw.word_id = w.id "
                f"LEFT JOIN users u ON u.id = uw.user_id "
                f"WHERE w.teaching_order > 0 "
                f"AND u.is_playing = 1 "
                f"ORDER BY w.teaching_order "
                f"LIMIT {self.max_items_to_show} OFFSET {self.offset};"
            ))
            words_to_show = [Word(
                id=id,
                split_form=split_form,
                thai=thai,
                english=english,
                tones=tones,
                pos=pos,
                location=location,
                xp=xp,
                x=location_x,
                y=location_y,
            ) for (id, split_form, thai, english, tones, pos, xp, location, location_x, location_y) in words_db]

            self.word_boxes = []
            for line in range(self.number_of_lines):
                for column in range(self.words_per_line):
                    try:
                        word = words_to_show[line * self.words_per_line + column]
                    except IndexError:
                        word = None
                    self.word_boxes.append(WordBox(
                        x=self.al.ui.percent_width(0.15) + column * self.square_width,
                        y=self.al.ui.percent_height(0.05) + line * self.square_height,
                        width=self.square_width,
                        height=self.square_height,
                        word=word,
                        blinking=word and word.location == self.location
                    ))
            self.actualized = True

    def get_broad_map_name(self):
        map_name = self.al.mas.current_map.filename
        mother_map = self.al.mas.get_map_from_name(map_name).parent
        return mother_map.filename if mother_map else map_name

    def w(self):
        self.actualized = False
        self.location = self.get_broad_map_name()
        self.active = not self.active

    def launch_presentation(self, word):
        self.al.active_presentation = WordPresentation(self.al, word, from_dex=True)

    def interact(self):
        ui = self.al.ui
        # if self.al.active_presentation:
        #     self.al.active_presentation.interact()
        #     return
        if ui.down:
            self.offset = self.offset + self.words_per_line
            self.actualized = False
        if ui.up:
            self.offset = max(0, self.offset - self.words_per_line)
            self.actualized = False
        if ui.hover:
            self.hovered_box = None
            for box in self.word_boxes:
                if ui.hover in box:
                    for other_box in self.word_boxes:
                        other_box.hovered = False
                    self.hovered_box = box
                    box.hovered = ui.hover
                    ui.hover = None
                    break
        if ui.click:
            for box in self.word_boxes:
                if ui.click in box:
                    ui.click = None
                    self.launch_presentation(box.word)
                    break
        if self.al.ui.escape:
            self.active = False
            self.al.ui.escape = False

    def draw(self):
        if not self.actualized:
            self.select_words_from_db()
        draw_square(self.al.ui.screen, (150, 150, 150), self.al.ui.percent_width(0.05), self.al.ui.percent_height(0.05), self.al.ui.percent_width(0.90), self.al.ui.percent_height(0.90))
        for box in self.word_boxes:
            box.draw_1(self.al.ui)
        if self.hovered_box:
            self.hovered_box.draw_2(self.al.ui)
        for box in self.word_boxes:
            box.draw_3(self.al.ui)
        if self.hovered_box:
            self.hovered_box.draw_tooltip(self.al.ui)
        if self.al.active_presentation:
            self.al.active_presentation.draw()
