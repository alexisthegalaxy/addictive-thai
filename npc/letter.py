from enum import Enum


class LetterType(Enum):
    VOWEL = 1
    LOW = 2
    MID = 3
    HIGH = 4


def _get_color_from_class(letter_class: str) -> str:
    if letter_class == "LOW":
        return "purple"
    if letter_class == "MID":
        return "blue"
    if letter_class == "HIGH":
        return "yellow"
    return "teal"


def get_sprite_name_from_letter_class(letter_class: str, al):
    color = _get_color_from_class(letter_class)
    return f"{color}_spell"
