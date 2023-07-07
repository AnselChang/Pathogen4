from enum import Enum, auto


class SegmentType(Enum):
    STRAIGHT = auto()
    ARC = auto()
    BEZIER = auto()