from abc import ABC, abstractmethod
from enum import Enum, auto
from data_structures.observer import Observable, Observer
from command_creation.command_type import CommandType
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from serialization.serializable import Serializable, SerializedState
from utility.pretty_printer import PrettyPrinter

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
        PathAttributeID.DISTANCE,
        PathAttributeID.THETA1
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

class AdapterState(SerializedState, PrettyPrinter):
    def __init__(self, type: CommandType, iconImageStates: list[ImageState] | ImageState):
        self.type = type
        if not isinstance(iconImageStates, list):
            iconImageStates = [iconImageStates]
        self.iconImageStates = [image.serialize() for image in iconImageStates]

    def _deserialize(self) -> 'PathAdapter':
        return PathAdapter(self.type, [ImageState.deserialize(state) for state in self.iconImageStates])

    def makeDeserialized(self):
        self.DESERIALIZED = self._deserialize()

    def deserialize(self) -> 'PathAdapter':
        return self.DESERIALIZED

"""
Abstract class that facilitates communication between Commands and Path entities
"""

class PathAdapter(ABC, Observable, Observer, Serializable):

    def _serialize(self) -> AdapterState:
        return AdapterState(self.type, self.iconImageStates)
    
    def makeSerialized(self):
        self.SERIALIZED = self._serialize()

    def serialize(self) -> AdapterState:
        return self.SERIALIZED
    
    def __init__(self, type: CommandType, iconImageStates: list[ImageState] | ImageState):
        self.type = type

        # set to true when adapter changes.
        # Every tick, command will poll, and if True, will recompute and set to False
        self._queueModify = False

        self.iconImageStates = iconImageStates
        self.iconStateID: Enum = None

        self._dictValue: dict[Enum, float] = {}
        self._dictStr: dict[Enum, str] = {}

        for attribute in legalAttributesForType[type]:
            self._dictValue[attribute] = -1
            self._dictStr[attribute] = ""

    def getDict(self) -> dict:
        return self._dict
    
    def modify(self):
        self._queueModify = True

    def wasModified(self) -> bool:
        return self._queueModify
    
    def resetModified(self):
        self._queueModify = False
    
    # value: the raw numerical value to be used in generated code
    # string: to be displayed by readouts, etc.
    def set(self, attribute: Enum, value: float, string: str):

        if attribute not in self._dictValue:
            return

        self._dictValue[attribute] = round(value, 3)
        self._dictStr[attribute] = string
        self.modify()

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
        self.modify()

    def getIconStateID(self) -> ImageID:
        return self.iconStateID
        
class NullPathAdapter(PathAdapter):
    def __init__(self):
        image = ImageState(0, ImageID.CUSTOM)
        super().__init__(CommandType.CUSTOM, image)


class AdapterInterface(ABC):

    @abstractmethod
    def getAdapter(self) -> PathAdapter:
        pass

    @abstractmethod
    def updateAdapter(self) -> None:
        pass