from abc import ABC, abstractmethod
from enum import Enum
from Observers.observer import Observable
from CommandCreation.command_type import CommandType
from image_manager import ImageID


class PathAdapter(ABC, Observable):

    def __init__(self, type: CommandType, dict: dict):
        self.type = type
        self._dict: dict = dict
        self.icon: ImageID = None

    def getDict(self) -> dict:
        return self._dict
    
    def get(self, variable: str) -> float | str | None:
        if variable in self._dict:
            return self._dict[variable]
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