from entity_base.entity import Entity
from entity_ui.selector_menu.selector_menu_entity import SelectorMenuEntity
from entity_ui.selector_menu.selector_menu_factory import *
from common.image_manager import ImageID

from root_container.field_container.node.path_node_entity import PathNodeEntity

"""
Stores a list of MenuDefinitions: one for each type of entity that can be selected.
For example, node, segment, etc.
Interacts with the Interactor to determine which menu to display when an entity is selected.
And creates the menu given the entity object
This class also builds the actual menus
"""

class SelectorMenuManager:

    def __init__(self, fieldContainer):

        self.menuDefinitions: list[MenuDefinition] = []

        # Store the field container, as menus need to use it to determine starting location
        self.fieldContainer = fieldContainer

        self.configureNodeMenu()

    def addMenuDefinition(self, menuDefinition: MenuDefinition):
        self.menuDefinitions.append(menuDefinition)

    # If the entity type is supported, create and return a SelectorMenuEntity for the entity
    def createMenuForEntity(self, entity: Entity) -> SelectorMenuEntity:
            
        for menuDefinition in self.menuDefinitions:
            if isinstance(entity, menuDefinition.entityType):
                return SelectorMenuEntity(self.fieldContainer, entity, menuDefinition.create())

        return None
    
    """
    Menu for path nodes. Functionality for:
        - revealing command associated with node
        - add/delete intermediate turns
        - Insert node before/after
            - When clicked, special mode where wherever mouse clicks next, there will be node
            - If not beginning/end, will subdivide a segment, but new node does not have to be on segment
    """
    def configureNodeMenu(self):

        # test menu for now
        nodeDefinition = MenuDefinition(PathNodeEntity)
        nodeDefinition.add(TestMenuClickAction("Button 1"), "Button 1 tooltip", ImageID.CHECKBOX_OFF)
        nodeDefinition.add(TestMenuClickAction("Button 2"), "Button 2 tooltip", ImageID.STRAIGHT_FORWARD)
        nodeDefinition.add(TestMenuClickAction("Button 2"), "Button 2 tooltip", ImageID.TURN_LEFT)

        self.addMenuDefinition(nodeDefinition)