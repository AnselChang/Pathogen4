from enum import Enum

class CommandType(Enum):
    TURN = 1
    STRAIGHT = 2
    ARC = 3
    BEZIER = 4
    CUSTOM = 5