from abc import ABC, abstractmethod
from enum import Enum
from data_structures.observer import Observable
from command_creation.command_type import CommandType
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState

"""
Abstract class that facilitates communication between Commands and Path entities
"""

class PathAdapter(ABC, Observable):

    def __init__(self, type: CommandType, iconImageStates: list[ImageState] | ImageState, attributes: type[Enum]):
        self.type = type

        self.iconImageStates = iconImageStates
        self.iconStateID: Enum = None

        self._dictValue: dict[Enum, float] = {}
        self._dictStr: dict[Enum, str] = {}
        for attribute in attributes:
            self._dictValue[attribute] = -1
            self._dictStr[attribute] = ""

    def getDict(self) -> dict:
        return self._dict
    
    # value: the raw numerical value to be used in generated code
    # string: to be displayed by readouts, etc.
    def set(self, attribute: Enum, value: float, string: str):
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