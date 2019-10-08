import sqlite3
from bag.bag import Bag
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
        self.mas.form_links()
        self.cursor = sqlite3.connect("../thai.db").cursor()
        self.mas.al = self
        self.ui: Ui = ui
        self.learner = None
        self.cell_types = cell_types
        self.active_test: Test = None
        self.active_sale: "Sale" = None
        self.active_npc: "Npc" = None
        self.active_learning = None
        self.active_presentation = None
        self.active_battle = None
        self.active_sale = None
        self.dex: Dex = None
        self.active_minimap: Minimap = None
        self.bag: Bag = Bag()

    def tick_activity(self):
        # How we make the game check on things at every tick
        if self.active_battle:
            self.active_battle.tick()
            self.active_battle.opponent_play()
        for npc in self.mas.current_map.npcs:
            if npc.must_walk_to:
                npc.walked_float += self.ui.cell_size / 6
                if npc.walked_float >= self.ui.cell_size:
                    npc.walked_float = 0
                    npc.makes_a_step_towards_goal(self)
