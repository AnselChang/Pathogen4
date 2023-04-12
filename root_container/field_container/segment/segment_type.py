from enum import Enum, auto

class PathSegmentType(Enum):
    STRAIGHT = 1
    ARC = 2
    BEZIER = 3