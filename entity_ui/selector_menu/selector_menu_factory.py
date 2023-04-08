from abc import ABC, abstractmethod
from enum import Enum
from common.image_manager import ImageID
from entity_base.image.image_entity import ImageEntity, ImageState
from entity_base.entity import Entity

from typing import TypeVar, Generic

# Implement this to define a menu action based on the target entity and mouse position
T = TypeVar('T')
class MenuClickAction(ABC, Generic[T]):

    # override this to return current state ID of the menu button
    def getStateID(self, targetEntity: Entity | T) -> Enum:
        return None
        
    # if not available, the button will be grayed out, and cannot be clicked
    def isActionAvailable(self, targetEntity: Entity | T) -> bool:
        return True

    # callback for when button is available and clicked
    # if something is returned, it will be recieved by onLeftClick at interactor
    # That is set to make the entity returned to start dragging
    @abstractmethod
    def onClick(self, targetEntity: Entity | T, mouse: tuple):
        pass

# Callback just prints out a specified message
class TestMenuClickAction(MenuClickAction):
    def __init__(self, actionAvailable: bool):
        self.actionAvailable = actionAvailable

    def isActionAvailable(self, targetEntity: Entity) -> bool:
        return self.actionAvailable

    def onClick(self, targetEntity: Entity, mouse: tuple):
        print(targetEntity, "test clicked")

# Used to construct a menu button for the menu
class MenuButtonDefinition:

    # onClick should take in TWO ARGUMENTS: the target entity and the mouse
    def __init__(self, imageStates: list[ImageState], action: MenuClickAction, condition = lambda entity: True):
        self.imageStates = imageStates
        self.action = action
        self.condition = condition
        

"""
Stores the type of entity that can be selected.
Stores the list of menu button definitions.
The menu button is only added if the condition is true
"""
class MenuDefinition:

    def __init__(self, entityType: type[Entity]):
        self.entityType = entityType
        self.definitions: list[MenuButtonDefinition] = []

    def add(self, imageStates: list[ImageState], action: MenuClickAction, condition = lambda entity: True):
        self.definitions.append(MenuButtonDefinition(imageStates, action, condition))