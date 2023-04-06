from enum import Enum
from dataclasses import dataclass
from color import ColorTheme


class CommandType(Enum):
    TURN = 1
    STRAIGHT = 2
    ARC = 3
    BEZIER = 4
    CUSTOM = 5

@dataclass
class CommandTypeInfo:
    color: tuple

COLOR_THEME = ColorTheme(70.8, 82)

COMMAND_INFO = {
    CommandType.TURN : CommandTypeInfo(COLOR_THEME.get(216)),
    CommandType.STRAIGHT : CommandTypeInfo(COLOR_THEME.get(0)),
    CommandType.ARC : CommandTypeInfo(COLOR_THEME.get(140)),
    CommandType.BEZIER : CommandTypeInfo(COLOR_THEME.get(183)),
    CommandType.CUSTOM : CommandTypeInfo(COLOR_THEME.get(275))
}