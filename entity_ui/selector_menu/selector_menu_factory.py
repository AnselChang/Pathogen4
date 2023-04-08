from abc import ABC, abstractmethod
from common.image_manager import ImageID

from entity_base.entity import Entity

# Implement this to define a menu action based on the target entity and mouse position
class MenuClickAction(ABC):

    @abstractmethod
    def isActionAvailable(self, targetEntity: Entity) -> bool:
        pass

    @abstractmethod
    def onClick(self, targetEntity: Entity, mouse: tuple):
        pass

# Callback just prints out a specified message
class TestMenuClickAction(MenuClickAction):
    def __init__(self, actionAvailable: bool, message: str):
        self.actionAvailable = actionAvailable
        self.message = message

    def isActionAvailable(self, targetEntity: Entity) -> bool:
        return self.actionAvailable

    def onClick(self, targetEntity: Entity, mouse: tuple):
        print(targetEntity, mouse, self.message, targetEntity.RECT)

# Used to construct a menu button for the menu
class MenuButtonDefinition:

    # onClick should take in TWO ARGUMENTS: the target entity and the mouse
    def __init__(self, action: MenuClickAction, tooltipString: str, imageOnID: ImageID, tooltipOffString: str = None, imageOffID: ImageID = None):
        self.action = action

        self.tooltipString = tooltipString
        self.imageOnID = imageOnID
        
        self.tooltipOffString = tooltipOffString
        self.imageOffID = imageOffID

"""
Stores the type of entity that can be selected.
Stores the list of menu button definitions.
"""
class MenuDefinition:

    def __init__(self, entityType: type[Entity]):
        self.entityType = entityType
        self.definitions: list[MenuButtonDefinition] = []

    def add(self, action: MenuClickAction, tooltipString: str, imageOnID: ImageID, tooltipOffString: str = None, imageOffID: ImageID = None):
        self.definitions.append(MenuButtonDefinition(action, tooltipString, imageOnID, tooltipOffString, imageOffID))

    def create(self) -> list[MenuButtonDefinition]:
        return self.definitions