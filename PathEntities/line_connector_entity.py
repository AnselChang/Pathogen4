from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from BaseEntity.EntityFunctions.click_function import Click
from BaseEntity.EntityFunctions.drag_function import Drag
from BaseEntity.EntityFunctions.select_function import Select
from BaseEntity.entity import Entity
from PathEntities.segment_entity import SegmentEntity

from pygame_functions import drawLine
from math_functions import pointTouchingLine

import pygame

# Abstract class for a non-functional edge
# only purpose is to connect two points. 

class LineConnectorEnttiy(SegmentEntity):
    def __init__(self, first: Entity, second: Entity, hitboxThickness: int, drag: Drag = None, select: Select = None, click: Click = None) -> None:
        super().__init__(first, second, drag = drag, select = select, click = click)

        self.hitboxThickness = hitboxThickness
    
    @abstractmethod
    def getColor(self, isActive: bool, isHovered: bool) -> tuple:
        pass

    @abstractmethod
    def getThickness(self, isActive: bool, isHovered: bool) -> int:
        pass

    def isVisible(self) -> bool:
        return True

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
        drawLine(screen, self.getColor(isActive, isHovered), x1, y1, x2, y2, self.getThickness(isActive, isHovered), 255)

    def toString(self) -> str:
        return "Edge"

