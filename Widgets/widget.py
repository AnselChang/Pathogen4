from abc import ABC, abstractmethod
from Observers.observer import Observable

class Widget(Observable):
    
    @abstractmethod
    def getVariableName(self) -> str:
        pass

    @abstractmethod
    def getVariableValue(self) -> float:
        pass