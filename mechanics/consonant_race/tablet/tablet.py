import pygame

from mechanics.consonant_race.tablet.spell_actions import spell_action
from ui.keyboard import Keyboard


class Tablet(object):
    def __init__(self, al):
        self.al = al
        self.keyboard = Keyboard(ui=al.ui, y=al.ui.percent_height(0.64))
        self.answer = ""  # the string being typed
        self.rendered_answer = None

    def draw_background(self):
        ui = self.al.ui
        x = ui.percent_width(0.1)
        y = ui.percent_height(0.4)
        height = ui.percent_height(0.8)
        width = ui.percent_width(0.8)
        screen = ui.screen
        pygame.draw.rect(screen, (150, 150, 150), (x, y, width, height))
        pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)

    def draw(self):
        ui = self.al.ui
        screen = ui.screen

        # Draw the background
        # self.draw_background()

        # Draw answer
        if self.rendered_answer:
            x = ui.percent_width(0.5) - self.rendered_answer.get_width() / 2
            y = ui.percent_height(0.55)
            screen.blit(
                self.rendered_answer, (x, y)
            )

        if self.al.ui.is_shift():
            screen.blit(ui.images["shift_keyboard"], [self.keyboard.x, self.keyboard.y])
        else:
            screen.blit(ui.images["default_keyboard"], [self.keyboard.x, self.keyboard.y])

    def answer_got_modified(self):
        if self.answer:
            self.rendered_answer = self.al.ui.fonts.sarabun48.render(self.answer, True, (0, 0, 0))
        else:
            self.rendered_answer = None

    def validate_spell(self):
        spell_testing = True
        if spell_testing:
            spell_action(self.al, self.answer)
            self.close()
        else:
            for spell in self.al.bag.spells:
                if spell.name == self.answer:
                    spell_action(self.al, spell.name)
                    self.al.bag.reduce_item_quantity(spell.name)
                    self.close()
                    return
        # if no spell was found:
        print('self.answer', self.answer)
        if self.answer == "":
            self.close()

    def close(self):
        self.al.active_tablet = None

    def interact(self, al):
        if al.ui.enter:
            al.ui.enter = False
            self.validate_spell()
        self.keyboard.interact(self, al)

