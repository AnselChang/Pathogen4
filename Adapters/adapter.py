from abc import ABC, abstractmethod
from enum import Enum
from Observers.observer import Observable
from Commands.command_type import CommandType


class Adapter(ABC, Observable):

    def __init__(self, type: CommandType):
        self.type = type
        self._dict: None = None

    def setDict(self, dict: dict):
        self._dict = dict
        self.notify()

    def getDict(self) -> dict:
        return self._dict
    
    def get(self, variable: str) -> float | str | None:
        if variable in self._dict:
            return self._dict[variable]
        else:
            return None


class AdapterInterface(ABC):

    @abstractmethod
    def getAdapter(self) -> Adapter:
        pass

    @abstractmethod
    def updateAdapter(self) -> None:
        pass