from abc import abstractmethod
from BaseEntity.entity import Entity
from reference_frame import PointRef, Ref, VectorRef
from BaseEntity.EntityListeners.drag_listener import Drag
from BaseEntity.EntityListeners.click_listener import Click
from BaseEntity.EntityListeners.select_listener import Select
from pygame_functions import drawTransparentCircle
from math_functions import scaleTuple, clampTuple, intTuple
import pygame, math

class CircleMixin(Entity):

    def __init__(self, radius: int, hoveredRadius: int):
        self.radius = radius
        self.radiusH = hoveredRadius

    @abstractmethod
    def getColor(self) -> tuple:
        pass

    # get the hitbox rect approximately spanning the circle
    def getHitbox(self) -> pygame.Rect:

        hitbox = pygame.Rect(0, 0, self.radius * 1.5, self.radius * 1.5)
        hitbox.center = self.getPosition().screenRef
        return hitbox

    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        MARGIN = 4
        return self.distanceTo(position) <= self.radius + MARGIN

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        r = self.radiusH if isHovered else self.radius
        pos = self.getPosition().screenRef

        # draw circle
        pygame.draw.circle(screen, self.getColor(), pos, r)

        # draw border if active
        if isActive:
            pygame.draw.circle(screen, (0,0,0), pos, r, 2)

    def toString(self) -> str:
        return "Circle"