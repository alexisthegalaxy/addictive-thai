import random


def get_corona_1(x, y, thai):
    random.seed(thai)
    adjacent_x_y = [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
        (x, y + 1),
        (x - 1, y),
    ]
    random.shuffle(adjacent_x_y)
    return adjacent_x_y


def get_corona_2(x, y, thai):
    """
    Get the cells in a David star pattern around the central cell
    """
    random.seed(thai)
    adjacent_x_y = [
        (x - 1, y - 2),
        (x + 1, y - 1),
        (x + 2, y + 1),
        (x + 1, y + 2),
        (x - 1, y + 1),
        (x - 2, y - 1),
    ]
    random.shuffle(adjacent_x_y)
    return adjacent_x_y


def get_corona_3(x, y, thai):
    """
    Get the cells in between the 6 summits of the David star pattern around the central cell
    """
    random.seed(thai)
    adjacent_x_y = [
        (x, y - 2),
        (x + 2, y),
        (x + 2, y + 2),
        (x, y + 2),
        (x - 2, y),
        (x - 2, y - 2),
    ]
    random.shuffle(adjacent_x_y)
    return adjacent_x_y


def get_coronas(x, y, thai):
    return (
        get_corona_1(x, y, thai) + get_corona_2(x, y, thai) + get_corona_3(x, y, thai)
    )
