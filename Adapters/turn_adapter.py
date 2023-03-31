from Adapters.path_adapter import PathAdapter
from CommandCreation.command_type import CommandType

from enum import Enum, auto

class TurnAttributeID(Enum):
    THETA1 = auto()
    THETA2 = auto()

class TurnAdapter(PathAdapter):

    def __init__(self):

        super().__init__(CommandType.TURN, TurnAttributeID)

    def set(self, attribute: TurnAttributeID, value: float):
        super().set(attribute, value)