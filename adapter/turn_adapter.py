from adapter.path_adapter import PathAdapter, PathAttributeID
from command_creation.command_type import CommandType
from data_structures.observer import NotifyType

from enum import Enum, auto

from entity_base.image.image_state import ImageState

TurnAttributeIDs = [
    PathAttributeID.THETA1,
    PathAttributeID.THETA2
]

class TurnAdapter(PathAdapter):

    def __init__(self, iconImageStates: list[ImageState]):

        super().__init__(CommandType.TURN, iconImageStates, TurnAttributeIDs)

        self.turnEnabled: bool = None # if set to false, means THETA1 ~= THETA2)

    def set(self, attribute: PathAttributeID, value: float, string: str):
        super().set(attribute, value, string)

    def setTurnEnabled(self, turnEnabled: bool):
        isChange = self.turnEnabled != turnEnabled
        self.turnEnabled = turnEnabled
        if isChange:
            self.notify(NotifyType.TURN_ENABLE_TOGGLED)
        

    def isTurnEnabled(self) -> bool:
        return self.turnEnabled