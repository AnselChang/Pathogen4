from abc import abstractmethod
from BaseEntity.entity import Entity
from reference_frame import PointRef, Ref, VectorRef
from BaseEntity.EntityFunctions.drag_function import Drag
from BaseEntity.EntityFunctions.click_function import Click
from BaseEntity.EntityFunctions.select_function import Select
from pygame_functions import drawTransparentCircle
import pygame, math

class CircleMixin(Entity):

    def __init__(self, radius: int, hoveredRadius: int, color: tuple):
        self.radius = radius
        self.radiusH = hoveredRadius
        self.color = color


    def getHitboxPoints(self) -> list[PointRef]:

        position = self.getPosition()
        points: list[PointRef] = [position]
        PI = 3.14
        
        for theta in [0, PI/2, PI, 3*PI/2]:
            dx, dy = self.radius * math.cos(theta), self.radius * math.sin(theta)
            points.append(position + VectorRef(Ref.SCREEN, (dx,dy)))

        return points

    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        return self.distanceTo(position) <= self.radius

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        r = self.radiusH if isHovered else self.radius
        pos = self.getPosition().screenRef

        # draw circle
        pygame.draw.circle(screen, self.color, pos, r)

        # draw border if active
        if isActive:
            pygame.draw.circle(screen, (0,0,0), pos, r, 2)

    def toString(self) -> str:
        return "Circle"