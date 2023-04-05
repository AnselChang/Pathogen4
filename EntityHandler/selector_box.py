from BaseEntity.entity import Entity
from EntityHandler.entity_manager import EntityManager
from pygame_functions import drawTransparentRect
from math_functions import isInsideBox

import pygame

class SelectorBox:

    def __init__(self):
        self.disable()

    def enable(self, start: tuple):
        self.active = True
        self.start = start
        self.x1, self.y1 = start

    def disable(self):
        self.active = False

    def isEnabled(self):
        return self.active
    
    # Whether the selector rectangle intersects with the hitbox rectangle of the entity
    def isSelecting(self, entity: Entity, x2, y2):
        hitboxRect = entity.select.getHitbox()

        # in this case, there is no specified hitbox
        if hitboxRect is None:
            return False

        selectorRect = pygame.Rect(self.x1, self.y1, x2 - self.x1, y2 - self.y1)
        return selectorRect.colliderect(hitboxRect)

    # return a list of selected entities
    def update(self, end: tuple, entities: EntityManager) -> list[Entity]:

        self.end = end
        x2, y2 = end

        self.selected: list[Entity] = []
        for entity in entities.entities:

            # not a multi-selectable entitity
            if entity.select is None:
                continue

            if self.isSelecting(entity, x2, y2):
                self.selected.append(entity)

        return self.selected
    

    def draw(self, screen: pygame.Surface):

        if not self.active:
            return
        x, y = self.start
        x2, y2 = self.end
        drawTransparentRect(screen, x, y, x2 - x, y2 - y, (173, 216, 230), 100)