from BaseEntity.entity import Entity
from UIEntities.Generic.linear_entity import LinearEntity
from EntityHandler.entity_manager import EntityManager

"""
A group of linear entities, arranged either horizontally or vertically
"""
class LinearGroupEntity(Entity):

    def __init__(self, parent: Entity, isHorizontal: bool):
        
        super().__init__(parent)

        self.groupEntities: list[LinearEntity] = []
        self.isHorizontal = isHorizontal

        self.N = 0

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
        raise Exception("No entity with id found")