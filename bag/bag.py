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
    """
    def __init__(self):
        self.items = []

    def add_item(self, item: Item, quantity=0):
        item_added = False
        for item in self.items:
            if item.name == item.name:
                item.amount += quantity if quantity else item.amount
                item_added = True
        if not item_added:
            self.items.append(item)
            if quantity:
                self.items[-1].amount = quantity

    def remove_item(self, item_name: 'name', quantity=1):
        for item in self.items:
            if item.name == item.name:
                item.amount -= quantity

    def get_quantities(self, item_list: List[Item]) -> List[int]:
        list_to_return = []
        for item in item_list:
            item_added = False
            for item_in_bag in self.items:
                if item_in_bag.name == item.name:
                    list_to_return.append(item_in_bag.amount)
                    item_added = True
            if not item_added:
                list_to_return.append(0)
        return list_to_return

    def get_item_quantity(self, item_name):
        for item_in_bag in self.items:
            if item_in_bag.name_id == item_name:
                return item_in_bag.amount
        return 0



