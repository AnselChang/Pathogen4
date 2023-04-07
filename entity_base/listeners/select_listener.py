from abc import ABC, abstractmethod
from enum import Enum, auto
import pygame

from common.reference_frame import PointRef

class SelectorType(Enum):
    FREE = auto() # no restriction on selecting
    SOLO = auto() # can be the only thing selected

class SelectListener(ABC):

    def __init__(self, entity, id: str, enableToggle: bool, greedy: bool = False, type: SelectorType = SelectorType.FREE, deselectOnMouseUp = False):
        self.entity = entity
        self.id = id
        self.type = type
        self.deselectOnMouseUp = deselectOnMouseUp

        # when selected, nothing else is hovered
        # when deselected by clicking somewhere else, do not select the other thing 
        self.greedy = greedy 

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

    def __init__(self, entity, id: str, enableToggle: bool = False, greedy: bool = False, type: SelectorType = SelectorType.FREE, deselectOnMouseUp = False, FgetHitbox = lambda : None, FonSelect = lambda interactor: None, FonDeselect = lambda interactor: None):
        super().__init__(entity, id, enableToggle, greedy, type, deselectOnMouseUp)
        self.FgetHitbox = FgetHitbox
        self.FonSelect = FonSelect
        self.FonDeselect = FonDeselect

    def getHitbox(self) -> pygame.Rect:
        return self.FgetHitbox()
    
    def onSelect(self, interactor) -> None:
        self.FonSelect(interactor)

    def onDeselect(self, interactor) -> None:
        self.FonDeselect(interactor)