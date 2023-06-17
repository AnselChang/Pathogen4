from typing import Iterator
from data_structures.observer import Observer
from entity_base.entity import Entity
from entity_handler.entity_traversal import traverseEntities, TraversalOrder
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

        self.keyEntities: list[Entity] = []        
        self.clickEntities: list[Entity] = []

    def initRootContainer(self):
        self.rootContainer = RootContainer()
        return self.rootContainer
    

    # by setting a parent, it will be removed when parent is removed
    # SHOULD ONLY BE CALLED WITHIN BASE ENTITY CLASS
    def _addEntity(self, entity: Entity):
        
        self.entities.append(entity)

        if entity.key is not None:
            self.keyEntities.append(entity)
        if entity.click is not None:
            self.clickEntities.append(entity)

    def removeEntity(self, entity: Entity, excludeChildrenIf = lambda child : False):

        i = 0
        while i < len(entity._children):
            child = entity._children[i]
            
            if not excludeChildrenIf(child):
                self.removeEntity(child)
                continue
            i += 1

        if entity._parent is not None and entity in entity._parent._children:
            entity._parent._children.remove(entity)

        if entity in self.entities:
            self.entities.remove(entity)

        if entity in self.keyEntities:
            self.keyEntities.remove(entity)
        if entity in self.clickEntities:
            self.clickEntities.remove(entity)

        # entity unsubscribes to any observables
        if isinstance(entity, Observer):
            entity.unsubscribeAll()

    def getEntityAtPosition(self, position: tuple) -> Entity:

        parent = None
        drawOrder: DrawOrder = None
        tiebreaker = None

        self.touching: list[Entity] = []
        for entity in traverseEntities(TraversalOrder.POSTFIX):
            if entity.isVisible() and entity.isTouching(position):

                currentTiebreaker = entity.drawOrderTiebreaker()
                if currentTiebreaker is None:
                    currentTiebreaker = 0

                if drawOrder is None:
                    parent = entity._parent
                    drawOrder = entity.drawOrder
                    tiebreaker = currentTiebreaker

                elif parent != entity._parent or entity.drawOrder != drawOrder or tiebreaker != currentTiebreaker:
                    break
                
                self.touching.append(entity)

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
        for entity in traverseEntities(TraversalOrder.PREFIX):
            if entity.isVisible():
                selected = entity in interactor.selected.entities
                hovering = entity is interactor.hoveredEntity and (selected or not (interactor.leftDragging or interactor.rightDragging))

                if interactor.greedyEntity is not None and interactor.greedyEntity is not entity:
                    hovering = False

                entity.draw(screen, selected, hovering)
                #entity.drawRect(screen)

        # draw tooltips on top of the entities
        for entity in self.entities:
            if isinstance(entity, TooltipOwner) and entity.isVisible() and entity is interactor.hoveredEntity:
                entity.drawTooltip(screen, mousePosition, dimensions)

    """
    Tick callbacks are invoked on a recursive manner. onTickStart() callbacks
    are invoked on the parent entities before children, while onTickEnd() callbacks
    are invoked on the children before the parent.
    """
    def tick(self):
        self._tick(self.rootContainer)

    def _tick(self, entity: Entity):

        tickable = (entity.tick is not None) and (entity.isVisible() or entity.recomputeWhenInvisible)

        if tickable:
            entity.tick.onTickStart()
        
        for child in entity._children:
            self._tick(child)

        if tickable:
            entity.tick.onTickEnd()

    def onKeyDown(self, key):
        for entity in self.keyEntities:
            entity.key.onKeyDown(key)

    def onKeyUp(self, key):
        for entity in self.keyEntities:
            entity.key.onKeyUp(key)