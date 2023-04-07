from entity_base.entity import Entity
from entity_ui.group.linear_entity import LinearEntity
from typing import TypeVar, Generic

"""
A group of linear entities, arranged either horizontally or vertically
"""
T = TypeVar('T')
class LinearGroupEntity(Entity, Generic[T]):

    def __init__(self, parent: Entity, isHorizontal: bool):
        
        super().__init__(parent)

        self.groupEntities: list[LinearEntity | T] = []
        self.isHorizontal = isHorizontal

        self.N = 0

        self.recomputePosition()

    # add linear entity to group. returns the linear entity's location
    def add(self, entity: LinearEntity):
        self.groupEntities.append(entity)
        self.N += 1

        return self.N - 1

    def N(self) -> int:
        return len(self.groupEntities)
    
    def getFromID(self, id) -> LinearEntity:
        for entity in self.groupEntities:
            if entity.id == id:
                return entity
        raise Exception(id, "No entity with id found")