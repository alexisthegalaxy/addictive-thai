import sqlite3
from bag.bag import Bag
from lexicon.dex import Dex
from models import get_current_map
from ui.ui import Ui


class All:
    def __init__(
        self,
        mas: "Mas",
        ui: "Ui",
        cell_types: "CellType",
        profiles: "Profile",
    ):
        from lexicon.tests.tests import Test

        self.mas = mas
        self.cursor = sqlite3.connect("../thai.db").cursor()
        self.mas.al = self
        self.ui: Ui = ui
        self.learner = None
        self.cell_types = cell_types
        self.profiles = profiles
        self.active_test: Test = None
        self.active_sale: "Sale" = None
        self.active_npc: "Npc" = None
        self.active_learning = None
        self.active_presentation = None
        self.active_battle = None
        self.active_sale = None
        self.dex: Dex = None
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

    def __getstate__(self):
        """Return state values to be pickled."""
        state = self.__dict__.copy()
        del state["mas"]
        del state["ui"]
        del state["cell_types"]
        del state["profiles"]
        del state["active_test"]
        del state["active_sale"]
        del state["active_battle"]
        del state["active_learning"]
        del state["active_npc"]
        del state["dex"]
        del state["cursor"]
        current_map = get_current_map(self)
        state["current_map"] = current_map
        learner = {
            "color": self.learner.color,
            "direction": self.learner.direction,
            "free_steps": self.learner.free_steps,
            "hp": self.learner.hp,
            "last_healing_place": {
                "x": self.learner.last_healing_place[0],
                "y": self.learner.last_healing_place[1],
                "map_name": self.learner.last_healing_place[2].filename,
            },
            "last_movement": self.learner.last_movement,
            "last_saved": self.learner.last_saved,
            "max_free_steps": self.learner.max_free_steps,
            "max_hp": self.learner.max_hp,
            "money": self.learner.money,
            "must_wait": self.learner.must_wait,
            "name": self.learner.name,
            "x": self.learner.x,
            "y": self.learner.y,
        }
        state["learner"] = learner

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Add baz back since it doesn't exist in the pickle
        self.baz = 0
