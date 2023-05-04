from adapter.path_adapter import PathAdapter, PathAttributeID
from command_creation.command_type import CommandType

from enum import Enum, auto

from entity_base.image.image_state import ImageState

BezierAttributeIDs = [
    PathAttributeID.X1,
    PathAttributeID.Y1,
    PathAttributeID.X2,
    PathAttributeID.Y2,
    PathAttributeID.THETA1,
    PathAttributeID.THETA2
]

class BezierAdapter(PathAdapter):

    def __init__(self, iconImageStates: list[ImageState]):

        super().__init__(CommandType.BEZIER, iconImageStates, BezierAttributeIDs)

    def set(self, attribute: PathAttributeID, value: float, string: str):
        super().set(attribute, value, string)