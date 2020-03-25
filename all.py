import sqlite3
from bag.bag import Bag
from event import execute_event
from form_links import form_links
from lexicon.dex import Dex
from mechanics.minimap import Minimap
from ui.ui import Ui


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
        self.active_battle = None
        self.active_fight = None
        self.active_sale = None
        self.dex: Dex = None
        self.active_minimap: Minimap = None
        self.bag: Bag = Bag()

    def tick_activity(self):
        # Called at every tick
        if self.active_battle:
            self.active_battle.tick()
            self.active_battle.opponent_play()
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


"""
Problem:
    Just before turning, the NPC makes one step in the wrong direction.
Solution:
    When reaching the place you want to be at, change your direction to the correct one
"""