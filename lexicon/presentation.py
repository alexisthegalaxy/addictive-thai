import pygame

from lexicon.items import Word
from mechanics.minimap import Minimap
from sounds.play_sound import play_transformed_thai_word


class Presentation(object):
    """
    An interactive screen that shows a word
    """

    def __init__(self, al, word: Word, from_learning=False, from_dex=False):
        self.al = al
        self.word = word
        # parameters
        self.from_learning = from_learning
        self.from_dex = from_dex
        # drawing
        self.selector_on_sound = False
        # obtained from DB
        self.sentences = word.get_sentences()
        self.selected_sentence_index = 0

    def interact(self):
        ui = self.al.ui
        if ui.hover:
            self.selector_on_sound = self.on_sound(ui.hover, ui)
        if ui.click:
            if self.on_sound(ui.click, ui):
                play_transformed_thai_word(self.word.thai)
                ui.click = None
            if self.outside_presentation(ui.click, ui):
                self.al.active_presentation = None
                self.al.active_minimap = None
                ui.click = None
        if ui.right:
            ui.right = None
            self.selected_sentence_index += 1
            if self.selected_sentence_index == len(self.sentences):
                self.selected_sentence_index = 0
        if ui.left:
            ui.left = None
            self.selected_sentence_index -= 1
            if self.selected_sentence_index == -1:
                self.selected_sentence_index = len(self.sentences) - 1
        if ui.m:
            ui.m = False
            self.al.active_minimap = Minimap(self.al, interest_point=(self.word.x, self.word.y))

    def on_sound(self, point, ui):
        if not point:
            return False
        x, y = point
        x1 = ui.percent_width(0.15)
        x2 = ui.percent_width(0.25)
        y1 = ui.percent_width(0.10)
        y2 = ui.percent_width(0.18)
        return x1 < x < x2 and y1 < y < y2

    def outside_presentation(self, point, ui):
        if not point:
            return False
        p_x, p_y = point
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        height = ui.percent_height(0.76)
        width = ui.percent_width(0.76)
        return not (x < p_x < x + width and y < p_y < y + height)

    def draw(self):
        ui = self.al.ui
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        height = ui.percent_height(0.76)
        width = ui.percent_width(0.76)

        screen = ui.screen
        pygame.draw.rect(screen, (180, 180, 180), (x, y, width, height))
        pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)

        # draw sound
        sound_x = ui.percent_width(0.15)
        sound_y = ui.percent_height(0.14)
        sound = "sound_icon_green" if self.selector_on_sound else "sound_icon"
        ui.screen.blit(ui.images[sound], [sound_x, sound_y])

        # Draw Thai word
        x = ui.percent_width(0.26)
        y = ui.percent_height(0.15)
        screen.blit(ui.fonts.garuda64.render(self.word.thai, True, (0, 0, 0)), (x, y))

        # Draw English
        x = ui.percent_width(0.26)
        y = ui.percent_height(0.27)
        screen.blit(
            ui.fonts.garuda48.render(self.word.english, True, (0, 0, 0)), (x, y)
        )

        if self.from_dex:
            x = ui.percent_width(0.26)
            y += ui.percent_height(0.10)
            s = f"Level: {self.word.level}  XP: {self.word.total_xp}"
            screen.blit(ui.fonts.garuda16.render(s, True, (0, 0, 0)), (x, y))

        try:
            sentence = self.sentences[self.selected_sentence_index]
            x = ui.percent_width(0.15)
            y += ui.percent_height(0.06)
            s = f"Sentences ({self.selected_sentence_index + 1}/{len(self.sentences)})"
            screen.blit(ui.fonts.garuda48.render(s, True, (0, 0, 0)), (x, y))

            x = ui.percent_width(0.23)
            y += ui.percent_height(0.11)
            s = f"{sentence.thai}"
            screen.blit(ui.fonts.garuda32.render(s, True, (0, 0, 0)), (x, y))

            x = ui.percent_width(0.23)
            y += ui.percent_height(0.08)
            s = f"{sentence.english}"
            screen.blit(ui.fonts.garuda28.render(s, True, (0, 0, 0)), (x, y))

        except IndexError:
            pass
