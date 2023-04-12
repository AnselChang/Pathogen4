from adapter.path_adapter import PathAdapter
from command_creation.command_type import CommandType

from enum import Enum, auto

from entity_base.image.image_state import ImageState

class BezierAttributeID(Enum):
    X1 = auto()
    Y1 = auto()
    X2 = auto()
    Y2 = auto()
    THETA1 = auto()
    THETA2 = auto()

class BezierAdapter(PathAdapter):

    def __init__(self, iconImageStates: list[ImageState]):

        super().__init__(CommandType.BEZIER, iconImageStates, BezierAttributeID)

    def set(self, attribute: BezierAttributeID, value: float, string: str):
        super().set(attribute, value, string)