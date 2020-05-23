import sqlite3

from bag.item import Item
from direction import Direction
from models import get_active_learner_id
from npc.npc import Npc, _process_dialog


def color_from_tones(tones):
    if tones[0] == "M":
        return "grey"
    if tones[0] == "L":
        return "black"
    if tones[0] == "F":
        return "red"
    if tones[0] == "H":
        return "white"
    if tones[0] == "R":
        return "rising"

class Spell(Npc):
    def __init__(self, al, ma, x, y, direction=Direction.UP, name="spell", word=None):
        from lexicon.items import Word

        if not word:
            assert False
        super().__init__(
            al=al,
            name=name,
            ma=ma,
            x=x,
            y=y,
            direction=direction,
            sprite='spell_' + color_from_tones(word.tones),
            wobble=True,
            standard_dialog=["The Spell comes closer... and attacks!"],
            defeat_dialog=["You caught the spell!"],
        )
        self.word: Word = word

    def process_dialog(self, al):
        for dialog in self.dialogs:
            _process_dialog(dialog, al)
            # for i, line in enumerate(dialog):
            #     dialog[i] = line.replace("[Name]", al.learner.name)
        if self.taught:
            self.review_dialog[0] = (
                self.review_dialog[0] + f" {self.taught.thai} ?"
            )

    def gets_caught(self):
        self.switch_to_dialog(self.defeat_dialog)

    def special_interaction(self, al):
        super().special_interaction(al)
        from lexicon.spell_identification import SpellIdentification
        if self.is_saying_last_sentence():
            if self.active_dialog == self.defeat_dialog:
                al.mas.current_map.npcs = [npc for npc in al.mas.current_map.npcs if npc != self]
                # TODO USER ITEM
                al.bag.add_item(Item('ลม', durability=100), quantity=1)
            else:
                al.active_spell_identification = SpellIdentification(al=al, spell=self)


def get_spells_of_player():
    """returns all the spells that a player has right now"""
    CONN = sqlite3.connect("thai.db")
    CURSOR = CONN.cursor()
    learner_id = get_active_learner_id()
    results = list(
        CURSOR.execute(
            f"SELECT item_id "
            f"FROM user_items "
            f"WHERE user_id = '{learner_id}' AND is_spell and durability > 0"
        )
    )
    return results and results[0]

