from abc import ABC, abstractmethod
from enum import Enum
import pygame

from reference_frame import PointRef

class Select(ABC):

    def __init__(self, entity, id: str):
        self.entity = entity
        self.id = id

    # the rect bounding box for the object
    @abstractmethod
    def getHitbox(self) -> pygame.Rect:
        return
    
    @abstractmethod
    def onSelect(self, interactor) -> None:
        pass

    @abstractmethod
    def onDeselect(self, interactor) -> None:
        pass
    
    
class SelectLambda(Select):

    def __init__(self, entity, id: str, FgetHitbox = lambda : None, FonSelect = lambda: None, FonDeselect = lambda: None):
        super().__init__(entity, id)
        self.FgetHitbox = FgetHitbox
        self.FonSelect = FonSelect
        self.FonDeselect = FonDeselect

    def getHitbox(self) -> pygame.Rect:
        return self.FgetHitbox()
    
    def onSelect(self, interactor) -> None:
        self.FonSelect()

    def onDeselect(self, interactor) -> None:
        self.FonDeselect()