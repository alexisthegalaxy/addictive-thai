import math
from typing import Union, Tuple

Number = Union[int, float]
Point2D = Tuple[Number, Number]


def distance_1d(x: Number, y: Number) -> float:
    return abs(x - y)


def distance_2d(point_1: Point2D, point_2: Point2D) -> float:
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)
