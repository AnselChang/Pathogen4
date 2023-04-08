from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity_ui.selector_menu.selector_menu_manager import SelectorMenuManager

from entity_base.entity import Entity
from entity_base.listeners.select_listener import SelectorType
from entity_ui.selector_menu.selector_menu_entity import SelectorMenuEntity


"""
Deals with selecting and multiselecting entities.
Holds a list of the entities currently selected.

Also, handles the menu that appears when an entity is selected.
Stores the current menu object, and despawns it if deselected
"""

# handle what can be selected with other entities and what cannot
class SelectHandler:

    def __init__(self):

        self.entities: list[Entity] = []
        
        self.activeMenu: SelectorMenuEntity = None

    def initMenuManager(self, menuManager: SelectorMenuManager):
        self.menuManager = menuManager

    # return true if successful add
    def add(self, entity: Entity) -> bool:

        if entity in self.entities:
            return False
        
        if entity.select.type == SelectorType.SOLO and not self.isEmpty():
            # do not allow if something already selected, and entity is SOLO
            return False
        elif len(self.entities) == 1 and self.entities[0].select.type == SelectorType.SOLO:
            # do not allow if something is already selected and that something is SOLO
            return False

        self.entities.append(entity)

        # If menu already open, close it
        if self.activeMenu is not None:
            self.activeMenu.despawn()
            self.activeMenu = None

        # If entity has a menu, open it, but only if there is only one entity selected
        if len(self.entities) == 1:
            self.activeMenu = self.menuManager.createMenuForEntity(entity)

        # returns true for successfully selecting entity
        return True
    
    def remove(self, entity: Entity) -> None:
        self.entities.remove(entity)

        # If menu already open, close it
        if self.activeMenu is not None:
            self.activeMenu.despawn()
            self.activeMenu = None

    def removeAll(self):
        self.entities.clear()

    def hasOnly(self, entity: Entity) -> bool:
        return len(self.entities) == 1 and entity is self.entities[0]
    
    def isEmpty(self) -> bool:
        return len(self.entities) == 0