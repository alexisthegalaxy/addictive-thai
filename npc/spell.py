from typing import List

from direction import Direction
from models import get_item_from_name
from npc.npc import Npc


class Spell(Npc):
    def __init__(self, al, ma, x, y, direction=Direction.UP, color="white", name="spell"):
        super().__init__(
            al=al,
            name=name,
            ma=ma,
            x=x,
            y=y,
            direction=direction,
            sprite=color + '_spell',
            wobble=True,
        )

    # def process_dialog(self, al):
    #     for dialog in self.dialogs:
    #         for i, line in enumerate(dialog):
    #             dialog[i] = line.replace("[Name]", al.learner.name)
    #     if self.taught:
    #         self.review_dialog[0] = (
    #             self.review_dialog[0] + f" {self.taught.thai} ?"
    #         )

    # def special_interaction(self, al):
    #     if self.is_saying_last_sentence() and (self.active_dialog == self.vendor_dialog_beginning):
    #         from mechanics.sale import Sale
    #         # al.active_npc = None
    #         al.active_sale = Sale(al=al, vendor=self)
