from adapter.path_adapter import PathAdapter
from command_creation.command_type import CommandType

from enum import Enum, auto

from entity_base.image.image_state import ImageState

class ArcAttributeID(Enum):
    X1 = auto()
    Y1 = auto()
    X2 = auto()
    Y2 = auto()
    RADIUS = auto()
    ARC_LENGTH = auto()
    THETA1 = auto()
    THETA2 = auto()

class ArcAdapter(PathAdapter):

    def __init__(self, iconImageStates: list[ImageState]):

        super().__init__(CommandType.ARC, iconImageStates, ArcAttributeID)

    def set(self, attribute: ArcAttributeID, value: float, string: str):
        super().set(attribute, value, string)