from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.select_listener import SelectorType


"""
Deals with selecting and multiselecting entities.
Holds a list of the entities currently selected.
"""

# handle what can be selected with other entities and what cannot
class SelectHandler:

    def __init__(self):

        self.entities: list[Entity] = []

    # return true if successful add
    def add(self, entity: Entity) -> bool:
        
        if entity.select.type == SelectorType.SOLO and not self.isEmpty():
            # do not allow if something already selected, and entity is SOLO
            return False
        elif len(self.entities) == 1 and self.entities[0].select.type == SelectorType.SOLO:
            # do not allow if something is already selected and that something is SOLO
            return False

        self.entities.append(entity)
        return True
    
    def remove(self, entity: Entity) -> None:
        self.entities.remove(entity)

    def removeAll(self):
        self.entities.clear()

    def hasOnly(self, entity: Entity) -> bool:
        return len(self.entities) == 1 and entity is self.entities[0]
    
    def isEmpty(self) -> bool:
        return len(self.entities) == 0