from adapter.path_adapter import AdapterState, PathAdapter, PathAttributeID
from command_creation.command_type import CommandType

from enum import Enum, auto

from entity_base.image.image_state import ImageState

class ArcAdapterState(AdapterState):
    def _deserialize(self) -> 'PathAdapter':
        return ArcAdapter([ImageState.deserialize(state) for state in self.iconImageStates])


class ArcAdapter(PathAdapter):

    def _serialize(self) -> ArcAdapterState:
        return ArcAdapterState(self.type, self.iconImageStates)

    def __init__(self, iconImageStates: list[ImageState]):

        super().__init__(CommandType.ARC, iconImageStates)

    def set(self, attribute: PathAttributeID, value: float, string: str):
        super().set(attribute, value, string)