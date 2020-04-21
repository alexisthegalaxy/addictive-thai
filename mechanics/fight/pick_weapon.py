import random
import time

from lexicon.items import Word
from lexicon.tests.tests import TestAnswerBox, draw_box
from mechanics.fight.fight_steps import FightStep
from mechanics.fight.tones_effects import get_explanatory_effects_from_tone
from models import get_least_known_known_words


class ExplanatoryBox(object):
    def __init__(self, al, x, y, index, word: Word):
        self.al = al
        self.x = x
        self.y = y
        self.index = index
        self.word = word
        self.width = al.ui.percent_width(0.4)
        self.height = al.ui.percent_height(0.15)
        tones_parameters = get_explanatory_effects_from_tone(
            self.word.tones
        )

        self.tone_name = tones_parameters["tone_name"]
        self.test_type = tones_parameters["test_type"]
        self.test_description = tones_parameters["test_description"]
        self.bg_color = tones_parameters["bg_color"]
        self.color = tones_parameters["color"]
        self.effects = tones_parameters["effects"]

        # self.tone_name = tones_parameters.get("tone_name", "empty")
        # tone_name, test_type, test_description, bg_color, color
        # self.tone_name = tone_name
        # self.test_type = test_type
        # self.test_description = test_description
        # self.bg_color = bg_color
        # self.color = color

    def draw(self):
        screen = self.al.ui.screen
        fonts = self.al.ui.fonts
        draw_box(
            screen,
            fonts,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            strings=[f"{self.tone_name} - {self.test_type}"] + self.test_description,
            bg=self.bg_color,
            default_color=self.color,
            font_size=16,
            thickness=1,
        )

    def contains(self, point):
        (x, y) = point
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height


class PickWeapon(object):
    def __init__(self, al, fight, attack_phase):
        self.draw_text_since = time.time()
        self.al = al
        self.fight = fight
        self.attack_phase = attack_phase
        self.selected_words = self.fight.player.word_cards
        self.hovered_option_index = -1

        self.boxes = [
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(0.24),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.12),
                string=self.selected_words[0].thai,
                index=0,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(0.40),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.12),
                string=self.selected_words[1].thai,
                index=1,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(0.56),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.12),
                string=self.selected_words[2].thai,
                index=2,
            ),
            TestAnswerBox(
                x=al.ui.percent_width(0.15),
                y=al.ui.percent_height(0.72),
                width=al.ui.percent_width(0.32),
                height=al.ui.percent_height(0.12),
                string=self.selected_words[3].thai,
                index=3,
            ),
        ]

        self.explanatory_boxes = [
            ExplanatoryBox(
                al=al,
                x=al.ui.percent_width(0.5),
                y=al.ui.percent_height(0.24),
                index=0,
                word=self.selected_words[0]
            ),
            ExplanatoryBox(
                al=al,
                x=al.ui.percent_width(0.5),
                y=al.ui.percent_height(0.40),
                index=1,
                word=self.selected_words[1]
            ),
            ExplanatoryBox(
                al=al,
                x=al.ui.percent_width(0.5),
                y=al.ui.percent_height(0.56),
                index=2,
                word=self.selected_words[2]
            ),
            ExplanatoryBox(
                al=al,
                x=al.ui.percent_width(0.5),
                y=al.ui.percent_height(0.72),
                index=3,
                word=self.selected_words[3]
            ),
        ]

    def draw(self):
        ui = self.al.ui
        # Draw "What's the Thai word for"
        explanatory_string = "Select which word to create a test about."
        x = ui.percent_width(0.12)
        y = ui.percent_height(0.12)
        ui.screen.blit(ui.fonts.sarabun32.render(explanatory_string, True, (0, 0, 0)), (x, y))

        for i, box in enumerate(self.boxes):
            box.draw(
                self.al.ui.screen,
                self.al.ui.fonts,
                selected=self.hovered_option_index == i,
            )
        if not self.hovered_option_index == -1:
            self.explanatory_boxes[self.hovered_option_index].draw()

    def interact(self):
        if self.al.ui.hover:
            self.hovered_option_index = -1
            for i, box in enumerate(self.boxes):
                if box.contains(self.al.ui.hover):
                    self.hovered_option_index = i
                    break
            self.al.ui.hover = None
        if self.al.ui.click:
            for i, box in enumerate(self.boxes):
                if box.contains(self.al.ui.click):
                    self.picks_weapon(self.selected_words[i], self.explanatory_boxes[i].effects)
                    break
            self.al.ui.click = None

    def picks_weapon(self, selected_word: Word, effects):
        self.attack_phase.chosen_weapon = selected_word
        self.attack_phase.chosen_weapon_effects = effects
        self.fight.current_step = FightStep.ATTACK_PHASE_TEST.value
        self.attack_phase.draw_text_since = time.time()

        # remove the card from the player's cards
        new_cards = [word_card for word_card in self.fight.player.word_cards if word_card.split_form != selected_word.split_form]
        old_cards_split_forms = [word_card.split_form for word_card in self.fight.player.word_cards]
        least_known_known_words = get_least_known_known_words(number_of_words_to_get=20)
        new_word = random.choice(least_known_known_words)
        while new_word.split_form in old_cards_split_forms:
            new_word = random.choice(least_known_known_words)
        new_cards.append(new_word)
        self.fight.player.word_cards = new_cards
