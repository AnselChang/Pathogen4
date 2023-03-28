from BaseEntity.entity import Entity
from reference_frame import PointRef, Ref, VectorRef
from BaseEntity.EntityFunctions.drag_function import Drag
from BaseEntity.EntityFunctions.click_function import Click
from BaseEntity.EntityFunctions.select_function import Select
from pygame_functions import drawTransparentCircle
import pygame

class CircleMixin(Entity):

    def __init__(self, radius: int, color: tuple):
        self.radius = radius
        self.color = color

    def getPosition(self) -> PointRef:
        raise Exception("Not implemented by subclass error")

    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        return self.distanceTo(position) <= self.radius

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        alpha = 170 if isHovered else 255
        drawTransparentCircle(screen, self.getPosition().screenRef, self.radius, self.color, alpha)

        # draw border if active
        if isActive:
            pygame.draw.circle(screen, (0,0,0), self.getPosition().screenRef, self.radius, 2)

    def toString(self) -> str:
        return "Circle"