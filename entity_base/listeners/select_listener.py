from abc import ABC, abstractmethod
from enum import Enum, auto
import pygame


class SelectorType(Enum):
    FREE = auto() # no restriction on selecting
    SOLO = auto() # can be the only thing selected

class SelectListener(ABC):

    def __init__(self, entity, id: str, enableToggle: bool, greedy: bool = False,
                 type: SelectorType = SelectorType.FREE, deselectOnMouseUp = False,
                 rootSelectEntity = None
                 ):
        self.entity = entity
        self.id = id
        self.type = type
        self.deselectOnMouseUp = deselectOnMouseUp

        if rootSelectEntity is None:
            self.rootSelectEntity = entity
        else:
            self.rootSelectEntity = rootSelectEntity

        # when selected, nothing else is hovered
        # when deselected by clicking somewhere else, do not select the other thing 
        self.greedy = greedy

        self.isSelected = False

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

    # Only applicable to greedy objects. Prevent selection if return true
    @abstractmethod
    def disableGreedyDeselect(self) -> bool:
        return False
    
    
class SelectLambda(SelectListener):

    def __init__(self, entity, id: str, enableToggle: bool = False, greedy: bool = False,
                 type: SelectorType = SelectorType.FREE, deselectOnMouseUp = False,
                 FgetHitbox = lambda : None, FonSelect = lambda interactor: None,
                   FonDeselect = lambda interactor: None, rootSelectEntity = None,
                   FdisableGreedySelect = lambda: False
                   ):
        super().__init__(entity, id, enableToggle, greedy, type, deselectOnMouseUp, rootSelectEntity)
        self.FgetHitbox = FgetHitbox
        self.FonSelect = FonSelect
        self.FonDeselect = FonDeselect
        self.FdisableGreedySelect = FdisableGreedySelect

    def getHitbox(self) -> pygame.Rect:
        return self.FgetHitbox()
    
    def onSelect(self, interactor) -> None:
        self.isSelected = True
        self.FonSelect(interactor)

    def onDeselect(self, interactor) -> None:
        self.isSelected = False
        self.FonDeselect(interactor)

    # Only applicable to greedy objects. Prevent selection if return true
    def disableGreedyDeselect(self) -> bool:
        return self.FdisableGreedySelect()