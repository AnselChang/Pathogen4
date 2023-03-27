from BaseEntity.entity import Entity
from reference_frame import PointRef
from EntityHandler.interactor import Interactor
import pygame

class EntityManager:

    def __init__(self):

        self.entities: list[Entity] = []

    def addEntity(self, entity: Entity):
        self.entities.append(entity)

    def removeEntity(self, entity: Entity):
        self.entities.remove(entity)

    def getEntityAtPosition(self, position: PointRef) -> Entity:
        for entity in self.entities:
            if entity.isVisible() and entity.isTouching(position):
                return entity
        return None
    
    def drawEntities(self, interactor: Interactor, screen: pygame.Surface):

        # active is the list of active entities.
        if len(interactor.selectedEntities) > 0:
            active = interactor.selectedEntities
        elif interactor.hoveredEntity is not None:
            active = [interactor.hoveredEntity]
        else:
            active = []

        for entity in self.entities:
            if entity.isVisible():
                entity.draw(screen, entity in active)