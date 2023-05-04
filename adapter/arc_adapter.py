from adapter.path_adapter import PathAdapter, PathAttributeID
from command_creation.command_type import CommandType

from enum import Enum, auto

from entity_base.image.image_state import ImageState

class ArcAdapter(PathAdapter):

    def __init__(self, iconImageStates: list[ImageState]):

        super().__init__(CommandType.ARC, iconImageStates)

    def set(self, attribute: PathAttributeID, value: float, string: str):
        super().set(attribute, value, string)