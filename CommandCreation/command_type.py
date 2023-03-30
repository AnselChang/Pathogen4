from enum import Enum
from dataclasses import dataclass


class CommandType(Enum):
    TURN = 1
    STRAIGHT = 2
    ARC = 3
    BEZIER = 4
    CUSTOM = 5

@dataclass
class CommandTypeInfo:
    color: tuple

COMMAND_INFO = {
    CommandType.TURN : CommandTypeInfo((0,0,0)),
    CommandType.STRAIGHT : CommandTypeInfo((0,0,0)),
    CommandType.ARC : CommandTypeInfo((0,0,0)),
    CommandType.BEZIER : CommandTypeInfo((0,0,0)),
    CommandType.CUSTOM : CommandTypeInfo((0,0,0))
}