from abc import ABC, abstractmethod
from enum import Enum
from Observers.observer import Observable
from CommandCreation.command_type import CommandType


class Adapter(ABC, Observable):

    def __init__(self, type: CommandType, dict: dict):
        self.type = type
        self._dict: dict = dict

    def getDict(self) -> dict:
        return self._dict
    
    def get(self, variable: str) -> float | str | None:
        if variable in self._dict:
            return self._dict[variable]
        else:
            return None
        
class NullAdapter(Adapter):
    def __init__(self):
        super().__init__(CommandType.CUSTOM, {})


class AdapterInterface(ABC):

    @abstractmethod
    def getAdapter(self) -> Adapter:
        pass

    @abstractmethod
    def updateAdapter(self) -> None:
        pass