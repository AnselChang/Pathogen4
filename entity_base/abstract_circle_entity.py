from abc import abstractmethod
from entity_base.entity import Entity
import pygame

class AbstractCircleEntity(Entity):

    # NO CONSTRUCTOR. FOR SUBCLASSES, WORKAROUND IS TO CALL ENTITY CONSTRUCTOR DIRECTLY
    # PYTHON IS CURSED

    def getColor(self, isHovered: bool = False) -> tuple:
        pass

    def getRadius(self, isHovered: bool = False) -> float:
        pass

    # get relative radius
    def _radius(self, isHovered: bool = False) -> float:
        return self.getRadius() * self.dimensions.RESOLUTION_RATIO

    def defineWidth(self) -> float:
        return self._radius() * 2
    
    def defineHeight(self) -> float:
        return self._radius() * 2

    # get the hitbox rect approximately spanning the circle
    def getHitbox(self) -> pygame.Rect:

        hitbox = pygame.Rect(0, 0, self._radius() * 1.5, self._radius() * 1.5)
        hitbox.center = self.CENTER_X, self.CENTER_Y
        return hitbox

    def isTouching(self, position: tuple) -> bool:
        MARGIN = 4
        return self.distanceTo(position) <= self._radius() + MARGIN

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        r = self._radius(isHovered)
        pos = (self.CENTER_X, self.CENTER_Y)

        # draw circle
        pygame.draw.circle(screen, self.getColor(isHovered), pos, r)

        # draw border if active
        if isActive:
            pygame.draw.circle(screen, (0,0,0), pos, r, 2)
