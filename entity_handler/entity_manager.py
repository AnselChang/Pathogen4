from entity_base.entity import Entity
from root_container.root_container import RootContainer
from entity_ui.tooltip import TooltipOwner
from common.dimensions import Dimensions
from common.draw_order import DrawOrder
import pygame

"""
Handles the list of entities. Add and remove entities and it will automatically
update and draw them every tick.
"""
class EntityManager:

    def __init__(self):

        self.entities: list[Entity] = []

        # entities that own Tick (must call onTick() every tick)
        self.tickEntities: list[Entity] = []
        self.keyEntities: list[Entity] = []        

    def initRootContainer(self):
        self.rootContainer = RootContainer()
        return self.rootContainer

    # by setting a parent, it will be removed when parent is removed
    # SHOULD ONLY BE CALLED WITHIN BASE ENTITY CLASS
    def _addEntity(self, entity: Entity):
        
        self.entities.append(entity)
        self.entities.sort(key = lambda entity: entity.drawOrder, reverse = True)

        if entity.tick is not None:
            self.tickEntities.append(entity)
        if entity.key is not None:
            self.keyEntities.append(entity)

    def removeEntity(self, entity: Entity):

        for child in entity._children:
            self.entities.remove(child)

        entity._parent._children.remove(entity)
        self.entities.remove(entity)

        if entity in self.tickEntities:
            self.tickEntities.remove(entity)
        if entity in self.keyEntities:
            self.keyEntities.remove(entity)

    def getEntityAtPosition(self, position: tuple) -> Entity:

        drawOrder: DrawOrder = None
        self.touching: list[Entity] = []
        for entity in self.entities:
            if entity.isVisible() and entity.isTouching(position):
                drawOrder = entity.drawOrder
                self.touching.append(entity)

        # At this point, drawOrder is set to entity with highest priority
        # We delete all entities from self.touching that are not this priority
        self.touching = [entity for entity in self.touching if entity.drawOrder == drawOrder]

        # Now we find the winning entity from the list.
        if len(self.touching) == 0:
            # no entity touching
            return None
        elif len(self.touching) == 1:
            # Simple case. Only one touching entity, so return
            return self.touching[0]
        else:
            # Multiple entities touching mouse. Find the closest one touching
            closestDistance = self.touching[0].distanceTo(position)
            closest = self.touching[0]
            for entity in self.touching[1:]:
                distance = entity.distanceTo(position)
                if distance < closestDistance:
                    closestDistance = distance
                    closest = entity
            return closest
    
    def drawEntities(self, interactor, screen: pygame.Surface, mousePosition: tuple, dimensions: Dimensions):

        for entity in self.entities:
            if entity.isVisible():
                selected = entity in interactor.selected.entities
                hovering = entity is interactor.hoveredEntity and (selected or not (interactor.leftDragging or interactor.rightDragging))

                if interactor.greedyEntity is not None and interactor.greedyEntity is not entity:
                    hovering = False

                entity.draw(screen, selected, hovering)
                #entity.drawRect(screen)

        # draw tooltips on top of the entities
        for entity in self.entities:
            if isinstance(entity, TooltipOwner) and entity.isVisible() and entity is interactor.hoveredEntity and interactor.selected.isEmpty():
                entity.drawTooltip(screen, mousePosition, dimensions)

    # call onTick() for every entity with tick object
    def tick(self):

        for entity in self.tickEntities:
            entity.tick.onTick()

    def onKeyDown(self, key):
        for entity in self.keyEntities:
            entity.key.onKeyDown(key)

    def onKeyUp(self, key):
        for entity in self.keyEntities:
            entity.key.onKeyUp(key)