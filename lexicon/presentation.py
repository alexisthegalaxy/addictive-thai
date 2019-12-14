import pygame

from lexicon.items import Word, Letter
from mechanics.minimap import Minimap, want_to_launch_map
from sounds.play_sound import play_transformed_thai_word


class Presentation(object):
    """
    An interactive screen that shows a word
    """

    def __init__(self):
        self.al = None
        self.presented = None
        self.from_learning = None
        self.from_dex = None
        # drawing
        self.selector_on_sound = None
        self.selector_on_map = None

    def interact(self):
        ui = self.al.ui
        if ui.hover:
            self.selector_on_sound = self.on_sound(ui.hover, ui)
            self.selector_on_map = self.on_map(ui.hover, ui)
            if not self.outside_presentation(ui.click, ui):
                ui.hover = None
        if ui.click:
            if self.on_sound(ui.click, ui):
                print('self.presented.audio', self.presented.audio)
                if hasattr(self.presented, 'audio'):
                    print('self.presented.audio', self.presented.audio)
                    play_transformed_thai_word(self.presented.audio)
                else:
                    play_transformed_thai_word(self.presented.thai)
                ui.click = None
            if self.from_dex and self.on_map(ui.click, ui):
                want_to_launch_map(self.al, interest_point=(self.presented.x, self.presented.y))
                ui.click = None
            if self.outside_presentation(ui.click, ui):
                self.al.active_presentation = None
                self.al.active_minimap = None
                ui.click = None
            else:
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
        if self.from_dex and ui.m:
            ui.m = False
            want_to_launch_map(self.al, interest_point=(self.presented.x, self.presented.y))
        if self.al.ui.escape:
            self.al.active_presentation = None
            self.al.ui.escape = False

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

    def on_map(self, point, ui):
        if not point:
            return False
        x, y = point
        x1 = ui.percent_width(0.73)
        width = ui.percent_width(0.12)
        y1 = ui.percent_width(0.10)
        height = ui.percent_width(0.04)
        return x1 < x < x1 + width and y1 < y < y1 + height

    def draw_map_button(self):
        ui = self.al.ui
        screen = ui.screen
        x1 = ui.percent_width(0.73)
        width = ui.percent_width(0.12)
        y1 = ui.percent_width(0.10)
        height = ui.percent_width(0.04)
        color = (0, 255, 0) if self.selector_on_map else (0, 0, 0)
        thickness = 2 if self.selector_on_map else 1
        pygame.draw.rect(screen, (200, 200, 200), (x1, y1, width, height))
        pygame.draw.rect(screen, color, [x1, y1, width, height], thickness)
        screen.blit(
            ui.fonts.garuda24.render(" See on map", True, color), (x1, y1)
        )

    def draw(self):
        pass


class WordPresentation(Presentation):
    """
    An interactive screen that shows a word
    """

    def __init__(self, al, presented: Word, from_learning=False, from_dex=False):
        super().__init__()
        self.al = al
        self.presented = presented
        # parameters
        self.from_learning = from_learning
        self.from_dex = from_dex
        # drawing
        self.selector_on_sound = False
        self.selector_on_map = False
        # obtained from DB
        self.sentences = presented.get_sentences()
        self.selected_sentence_index = 0

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
        screen.blit(ui.fonts.garuda64.render(self.presented.thai, True, (0, 0, 0)), (x, y))

        # Draw English
        x = ui.percent_width(0.26)
        y = ui.percent_height(0.27)
        screen.blit(
            ui.fonts.garuda48.render(self.presented.english, True, (0, 0, 0)), (x, y)
        )

        if self.from_dex:
            self.draw_map_button()

        if self.from_dex:
            x = ui.percent_width(0.26)
            y += ui.percent_height(0.10)
            s = f"Level: {self.presented.level}  XP: {self.presented.total_xp}"
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


class LetterPresentation(Presentation):
    """
    An interactive screen that shows a letter
    """

    def __init__(self, al, presented: "Letter", from_learning=False, from_dex=False):
        super().__init__()
        self.al = al
        self.presented = presented
        # parameters
        self.from_learning = from_learning
        self.from_dex = from_dex
        # drawing
        self.selector_on_sound = False
        self.selector_on_map = False
        # Show the 10 most early words using that letter
        # self.words = presented.get_words()
        # self.selected_word_index = 0

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
        screen.blit(ui.fonts.garuda64.render(self.presented.thai, True, (0, 0, 0)), (x, y))

        # Draw English
        x = ui.percent_width(0.26)
        y = ui.percent_height(0.27)
        screen.blit(
            ui.fonts.garuda48.render(self.presented.english, True, (0, 0, 0)), (x, y)
        )

        if self.from_dex:
            self.draw_map_button()

        if self.from_dex:
            x = ui.percent_width(0.26)
            y += ui.percent_height(0.10)
            s = f"Level: {self.presented.level}  XP: {self.presented.total_xp}"
            screen.blit(ui.fonts.garuda16.render(s, True, (0, 0, 0)), (x, y))
