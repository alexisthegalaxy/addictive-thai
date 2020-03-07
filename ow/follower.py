import pygame
import time

from movement import Movement
from ow.direction import Direction, dir_equal, string_from_direction, opposite_direction
from ow.overworld import CellTypes
from sounds.play_sound import play_thai_word


class Follower(object):
    def __init__(self, al, direction, sprite, name, x=8, y=12, color=(150, 0, 0)):
        self.al: "All" = al
        self.name = name
        self.sprite = sprite
        # self.must_wait = 0.1
        # self.last_movement = time.time()
        self.x = x
        self.y = y
        self.color = color
        self.direction = Direction.DOWN
        self.last_healing_place = (8, 12, self.al.mas.house_learner_f2)
        self.movement: Movement = None

    # def draw(self, al):
    #     cell_size = al.ui.cell_size
    #     if cell_size == 30:
    #         x = 19 * al.ui.cell_size
    #         y = 10 * al.ui.cell_size
    #     elif cell_size == 60:
    #         x = 10 * al.ui.cell_size
    #         y = 5 * al.ui.cell_size
    #     else:  # cell_size == 80:
    #         x = 7 * al.ui.cell_size
    #         y = 4 * al.ui.cell_size
    #     sprite_name = f"{self.sprite}_{string_from_direction(self.direction)}"
    #     if sprite_name in al.ui.npc_sprites:
    #         sprite = al.ui.npc_sprites[sprite_name]
    #         al.ui.screen.blit(sprite, [x, y])
    #     else:
    #         pygame.draw.rect(
    #             al.ui.screen,
    #             self.color,
    #             pygame.Rect(x, y, al.ui.cell_size, al.ui.cell_size),
    #         )

    # def move(self, al: "All"):
    #     has_moved = False
    #     next_x = self.x
    #     next_y = self.y
    #
    #     if al.ui.up:
    #         next_y -= 1
    #         self.direction = Direction.UP
    #     elif al.ui.down:
    #         next_y += 1
    #         self.direction = Direction.DOWN
    #     elif al.ui.left:
    #         next_x -= 1
    #         self.direction = Direction.LEFT
    #     elif al.ui.right:
    #         next_x += 1
    #         self.direction = Direction.RIGHT
    #
    #     next_position_walkable = True
    #
    #     # Check for walls:
    #     next_cell = al.mas.current_map.get_cell_at(next_x, next_y)
    #     if not next_cell.walkable():
    #         next_position_walkable = False
    #     if next_position_walkable and next_cell.typ.name == "cave_0011" and self.direction == Direction.DOWN:
    #         next_position_walkable = False
    #     if next_position_walkable and (next_cell.typ.name == "stairs_up" or next_cell.typ.name == "stairs_down") and (self.direction == Direction.RIGHT or self.direction == Direction.LEFT):
    #         next_position_walkable = False
    #     if next_position_walkable:
    #         current_cell = al.mas.current_map.get_cell_at(self.x, self.y)
    #         if current_cell.typ.name == "cave_0011" and self.direction == Direction.UP:
    #             next_position_walkable = False
    #     # Check for npcs:
    #     if next_position_walkable:
    #         for npc in al.mas.current_map.npcs:
    #             if npc.x == next_x and npc.y == next_y and npc.should_appear():
    #                 next_position_walkable = False
    #                 break
    #
    #     if next_position_walkable:
    #         has_moved = next_x != self.x or next_y != self.y
    #         self.x = next_x
    #         self.y = next_y
    #         self.movement = Movement(self.direction, self)
    #
    #     if has_moved:
    #         self.al.mas.current_map.response_to_movement(self, self.x, self.y)
    #         self.free_steps -= 1
    #         self.last_movement = time.time()

    # def can_move(self):
    #     return time.time() - self.last_movement > self.must_wait
