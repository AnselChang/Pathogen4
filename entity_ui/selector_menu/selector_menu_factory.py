from abc import ABC, abstractmethod
from common.image_manager import ImageID

from entity_base.entity import Entity

# Implement this to define a menu action based on the target entity and mouse position
class MenuClickAction(ABC):

    @abstractmethod
    def onClick(self, targetEntity: Entity, mouse: tuple):
        pass

# Callback just prints out a specified message
class TestMenuClickAction(MenuClickAction):
    def __init__(self, message: str):
        self.message = message
    def onClick(self, targetEntity: Entity, mouse: tuple):
        print(targetEntity, mouse, self.message)

# Used to construct a menu button for the menu
class MenuButtonDefinition:

    # onClick should take in TWO ARGUMENTS: the target entity and the mouse
    def __init__(self, action: MenuClickAction, tooltipString: str, imageID: ImageID, imageHoveredID: ImageID = None):
        self.action = action
        self.tooltipString = tooltipString
        self.imageID = imageID
        self.imageHoveredID = imageHoveredID

"""
Stores the type of entity that can be selected.
Stores the list of menu button definitions.
"""
class MenuDefinition:

    def __init__(self, entityType: type[Entity]):
        self.entityType = entityType
        self.definitions: list[MenuButtonDefinition] = []

    def add(self, action: MenuClickAction, tooltipString: str, imageID: ImageID, imageHoveredID: ImageID = None):
        self.definitions.append(MenuButtonDefinition(action, tooltipString, imageID, imageHoveredID))

    def create(self) -> list[MenuButtonDefinition]:
        return self.definitions