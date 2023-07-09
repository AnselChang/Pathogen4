from entity_base.entity import Entity
from entity_ui.selector_menu.selector_menu_entity import SelectorMenuEntity
from entity_ui.selector_menu.selector_menu_factory import *
from common.image_manager import ImageID

from entities.root_container.field_container.segment.straight_segment_entity import StraightSegmentEntity

from entity_ui.selector_menu.configurations.segment_menu import configureSegmentMenu
from entity_ui.selector_menu.configurations.node_menu import configureNodeMenu


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

        # add configured menus to the list
        self.addMenuDefinition(configureNodeMenu())
        self.addMenuDefinition(configureSegmentMenu())

    def addMenuDefinition(self, menuDefinition: MenuDefinition):
        self.menuDefinitions.append(menuDefinition)

    # If the entity type is supported, create and return a SelectorMenuEntity for the entity
    def createMenuForEntity(self, entity: Entity) -> SelectorMenuEntity:
        print("create menu for entity", entity)
        for menuDefinition in self.menuDefinitions:
            if isinstance(entity, menuDefinition.entityType):
                return SelectorMenuEntity(self.fieldContainer, entity, menuDefinition)

        return None   