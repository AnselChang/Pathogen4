from adapter.path_adapter import AdapterState, PathAdapter, PathAttributeID
from command_creation.command_type import CommandType

from enum import Enum, auto

from entity_base.image.image_state import ImageState

class StraightAdapterState(AdapterState):
    def _deserialize(self) -> 'PathAdapter':
        return StraightAdapter([ImageState.deserialize(state) for state in self.iconImageStates])


class StraightAdapter(PathAdapter):

    def _serialize(self) -> StraightAdapterState:
        return StraightAdapterState(self.type, self.iconImageStates)

    def __init__(self, iconImageStates: list[ImageState]):

        super().__init__(CommandType.STRAIGHT, iconImageStates)

    def set(self, attribute: PathAttributeID, value: float, string: str):
        super().set(attribute, value, string)