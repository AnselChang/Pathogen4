from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from BaseEntity.EntityFunctions.click_function import Click
from BaseEntity.EntityFunctions.drag_function import Drag
from BaseEntity.EntityFunctions.select_function import Select
from BaseEntity.entity import Entity
from PathEntities.path_segment_entity import PathSegmentEntity

from pygame_functions import drawLine
from math_functions import pointTouchingLine

import pygame

# Abstract class for a non-functional edge
# only purpose is to connect two points. 

class StraightPathSegmentEntity(PathSegmentEntity):
    def __init__(self, interactor, first: Entity, second: Entity) -> None:
        super().__init__(interactor, first, second)


    def isTouching(self, position: PointRef) -> bool:
        mx, my = position.screenRef
        x1, y1 = self.first.getPosition().screenRef
        x2, y2 = self.second.getPosition().screenRef
        return pointTouchingLine(mx, my, x1, y1, x2, y2, self.hitboxThickness)

    def distanceTo(self, position: PointRef) -> float:
        return (self.getPosition() - position).magnitude(Ref.SCREEN)

    def getPosition(self) -> PointRef:
        fpos = self.first.getPosition()
        spos = self.second.getPosition()

        return fpos + (spos - fpos) / 2

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        x1, y1 = self.first.getPosition().screenRef
        x2, y2 = self.second.getPosition().screenRef

        border = (0,0,0) if isActive else None
        drawLine(screen, self.getColor(isActive, isHovered), x1, y1, x2, y2, self.thickness, None)

    def toString(self) -> str:
        return "Edge"

