from enum import Enum


class Tone(Enum):
    LOW = 1
    MID = 2
    HIGH = 3
    RISING = 4
    FALLING = 5
    UNKNOWN = 6


class Length(Enum):
    SHORT = 1
    LONG = 2
    UNKNOWN = 3
