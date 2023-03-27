from BaseEntity.entity import Entity
from EntityHandler.entity_manager import EntityManager

class Interactor:

    def __init__(self):
        self.hoveredEntity: Entity = None
        self.selectedEntities: list[Entity] = []
        self.dragging: bool = False

    def onMouseDown(self, entities: EntityManager):
        pass

    def onMouseUp(self, entities: EntityManager):
        pass