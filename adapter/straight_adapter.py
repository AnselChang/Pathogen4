from adapter.path_adapter import PathAdapter
from command_creation.command_type import CommandType

from enum import Enum, auto

class StraightAttributeID(Enum):
    X1 = auto()
    Y1 = auto()
    X2 = auto()
    Y2 = auto()
    DISTANCE = auto()

class StraightAdapter(PathAdapter):

    def __init__(self):

        super().__init__(CommandType.STRAIGHT, StraightAttributeID)

    def set(self, attribute: StraightAttributeID, value: float, string: str):
        super().set(attribute, value, string)