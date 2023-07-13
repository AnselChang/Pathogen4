from adapter.path_adapter import AdapterState, PathAdapter, PathAttributeID
from command_creation.command_type import CommandType
from data_structures.observer import NotifyType

from enum import Enum, auto

from entity_base.image.image_state import ImageState

class TurnAdapterState(AdapterState):
    def _deserialize(self) -> 'PathAdapter':
        return TurnAdapter([ImageState.deserialize(state) for state in self.iconImageStates])

class TurnAdapter(PathAdapter):

    def _serialize(self) -> TurnAdapterState:
        return TurnAdapterState(self.type, self.iconImageStates)

    def __init__(self, iconImageStates: list[ImageState]):

        super().__init__(CommandType.TURN, iconImageStates)

        self.turnEnabled: bool = None # if set to false, means THETA1 ~= THETA2)

    def set(self, attribute: PathAttributeID, value: float, string: str):
        super().set(attribute, value, string)

    def setTurnEnabled(self, turnEnabled: bool):
        if self.turnEnabled == turnEnabled:
            return
        self.turnEnabled = turnEnabled
        self.notify(NotifyType.TURN_ENABLE_TOGGLED)

    def isTurnEnabled(self) -> bool:
        return self.turnEnabled
    
    def _deserialize(self) -> 'PathAdapter':
        return TurnAdapter([ImageState.deserialize(state) for state in self.iconImageStates])
