from enum import Enum
from typing import List

from bag.item import Item


class Compartment(Enum):
    BATTLE = 1
    OUT_OF_BATTLE = 2
    BONUS = 3
    QUEST = 4


class Bag(object):
    """
    A bag has four compartments:
        Battle items
        Out-of-battle items
        Bonus items (bike, swimming wear, train pass, etc.)
        Quest items (labelled as other)
    """
    def __init__(self):
        self.battle = []
        self.out_of_battle = []
        self.bonus = []
        self.quest = []

    def compartment_for_item(self, item: Item):
        if item.compartment == Compartment.BATTLE:
            return self.battle
        if item.compartment == Compartment.OUT_OF_BATTLE:
            return self.out_of_battle
        if item.compartment == Compartment.BONUS:
            return self.bonus
        if item.compartment == Compartment.QUEST:
            return self.quest

    def add_item(self, item: Item, quantity=0):
        item_added = False
        compartment_to_add_item_in = self.compartment_for_item(item)
        for compartment_item in compartment_to_add_item_in:
            if compartment_item.name == item.name:
                compartment_item.amount += quantity if quantity else item.amount
                item_added = True
        if not item_added:
            compartment_to_add_item_in.append(item)
            if quantity:
                compartment_to_add_item_in[-1].amount = quantity

    def get_all_items(self):
        return self.battle + self.out_of_battle + self.bonus + self.quest

    def get_quantities(self, item_list: List[Item]) -> List[int]:
        list_to_return = []
        for item in item_list:
            compartment = self.compartment_for_item(item)
            item_added = False
            for compartment_item in compartment:
                if compartment_item.name == item.name:
                    list_to_return.append(compartment_item.amount)
                    item_added = True
            if not item_added:
                list_to_return.append(0)
        return list_to_return

