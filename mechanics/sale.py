from bag.item import Item
from npc.vendor import Vendor
import pygame


class Sale(object):
    def __init__(self, al, vendor: Vendor):
        self.al = al
        self.vendor = vendor
        self.quantities = None
        self.update_quantities()

        # UI
        self.x = al.ui.percent_width(0.07)
        self.y = al.ui.percent_height(0.07)
        self.height = al.ui.percent_height(0.86)
        self.width = al.ui.percent_width(0.86)
        self.from_line = 0

        self.selector = 0
        self.max_items_to_show = 7
        self.number_of_items = len(vendor.sold_items)

    def update_quantities(self):
        self.quantities = self.al.bag.get_quantities(self.vendor.sold_items)

    def draw_selector(self):
        ui = self.al.ui
        x = ui.percent_width(0.1)
        y = ui.percent_width(0.1) + self.selector * ui.percent_width(0.04)
        ui.screen.blit(ui.images["selection_arrow"], [x, y])

    def draw(self):
        ui = self.al.ui
        g16 = ui.fonts.garuda24
        screen = ui.screen
        pygame.draw.rect(
            screen, (200, 200, 200), (self.x, self.y, self.width, self.height)
        )
        pygame.draw.rect(
            screen, (0, 0, 0), [self.x, self.y, self.width, self.height], 1
        )

        # Draw header
        y = ui.percent_height(0.11)
        x = ui.percent_width(0.12)
        screen.blit(g16.render("Item", True, (0, 0, 0)), (x, y))
        x = ui.percent_width(0.28)
        screen.blit(g16.render("Description", True, (0, 0, 0)), (x, y))
        x = ui.percent_width(0.70)
        screen.blit(g16.render("Price", True, (0, 0, 0)), (x, y))
        x = ui.percent_width(0.80)
        screen.blit(g16.render("In bag", True, (0, 0, 0)), (x, y))

        y = ui.percent_height(0.15)
        for i, item in enumerate(self.vendor.sold_items):
            if 0 <= i - self.from_line < 15:
                x = ui.percent_width(0.12)
                screen.blit(g16.render(item.name, True, (0, 0, 0)), (x, y))
                x = ui.percent_width(0.28)
                screen.blit(g16.render(item.description, True, (0, 0, 0)), (x, y))
                x = ui.percent_width(0.70)
                screen.blit(g16.render(f"{str(item.price)}฿", True, (0, 0, 0)), (x, y))
                x = ui.percent_width(0.80)
                screen.blit(g16.render(str(self.quantities[i]), True, (0, 0, 0)), (x, y))
                y += ui.percent_width(0.04)
        self.draw_selector()

    def try_to_buy_item(self, item, quantity):
        if item.price * quantity <= self.al.learner.money:
            self.al.learner.money -= item.price * quantity
            self.al.bag.add_item(item, quantity=quantity)
            self.update_quantities()

    def get_selected_item(self) -> Item:
        return self.vendor.sold_items[self.selector]

    def interact(self, al):
        if al.ui.up:
            al.ui.up = False
            self.selector = max(self.selector - 1, 0)
        if al.ui.down:
            al.ui.down = False
            self.selector = min(self.selector + 1, self.number_of_items - 1)
        # if al.ui.down:
        #     al.ui.down = False
        #     if self.selector_on_sound:
        #         self.selector_on_sound = False
        #         self.selected_option_index = 0
        #     else:
        #         self.selected_option_index += 2
        #         if self.selected_option_index >= (self.number_of_distr + 1):
        #             self.selector_on_sound = True
        # if al.ui.left or al.ui.right:
        #     self.selected_option_index += (
        #         1 if self.selected_option_index % 2 == 0 else -1
        #     )
        #     al.ui.left = False
        #     al.ui.right = False
        if al.ui.space:
            al.ui.space = False
            self.try_to_buy_item(item=self.get_selected_item(), quantity=1)
            # if self.selector_on_sound:
            #     play_transformed_thai_word(self.correct_word.thai)
            # else:
            #     self.learner_select_option()
