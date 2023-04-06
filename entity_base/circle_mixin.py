from abc import abstractmethod
from entity_base.entity import Entity
import pygame

class CircleMixin(Entity):

    @abstractmethod
    def getColor(self) -> tuple:
        pass

    @abstractmethod
    def getRadius(self, isHovered: bool = False) -> float:
        pass

    # get the hitbox rect approximately spanning the circle
    def getHitbox(self) -> pygame.Rect:

        hitbox = pygame.Rect(0, 0, self.getRadius() * 1.5, self.getRadius() * 1.5)
        hitbox.center = self.CENTER_X, self.CENTER_Y
        return hitbox

    def isTouching(self, position: tuple) -> bool:
        MARGIN = 4
        return self.distanceTo(position) <= self.getRadius() + MARGIN

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        r = self.getRadius(isHovered)
        pos = (self.CENTER_X, self.CENTER_Y)

        # draw circle
        pygame.draw.circle(screen, self.getColor(), pos, r)

        # draw border if active
        if isActive:
            pygame.draw.circle(screen, (0,0,0), pos, r, 2)
