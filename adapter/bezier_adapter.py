from adapter.path_adapter import AdapterState, PathAdapter, PathAttributeID
from command_creation.command_type import CommandType

from enum import Enum, auto

from entity_base.image.image_state import ImageState

class BezierAdapterState(AdapterState):
    def _deserialize(self) -> 'PathAdapter':
        return BezierAdapter([ImageState.deserialize(state) for state in self.iconImageStates])


class BezierAdapter(PathAdapter):

    def _serialize(self) -> BezierAdapterState:
        return BezierAdapterState(self.type, self.iconImageStates)

    def __init__(self, iconImageStates: list[ImageState]):

        super().__init__(CommandType.BEZIER, iconImageStates)

    def set(self, attribute: PathAttributeID, value: float, string: str):
        super().set(attribute, value, string)