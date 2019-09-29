import pygame
import time

from all import All
from movement import Movement
from ow.direction import Direction, dir_equal, string_from_direction, opposite_direction
from ow.overworld import CellTypes
from sounds.play_sound import play_thai_word


class Learner(object):
    def __init__(self, al, x=45, y=9, color=(150, 0, 150)):
        self.name = "Alexis"
        self.sprite = self.name.lower()
        self.money = 5
        self.max_hp = 5
        self.must_wait = 0.1
        self.hp = self.max_hp
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.last_movement = time.time()
        self.direction = Direction.DOWN
        self.al: "All" = al
        self.max_free_steps = 3
        self.free_steps = self.max_free_steps
        self.last_healing_place = (28, 92, self.al.mas.chaiyaphum)
        self.movement: Movement = None
        self.follower = None

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

    def draw_money(self, al):
        color = (0, 0, 0)
        rendered = al.ui.fonts.garuda32.render(str(self.money) + "฿", True, color)
        x = al.ui.width - rendered.get_width() - 5
        y = 20
        al.ui.screen.blit(rendered, (x, y))

    def draw_hp(self, al):
        full_hearts = self.hp
        empty_hearts = self.max_hp - self.hp
        x = al.ui.width - 40
        for i in range(empty_hearts):
            al.ui.screen.blit(al.ui.images["empty_heart"], [x, 0])
            x -= 40
        for i in range(full_hearts):
            al.ui.screen.blit(al.ui.images["full_heart"], [x, 0])
            x -= 40

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
        self.draw_hp(al)

    def move(self, al: "All"):
        has_moved = False
        next_x = self.x
        next_y = self.y

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
        if next_position_walkable:
            current_cell = al.mas.current_map.get_cell_at(self.x, self.y)
            if current_cell.typ.name == "cave_0011" and self.direction == Direction.UP:
                next_position_walkable = False
        # Check for npcs:
        if next_position_walkable:
            for npc in al.mas.current_map.npcs:
                if npc.x == next_x and npc.y == next_y and npc.should_appear():
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

        # check for trainers seeing the learner
        for npc in al.mas.current_map.npcs:
            if (npc.is_trainer() or npc.wanna_meet) and npc.wants_battle and not npc.must_walk_to and not al.active_npc:
                must_walk_to = npc.sees_learner(al)
                if must_walk_to:
                    npc.gets_exclamation_mark()
                    npc.must_walk_to = must_walk_to
                    if npc.must_walk_to.x == npc.x and npc.must_walk_to.y == npc.y:
                        npc.must_walk_to = None
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
        print(f"location: {self.al.mas.current_map.filename} ({self.x}, {self.y})")

    def hurt(self, damage):
        self.hp = max(self.hp - damage, 0)
        if self.hp == 0:
            self.faints()

    def faints(self):
        x, y, ma = self.last_healing_place
        self.teleport(x, y, ma)
        self.al.active_test = None
        self.al.active_battle = None
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
