from BaseEntity.entity import Entity
from reference_frame import PointRef
import pygame

class EntityManager:

    def __init__(self):

        self.entities: list[Entity] = []

        # entities that own Tick (must call onTick() every tick)
        self.tickEntities: list[Entity] = []

    # by setting a parent, it will be removed when parent is removed
    def addEntity(self, entity: Entity, parent: Entity = None):
        
        if parent is not None:
            entity._setParent(parent)

        self.entities.append(entity)
        self.entities.sort(key = lambda entity: entity.drawOrder, reverse = True)

        if entity.tick is not None:
            self.tickEntities.append(entity)

    def removeEntity(self, entity: Entity):

        for child in entity._children:
            self.entities.remove(child)

        self.entities.remove(entity)

        if entity in self.tickEntities:
            self.tickEntities.remove(entity)

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
                selected = entity in interactor.selected.entities
                hovering = entity is interactor.hoveredEntity and (selected or not (interactor.leftDragging or interactor.rightDragging))
                entity.draw(screen, selected, hovering)

    # call onTick() for every entity with tick object
    def tick(self):

        for entity in self.tickEntities:
            entity.tick.onTick()