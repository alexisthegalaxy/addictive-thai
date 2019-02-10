import pygame


class Dex(object):
    def __init__(self, al):
        self.active = False
        self.al = al
        self.from_line = 0
        self.words_to_show = []
        self.word_count = len(self.words_to_show)
        self.determine_words_to_show()

    def determine_words_to_show(self):
        self.words_to_show = []
        for word in self.al.words.words:
            if word.total_xp > 0:
                self.words_to_show.append(word)

    def w(self):
        self.active = not self.active

    def interact(self):
        if self.al.ui.down:
            print("down")
            self.from_line = min(self.word_count, self.from_line + 1)
        if self.al.ui.up:
            print("up")
            self.from_line = max(0, self.from_line - 1)

    def draw(self):
        ui = self.al.ui
        g16 = ui.fonts.garuda16
        x = ui.percent_width(0.1)
        y = ui.percent_height(0.1)
        height = ui.percent_height(0.8)
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
        x = ui.percent_width(0.46)
        screen.blit(g16.render("Level", True, (0, 0, 0)), (x, y))
        x = ui.percent_width(0.60)
        screen.blit(g16.render("Experience", True, (0, 0, 0)), (x, y))

        y = ui.percent_height(0.15)
        for i, word in enumerate(self.words_to_show):
            if 0 <= i - self.from_line < 15:
                x = ui.percent_width(0.12)
                screen.blit(g16.render(word.thai, True, (0, 0, 0)), (x, y))
                x = ui.percent_width(0.28)
                screen.blit(g16.render(word.english, True, (0, 0, 0)), (x, y))
                x = ui.percent_width(0.46)
                screen.blit(g16.render(str(word.level), True, (0, 0, 0)), (x, y))
                x = ui.percent_width(0.60)
                screen.blit(g16.render(str(word.total_xp), True, (0, 0, 0)), (x, y))
                y += ui.percent_width(0.03)
