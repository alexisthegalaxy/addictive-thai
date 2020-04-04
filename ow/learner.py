import pygame
import time

from all import All
from models import set_as_active_player
from movement import Movement
from ow.direction import Direction, dir_equal, string_from_direction, opposite_direction
from ow.overworld import CellTypes
from sounds.play_sound import play_thai_word


class Learner(object):
    def __init__(self, al, name, x=8, y=12, color=(150, 0, 150), learns_letters=True, gender=1):
        self.name = name
        self.gender = gender
        set_as_active_player(name, gender, learns_letters)
        self.sprite = self.name.lower()
        self.money = 5
        self.learns_letters = learns_letters
        self.max_hp = 1
        self.must_wait = 0.1
        self.hp = self.max_hp
        self.x = x
        self.y = y
        self.color = color
        self.last_movement = time.time()
        self.direction = Direction.DOWN
        self.al: "All" = al
        self.max_free_steps = 3
        self.free_steps = self.max_free_steps
        self.last_healing_place = (8, 12, self.al.mas.house_learner_f2)
        self.movement: Movement = None
        self.followers = []

    def draw(self, al):
        cell_size = al.ui.cell_size
        if cell_size == 30:
            x = 19 * al.ui.cell_size
            y = 10 * al.ui.cell_size
        elif cell_size == 60:
            x = 10 * al.ui.cell_size
            y = 5 * al.ui.cell_size
        else:  # cell_size == 80:
            x = 7 * al.ui.cell_size
            y = 4 * al.ui.cell_size

        x += al.weather.get_offset_x()
        y += al.weather.get_offset_y()

        sprite_name = f"{self.sprite}_{string_from_direction(self.direction)}"
        if sprite_name in al.ui.npc_sprites:
            sprite = al.ui.npc_sprites[sprite_name]
            al.ui.screen.blit(sprite, [x, y])
        else:
            pygame.draw.rect(
                al.ui.screen,
                self.color,
                pygame.Rect(x, y, al.ui.cell_size, al.ui.cell_size),
            )

        for follower in self.followers:
            follower.draw(al)

    def draw_money(self, al, x=None, y=None):
        color = (0, 0, 0)
        rendered = al.ui.fonts.garuda32.render(str(self.money) + "฿", True, color)
        if not x:
            x = al.ui.width - rendered.get_width() - 5
        if not y:
            y = 20
        al.ui.screen.blit(rendered, (x, y))

    def draw_money_and_hp(self, al):
        x = al.ui.width - self.max_hp * 40
        y = 0
        width = self.max_hp * 40
        height = 80
        black = (0, 0, 0)
        grey = (150, 150, 150)
        pygame.draw.rect(al.ui.screen, black, (x, y, width, height))
        pygame.draw.rect(al.ui.screen, grey, (x + 1, y, width, height - 1))

        self.draw_money(al)
        draw_hp(al, self.hp, self.max_hp)

    def move(self, al: "All"):
        has_moved = False
        next_x = self.x
        next_y = self.y
        self.previous_x = self.x
        self.previous_y = self.y

        if al.ui.up:
            next_y -= 1
            self.direction = Direction.UP
        elif al.ui.down:
            next_y += 1
            self.direction = Direction.DOWN
        elif al.ui.left:
            next_x -= 1
            self.direction = Direction.LEFT
        elif al.ui.right:
            next_x += 1
            self.direction = Direction.RIGHT

        next_position_walkable = True

        # Check for walls:
        next_cell = al.mas.current_map.get_cell_at(next_x, next_y)
        if not next_cell.walkable():
            next_position_walkable = False
        if next_position_walkable and next_cell.typ.name == "cave_0011" and self.direction == Direction.DOWN:
            next_position_walkable = False
        if next_position_walkable and (next_cell.typ.name == "stairs_up" or next_cell.typ.name == "stairs_down") and (self.direction == Direction.RIGHT or self.direction == Direction.LEFT):
            next_position_walkable = False
        if next_position_walkable:
            current_cell = al.mas.current_map.get_cell_at(self.x, self.y)
            if current_cell.typ.name == "cave_0011" and self.direction == Direction.UP:
                next_position_walkable = False
        # Check for npcs:
        if next_position_walkable:
            for npc in al.mas.current_map.npcs:
                if npc.x == next_x and npc.y == next_y and npc.should_appear() and not npc.is_walkable:
                    next_position_walkable = False
                    break

        if next_position_walkable:
            has_moved = next_x != self.x or next_y != self.y
            self.x = next_x
            self.y = next_y
            self.movement = Movement(self.direction, self)

        if has_moved:
            self.al.mas.current_map.response_to_movement(self, self.x, self.y)
            self.free_steps -= 1
            self.last_movement = time.time()

            previous_x = self.previous_x
            previous_y = self.previous_y
            for follower in self.followers:
                follower.move(al, previous_x, previous_y)
                previous_x = follower.previous_x
                previous_y = follower.previous_y

        # check for trainers seeing the learner
        for npc in al.mas.current_map.npcs:
            if (npc.is_trainer() or npc.wanna_meet) and npc.wants_battle and not npc.must_walk_to and not al.active_npc:
                must_walk_to = npc.sees_learner(al)
                if must_walk_to:
                    npc.gets_exclamation_mark()
                    npc.must_walk_to = must_walk_to
                    if npc.must_walk_to[0].x == npc.x and npc.must_walk_to[0].y == npc.y:
                        npc.must_walk_to.pop(0)
                        al.learner.direction = opposite_direction(npc.direction)
                        npc.interact(al)


    def open(self):
        x, y = self.next_position()
        cell_in_front = self.al.mas.current_map.get_cell_at(x, y)
        if cell_in_front.walkable():
            cell_in_front.typ = CellTypes.wall
        else:
            cell_in_front.typ = CellTypes.path

    def next_position(self):
        next_x = self.x
        next_y = self.y
        if dir_equal(self.direction, Direction.UP):
            next_y -= 1
        if dir_equal(self.direction, Direction.DOWN):
            next_y += 1
        if dir_equal(self.direction, Direction.LEFT):
            next_x -= 1
        if dir_equal(self.direction, Direction.RIGHT):
            next_x += 1

        return next_x, next_y

    def next_next_position(self):
        next_next_x = self.x
        next_next_y = self.y

        if dir_equal(self.direction, Direction.UP):
            next_next_y -= 2
        if dir_equal(self.direction, Direction.DOWN):
            next_next_y += 2
        if dir_equal(self.direction, Direction.LEFT):
            next_next_x -= 2
        if dir_equal(self.direction, Direction.RIGHT):
            next_next_x += 2

        return next_next_x, next_next_y

    def start_interacting_with_npcs(self, al: All):
        if self.al.active_npc:
            self.al.active_npc.interact(al)
            return
        next_x, next_y = self.next_position()
        for npc in al.mas.current_map.npcs:
            if npc.x == next_x and npc.y == next_y:
                npc.interact(al)
                return
        next_next_x, next_next_y = self.next_next_position()
        for npc in al.mas.current_map.npcs:
            if npc.x == next_next_x and npc.y == next_next_y:
                npc.interact(al)
                return

    def start_interacting(self, al: All):
        al.ui.space = False
        self.start_interacting_with_npcs(al)

    def can_move(self):
        return time.time() - self.last_movement > self.must_wait

    def print_location(self):
        print(f"location: {self.al.mas.current_map.filename} ({self.x}, {self.y})"
              f"({self.x + self.al.mas.current_map.x_shift}, {self.y + self.al.mas.current_map.y_shift})")

    def hurt(self, damage):
        self.hp = max(self.hp - damage, 0)
        if self.hp == 0:
            self.faints()

    def faints(self):
        x, y, ma = self.last_healing_place
        self.teleport(x, y, ma)
        self.al.active_test = None
        self.al.active_fight = None
        self.al.active_npc = None
        self.al.active_learning = None
        self.hp = self.max_hp
        self.money = int(self.money / 2)

    def teleport(self, x, y, ma):
        self.x = x
        self.y = y
        self.al.mas.current_map = ma

    def inn_heal(self):
        self.hp = self.max_hp
        self.last_healing_place = (self.x, self.y, self.al.mas.current_map)
        play_thai_word("heal")

    def bed_heal(self):
        self.hp = self.max_hp
        self.last_healing_place = (self.x, self.y, self.al.mas.current_map)

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)
        play_thai_word("heal")


def draw_hp(al, hp, max_hp, x=None, y=0):
    if hp < 0:
        hp = 0
    rounded_hp = round(hp*8)/8
    decimal_part = round(rounded_hp - int(rounded_hp), 3)
    heart_index = int(decimal_part * 8)
    if heart_index == 0:
        heart_index = 8
    last_full_heart_image = al.ui.images[f"heart_{heart_index}"]

    full_hearts = int(rounded_hp) + (1 if decimal_part > 0 else 0)
    empty_hearts = max_hp - full_hearts
    if not x:
        x = al.ui.width - 40
    for i in range(empty_hearts):
        al.ui.screen.blit(al.ui.images["heart_0"], [x, y])
        x -= 40
    for i in range(full_hearts):
        if i == 0:
            al.ui.screen.blit(last_full_heart_image, [x, y])
        else:
            al.ui.screen.blit(al.ui.images["heart_8"], [x, y])
        x -= 40
