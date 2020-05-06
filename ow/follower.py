import pygame
import time

from ow.direction import Direction, dir_equal, string_from_direction


class Follower(object):
    def __init__(self, al, direction, sprite, name, x=8, y=12):
        self.al: "All" = al
        self.name = name
        self.sprite = sprite
        self.last_movement = time.time()
        self.x = x
        self.y = y
        self.previous_x = x
        self.previous_y = y
        self.direction = direction

    def draw(self, al):
        progressive_offset = 1.05 * (time.time() - self.last_movement) / al.learner.must_wait
        learner_movement_offset_x, learner_movement_offset_y = al.learner.movement.get_offset() if al.learner.movement else (0, 0)
        center_x = 7
        center_y = 4

        x = self.x - al.learner.x + center_x
        y = self.y - al.learner.y + center_y

        if (not al.learner.can_move()) and al.learner.movement:
            progressive_offset_x = 0
            progressive_offset_y = 0
            if dir_equal(self.direction, Direction.UP):
                progressive_offset_y = 1 - progressive_offset
            elif dir_equal(self.direction, Direction.DOWN):
                progressive_offset_y = progressive_offset - 1
            elif dir_equal(self.direction, Direction.RIGHT):
                progressive_offset_x = progressive_offset - 1
            else:
                progressive_offset_x = 1 - progressive_offset

            x += progressive_offset_x + learner_movement_offset_x
            y += progressive_offset_y + learner_movement_offset_y

        final_x = x * al.ui.cell_size
        final_y = y * al.ui.cell_size

        final_x += al.weather.get_offset_x()
        final_y += al.weather.get_offset_y()

        sprite_name = f"{self.sprite}_{string_from_direction(self.direction)}"
        if sprite_name in al.ui.npc_sprites:
            sprite = al.ui.npc_sprites[sprite_name]
            al.ui.screen.blit(sprite, [final_x, final_y])
        else:
            pygame.draw.rect(
                al.ui.screen,
                self.color,
                pygame.Rect(final_x, final_y, al.ui.cell_size, al.ui.cell_size),
            )

    def move(self, al: "All", next_x, next_y):
        self.previous_x = self.x
        self.previous_y = self.y
        self.last_movement = time.time()
        if self.x == next_x:
            if next_y >= self.y:
                self.direction = Direction.DOWN
            elif next_y <= self.y:
                self.direction = Direction.UP
        elif next_y == self.y:
            if next_x >= self.x:
                self.direction = Direction.RIGHT
            elif next_x <= self.x:
                self.direction = Direction.LEFT
        self.x = next_x
        self.y = next_y
