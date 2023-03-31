from abc import ABC, abstractmethod
from enum import Enum
from Observers.observer import Observable
from CommandCreation.command_type import CommandType
from image_manager import ImageID


class PathAdapter(ABC, Observable):

    def __init__(self, type: CommandType, attributes: type[Enum]):
        self.type = type
        self.icon: ImageID = None

        self._dict: dict[Enum, float] = {}
        for attribute in attributes:
            self._dict[attribute] = -1

    def getDict(self) -> dict:
        return self._dict
    
    def set(self, attribute: Enum, value: float):
        self._dict[attribute] = value
    
    def get(self, attribute: Enum) -> float:
        if attribute in self._dict:
            return self._dict[attribute]
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