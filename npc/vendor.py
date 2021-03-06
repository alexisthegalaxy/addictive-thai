from typing import List

from direction import Direction
from models import get_item_from_name
from npc.npc import Npc, _process_dialog


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
        sold_items: List[str] = None,
    ):
        super().__init__(
            al=al, name=name, ma=ma, x=x, y=y, direction=direction, sprite=sprite
        )
        self.vendor_dialog_beginning = vendor_dialog_beginning
        self.vendor_dialog_end = vendor_dialog_end or ["Hope to see you again!"]
        self.sold_items = [get_item_from_name(item_name) for item_name in sold_items]
        # self.sold_items = sold_items
        self.active_dialog: List[str] = self.vendor_dialog_beginning

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
        if self.is_saying_last_sentence() and (self.active_dialog == self.vendor_dialog_beginning):
            from mechanics.sale import Sale
            # al.active_npc = None
            al.active_sale = Sale(al=al, vendor=self)

