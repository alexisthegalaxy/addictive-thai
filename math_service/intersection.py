from typing import Tuple, Optional, Union


TOP = 1
BOTTOM = 2
RIGHT = 3
LEFT = 4


def line(p1: Tuple[int, int], p2: Tuple[int, int]) -> Tuple[int, int, int]:
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C


def intersection(line_1: Tuple[int, int, int], line_2: Tuple[int, int, int]) -> Union[Tuple[int, int], bool]:
    d = line_1[0] * line_2[1] - line_1[1] * line_2[0]
    d_x = line_1[2] * line_2[1] - line_1[1] * line_2[2]
    d_y = line_1[0] * line_2[2] - line_1[2] * line_2[0]
    if d == 0:
        return False
    x = d_x / d
    y = d_y / d
    return int(x), int(y)


def get_intersection_with_screen_border(al, point_1, point_2) -> Optional[Tuple[int, int]]:
    """
    In this function, point_1 is expected to be inside the screen and point_2 might either in or out
    """
    main_line = line(point_1, point_2)

    if point_2[0] > al.ui.width:
        if point_2[1] < 0:
            lines_to_check = [TOP, RIGHT]
        elif point_2[1] > al.ui.height:
            lines_to_check = [BOTTOM, RIGHT]
        else:
            lines_to_check = [RIGHT]
    elif point_2[0] < 0:
        if point_2[1] < 0:
            lines_to_check = [TOP, LEFT]
        elif point_2[1] > al.ui.height:
            lines_to_check = [BOTTOM, LEFT]
        else:
            lines_to_check = [LEFT]
    elif point_2[1] < 0:
        lines_to_check = [TOP]
    elif point_2[1] > al.ui.height:
        lines_to_check = [BOTTOM]
    else:
        return None

    if TOP in lines_to_check:
        top_line = line((0, 0), (al.ui.width, 0))
        intersection_with_top = intersection(main_line, top_line)
        if intersection_with_top and 0 <= intersection_with_top[0] <= al.ui.width:
            return intersection_with_top

    if BOTTOM in lines_to_check:
        bottom_line = line((0, al.ui.height), (al.ui.width, al.ui.height))
        intersection_with_bottom = intersection(main_line, bottom_line)
        if intersection_with_bottom and 0 <= intersection_with_bottom[0] <= al.ui.width:
            return intersection_with_bottom

    if LEFT in lines_to_check:
        left_line = line((0, 0), (0, al.ui.height))
        intersection_with_left = intersection(main_line, left_line)
        if intersection_with_left and 0 <= intersection_with_left[1] <= al.ui.height:
            return intersection_with_left

    if RIGHT in lines_to_check:
        right_line = line((al.ui.width, 0), (al.ui.width, al.ui.height))
        intersection_with_right = intersection(main_line, right_line)
        if intersection_with_right and 0 <= intersection_with_right[1] <= al.ui.height:
            return intersection_with_right

    return None
