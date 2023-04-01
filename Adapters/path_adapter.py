from abc import ABC, abstractmethod
from enum import Enum
from Observers.observer import Observable
from CommandCreation.command_type import CommandType
from image_manager import ImageID

"""
Abstract class that facilitates communication between Commands and Path entities
"""

class PathAdapter(ABC, Observable):

    def __init__(self, type: CommandType, attributes: type[Enum]):
        self.type = type
        self.icon: ImageID = None

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
        
    def setIcon(self, icon: ImageID):
        self.icon = icon

    def getIcon(self) -> ImageID:
        return self.icon
        
class NullPathAdapter(PathAdapter):
    def __init__(self):
        super().__init__(CommandType.CUSTOM, {})
        self.setIcon(ImageID.CUSTOM)


class AdapterInterface(ABC):

    @abstractmethod
    def getAdapter(self) -> PathAdapter:
        pass

    @abstractmethod
    def updateAdapter(self) -> None:
        pass