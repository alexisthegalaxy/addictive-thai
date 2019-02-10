from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


def direction_from_string(name):
    if name == "up":
        return Direction.UP
    if name == "down":
        return Direction.DOWN
    if name == "right":
        return Direction.RIGHT
    if name == "left":
        return Direction.LEFT


def string_from_direction(direction):
    if direction.name == Direction.UP.name:
        return "up"
    if direction.name == Direction.DOWN.name:
        return "down"
    if direction.name == Direction.RIGHT.name:
        return "right"
    if direction.name == Direction.LEFT.name:
        return "left"


def opposite_direction(direction):
    if direction.name == Direction.UP.name:
        return Direction.DOWN
    if direction.name == Direction.DOWN.name:
        return Direction.UP
    if direction.name == Direction.RIGHT.name:
        return Direction.LEFT
    if direction.name == Direction.LEFT.name:
        return Direction.RIGHT
