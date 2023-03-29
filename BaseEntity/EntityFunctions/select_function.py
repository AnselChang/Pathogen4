from abc import ABC, abstractmethod
from enum import Enum

from reference_frame import PointRef

class Select(ABC):

    def __init__(self, entity, id: str):
        self.entity = entity
        self.id = id

    @abstractmethod
    def getHitboxPoints(self) -> list[PointRef]:
        return
    
    @abstractmethod
    def onSelect(self, interactor) -> None:
        pass

    @abstractmethod
    def onDeselect(self, interactor) -> None:
        pass
    
    
class SelectLambda(Select):

    def __init__(self, entity, id: str, FgetHitboxPoints = lambda : [], FonSelect = lambda: None, FonDeselect = lambda: None):
        super().__init__(entity, id)
        self.FgetHitboxPoints = FgetHitboxPoints
        self.FonSelect = FonSelect
        self.FonDeselect = FonDeselect

    def getHitboxPoints(self) -> list[PointRef]:
        return self.FgetHitboxPoints()
    
    def onSelect(self, interactor) -> None:
        self.FonSelect()

    def onDeselect(self, interactor) -> None:
        self.FonDeselect()