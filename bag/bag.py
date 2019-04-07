from enum import Enum
from typing import List

from bag.item import Item


class Compartment(Enum):
    BATTLE_ITEMS = 1
    OUT_OF_BATTLE_ITEMS = 2
    BONUS_ITEMS = 3
    QUEST_ITEMS = 4


class Bag(object):
    """
    A bag has four compartments:
        Battle items
        Out-of-battle items
        Bonus items (bike, swimming wear, train pass, etc.)
        Quest items (labelled as other)
    """
    def __init__(self):
        self.battle_items = []
        self.out_of_battle_items = []
        self.bonus_items = []
        self.quest_items = []

    def compartment_for_item(self, item: Item):
        if item.compartment == Compartment.BATTLE_ITEMS:
            return self.battle_items
        if item.compartment == Compartment.OUT_OF_BATTLE_ITEMS:
            return self.out_of_battle_items
        if item.compartment == Compartment.BONUS_ITEMS:
            return self.bonus_items
        if item.compartment == Compartment.QUEST_ITEMS:
            return self.quest_items

    def add_item(self, item: Item, quantity=0):
        compartment_to_add_item_in = self.compartment_for_item(item)
        item_added = False
        for compartment_item in compartment_to_add_item_in:
            if compartment_item.name == item.name:
                compartment_item.amount += quantity if quantity else item.amount
                item_added = True
        if not item_added:
            compartment_to_add_item_in.append(item)
            if quantity:
                compartment_to_add_item_in[-1].amount = quantity

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

