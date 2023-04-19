from common.draw_order import DrawOrder
from entity_base.container_entity import Container
from entity_base.entity import Entity
from entity_ui.group.linear_container import LinearContainer
from typing import TypeVar, Generic

"""
A group of linear entities, arranged either horizontally or vertically
"""
T = TypeVar('T')
class LinearGroupContainer(Container, Generic[T]):

    def __init__(self, parent: Entity, isHorizontal: bool, drawOrder: DrawOrder = DrawOrder.PANEL_BACKGROUND):
        
        super().__init__(parent, drawOrder = drawOrder)

        self.groupEntities: list[LinearContainer | T] = []
        self.isHorizontal = isHorizontal

        self.N = 0

    # add linear entity to group. returns the linear entity's location
    def add(self, entity: LinearContainer):
        self.groupEntities.append(entity)
        self.N += 1

        return self.N - 1
    
    def remove(self, entity: LinearContainer):
        self.groupEntities.remove(entity)
        self.N -= 1

    def N(self) -> int:
        return len(self.groupEntities)
    
    def getFromID(self, id) -> LinearContainer:
        for entity in self.groupEntities:
            if entity.id == id:
                return entity
        raise Exception(id, "No entity with id found")