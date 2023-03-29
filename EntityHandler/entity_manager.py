from BaseEntity.entity import Entity
from reference_frame import PointRef
import pygame

class EntityManager:

    def __init__(self):

        self.entities: list[Entity] = []

    def addEntity(self, entity: Entity):
        self.entities.append(entity)
        self.entities.sort(key = lambda entity: entity.drawOrder, reverse = True)

    def removeEntity(self, entity: Entity):
        self.entities.remove(entity)

    def getEntityAtPosition(self, position: PointRef) -> Entity:

        self.touching: list[Entity] = []
        for entity in self.entities:
            if entity.isVisible() and entity.isTouching(position):
                self.touching.append(entity)

        if len(self.touching) == 0:
            return None
        elif len(self.touching) == 1:
            return self.touching[0]
        else:
            # Find the closest one touching
            closestDistance = self.touching[0].distanceTo(position)
            closest = self.touching[0]
            for entity in self.touching[1:]:
                distance = entity.distanceTo(position)
                if distance < closestDistance:
                    closestDistance = distance
                    closest = entity
            return closest
    
    def drawEntities(self, interactor, screen: pygame.Surface):


        for entity in self.entities:
            if entity.isVisible():
                selected = entity in interactor.selectedEntities
                hovering = entity is interactor.hoveredEntity and (selected or not (interactor.leftDragging or interactor.rightDragging))
                entity.draw(screen, selected, hovering)