from typing import List

from bag.item import Item
from direction import Direction
from npc.npc import Npc


class Vendor(Npc):
    def __init__(
        self,
        al,
        name,
        ma,
        x,
        y,
        vendor_dialog_beginning=None,
        vendor_dialog_end=None,
        direction=Direction.UP,
        sprite="vendor",
        sold_items: List[Item] = None,
    ):
        super().__init__(
            al=al, name=name, ma=ma, x=x, y=y, direction=direction, sprite=sprite
        )
        self.vendor_dialog_beginning = vendor_dialog_beginning
        self.vendor_dialog_end = vendor_dialog_end
        self.sold_items = sold_items
        self.active_dialog: List[str] = self.vendor_dialog_beginning

    def process_dialog(self, al):
        for dialog in self.dialogs:
            for i, line in enumerate(dialog):
                dialog[i] = line.replace("[Name]", al.learner.name)
        if self.taught_word:
            self.review_dialog[0] = (
                self.review_dialog[0] + f" {self.taught_word.thai} ?"
            )

    def special_interaction(self, al):
        if self.is_saying_last_sentence() and (self.active_dialog == self.vendor_dialog_beginning):
            from mechanics.sale import Sale
            # al.active_npc = None
            al.active_sale = Sale(al=al, vendor=self)
            # al.active_battle.goes_to_first_step()

