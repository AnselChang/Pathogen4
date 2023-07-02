from entity_base.entity import Entity
from entity_handler.entity_manager import EntityManager
from utility.pygame_functions import drawTransparentRect
from utility.math_functions import isInsideBox

import pygame

class SelectorBox:

    def __init__(self):
        self.disable()

    def enable(self, start: tuple):
        self.active = True
        self.start = start
        self.x1, self.y1 = start
        print("enable mu")

    def disable(self):
        self.active = False
        print("disable ")

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
        x1, y1 = self.start
        x2, y2 = self.end

        x = min(x1, x2)
        y = min(y1, y2)
        width = abs(x1 - x2)
        height = abs(y1 - y2)

        print("d")

        drawTransparentRect(screen, x, y, width, height, (173, 216, 230), 100)