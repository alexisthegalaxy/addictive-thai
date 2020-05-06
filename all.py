import sqlite3
from bag.bag import Bag
from direction import Direction
from event import execute_event
from follower import Follower
from form_links import form_links
from lexicon.dex import Dex
from mechanics.minimap import Minimap
from models import get_event_status
from ui.ui import Ui
from weather.weather import Weather, Overlay


class All:
    def __init__(
        self,
        mas: "Mas",
        ui: "Ui",
        cell_types: "CellType",
    ):
        from lexicon.tests.tests import Test

        self.mas = mas
        form_links(self.mas)
        self.cursor = sqlite3.connect("../thai.db").cursor()
        self.mas.al = self
        self.ui: Ui = ui
        self.learner = None
        self.cell_types = cell_types
        self.active_test: Test = None
        self.active_sale: "Sale" = None
        self.active_npc: "Npc" = None
        self.active_learning = None
        self.active_spell_identification = None
        self.active_presentation = None
        self.active_naming = None
        self.active_fight = None
        self.active_consonant_race = None
        self.active_sale = None
        self.dex: Dex = None
        self.lex: Lex = None
        self.active_minimap: Minimap = None
        self.bag: Bag = Bag()
        self.weather = Weather(al=self)

    def tick_activity(self):
        # Called at every tick
        self.weather.tick(self)
        if self.active_consonant_race:
            self.active_consonant_race.tick()
        if self.active_test and self.active_test.allowed_time:
            if self.active_test.is_timer_over():
                self.active_test.fails()
        for npc in self.mas.current_map.npcs:
            if npc.must_walk_to:
                npc.walked_float += self.ui.cell_size / 6
                if npc.walked_float >= self.ui.cell_size:
                    npc.walked_float = 0
                    npc.makes_a_step_towards_goal(self)
                    x, y = npc.x, npc.y
                    trigger = self.mas.current_map.get_cell_at(x, y).trigger
                    if trigger and npc.name in trigger.npcs:
                        execute_event(trigger.event, self)


# TODO put the following functions in a separate file
def letter_islands(al):
    if get_event_status("nim_is_following") == 1:
        al.learner.followers.append(
            Follower(
                al,
                direction=al.learner.direction,
                sprite='nim',
                name='Nim',
                x=al.learner.x,
                y=al.learner.y,
            )
        )
    if al.mas.current_map.filename == "ko_kut":
        if get_event_status("spirit_bird_is_beaten") == 1:
            from npc.import_npcs.ko_kut import spirit_bird_victory_callback
            spirit_bird_victory_callback(al)
        else:
            al.weather = Weather(
                al=al,
                rain=True,
                wind=30,
                overlay=Overlay(color=(30, 30, 30), transparency=92),
                lightning=True,
            )
    if al.mas.current_map.filename == "ko_mak":
        if get_event_status("spirit_gecko_is_beaten") == 1:
            from npc.import_npcs.ko_kut import spirit_bird_victory_callback
            spirit_bird_victory_callback(al)
        else:
            al.weather = Weather(
                al=al,
                # rain=True,
                # wind=30,
                # overlay=Overlay(color=(30, 30, 30), transparency=92),
                # lightning=True,
                quake=True,
            )


def sushi_is_following(al):
    if get_event_status("sushi_is_following") == 1:
        al.learner.followers.append(
            Follower(
                al,
                direction=Direction.DOWN,
                sprite='dog',
                name='ซูชิ',
                x=-1,
                y=-1,
            )
        )


def special_loading(al: All):
    letter_islands(al)
    sushi_is_following(al)