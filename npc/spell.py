from direction import Direction
from npc.npc import Npc, _process_dialog


class Spell(Npc):
    def __init__(self, al, ma, x, y, direction=Direction.UP, color="white", name="spell", word=None):
        super().__init__(
            al=al,
            name=name,
            ma=ma,
            x=x,
            y=y,
            direction=direction,
            sprite=color + '_spell',
            wobble=True,
            standard_dialog=["The Spell comes closer...", "...and attacks!"],
        )
        self.word = word

    def process_dialog(self, al):
        for dialog in self.dialogs:
            _process_dialog(dialog, al)
            # for i, line in enumerate(dialog):
            #     dialog[i] = line.replace("[Name]", al.learner.name)
        if self.taught:
            self.review_dialog[0] = (
                self.review_dialog[0] + f" {self.taught.thai} ?"
            )

    def special_interaction(self, al):
        super().special_interaction(al)
        from lexicon.spell_identification import SpellIdentification
        if self.is_saying_last_sentence():
            al.active_spell_identification = SpellIdentification(al=al, spell=self)
