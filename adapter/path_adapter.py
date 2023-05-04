from abc import ABC, abstractmethod
from enum import Enum, auto
from data_structures.observer import Observable
from command_creation.command_type import CommandType
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState

class PathAttributeID(Enum):
    NONE = auto()
    X1 = auto()
    Y1 = auto()
    X2 = auto()
    Y2 = auto()
    DISTANCE = auto()
    THETA1 = auto()
    THETA2 = auto()
    XCENTER = auto()
    YCENTER = auto()
    RADIUS = auto()
    ARC_LENGTH = auto()

legalAttributesForType: dict[CommandType, list[PathAttributeID]] = {
    CommandType.STRAIGHT: [
        PathAttributeID.X1,
        PathAttributeID.Y1,
        PathAttributeID.X2,
        PathAttributeID.Y2,
        PathAttributeID.DISTANCE
    ],
    CommandType.TURN: [
        PathAttributeID.THETA1,
        PathAttributeID.THETA2
    ],
    CommandType.BEZIER: [
        PathAttributeID.X1,
        PathAttributeID.Y1,
        PathAttributeID.X2,
        PathAttributeID.Y2,
        PathAttributeID.THETA1,
        PathAttributeID.THETA2
    ],
    CommandType.ARC: [
        PathAttributeID.X1,
        PathAttributeID.Y1,
        PathAttributeID.X2,
        PathAttributeID.Y2,
        PathAttributeID.XCENTER,
        PathAttributeID.YCENTER,
        PathAttributeID.RADIUS,
        PathAttributeID.ARC_LENGTH,
        PathAttributeID.THETA1,
        PathAttributeID.THETA2
    ],
    CommandType.CUSTOM: []
}



"""
Abstract class that facilitates communication between Commands and Path entities
"""

class PathAdapter(ABC, Observable):

    def __init__(self, type: CommandType, iconImageStates: list[ImageState] | ImageState):
        self.type = type

        self.iconImageStates = iconImageStates
        self.iconStateID: Enum = None

        self._dictValue: dict[Enum, float] = {}
        self._dictStr: dict[Enum, str] = {}

        for attribute in legalAttributesForType[type]:
            self._dictValue[attribute] = -1
            self._dictStr[attribute] = ""

    def getDict(self) -> dict:
        return self._dict
    
    # value: the raw numerical value to be used in generated code
    # string: to be displayed by readouts, etc.
    def set(self, attribute: Enum, value: float, string: str):

        # make sure the attribute belongs to the corresponding type of adapter
        assert(attribute in self._dictValue)

        self._dictValue[attribute] = round(value, 3)
        self._dictStr[attribute] = string
        self.notify()
    
    def getValue(self, attribute: Enum) -> float:
        if attribute in self._dictValue:
            return self._dictValue[attribute]
        else:
            return None
        
    def getString(self, attribute: Enum) -> str:
        if attribute in self._dictStr:
            return self._dictStr[attribute]
        else:
            return None
        
    def setIconStateID(self, iconStateID: Enum):
        self.iconStateID = iconStateID

    def getIconStateID(self) -> ImageID:
        return self.iconStateID
        
class NullPathAdapter(PathAdapter):
    def __init__(self):
        image = ImageState(0, ImageID.CUSTOM)
        super().__init__(CommandType.CUSTOM, image, {})


class AdapterInterface(ABC):

    @abstractmethod
    def getAdapter(self) -> PathAdapter:
        pass

    @abstractmethod
    def updateAdapter(self) -> None:
        pass