from adapter.path_adapter import PathAdapter
from command_creation.command_type import CommandType

from enum import Enum, auto

class TurnAttributeID(Enum):
    THETA1 = auto()
    THETA2 = auto()

class TurnAdapter(PathAdapter):

    def __init__(self):

        super().__init__(CommandType.TURN, TurnAttributeID)

    def set(self, attribute: TurnAttributeID, value: float, string: str):
        super().set(attribute, value, string)