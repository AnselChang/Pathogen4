from enum import IntEnum, auto

# Lowest number is drawn in the front
class DrawOrder(IntEnum):
    MOUSE_SELECT_BOX = auto()
    TAB = auto()
    COMMANND_BLOCK = auto()
    PANEL_BACKGROUND = auto()
    NODE = auto()
    SEGMENT = auto()
    FIELD_BACKGROUND = auto()
