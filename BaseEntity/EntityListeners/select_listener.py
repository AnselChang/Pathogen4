from abc import ABC, abstractmethod
from enum import Enum, auto
import pygame

from reference_frame import PointRef

class SelectorType(Enum):
    FREE = auto() # no restriction on selecting
    SOLO = auto() # can be the only thing selected

class SelectListener(ABC):

    def __init__(self, entity, id: str, enableToggle: bool, type: SelectorType = SelectorType.FREE):
        self.entity = entity
        self.id = id
        self.type = type
        self.enableToggle = enableToggle # if set to true, clicking while selected will deselect

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
    
    
class SelectLambda(SelectListener):

    def __init__(self, entity, id: str, enableToggle: bool = False, FgetHitbox = lambda : None, FonSelect = lambda: None, FonDeselect = lambda: None):
        super().__init__(entity, id, enableToggle)
        self.FgetHitbox = FgetHitbox
        self.FonSelect = FonSelect
        self.FonDeselect = FonDeselect

    def getHitbox(self) -> pygame.Rect:
        return self.FgetHitbox()
    
    def onSelect(self, interactor) -> None:
        self.FonSelect()

    def onDeselect(self, interactor) -> None:
        self.FonDeselect()