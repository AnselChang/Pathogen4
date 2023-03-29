from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from BaseEntity.EntityFunctions.click_function import Click, ClickLambda
from BaseEntity.EntityFunctions.drag_function import Drag
from BaseEntity.EntityFunctions.select_function import Select
from BaseEntity.entity import Entity
from PathEntities.segment_entity import SegmentEntity
from draw_order import DrawOrder

from pygame_functions import shade
from math_functions import pointTouchingLine

import pygame

"""
Segments specifically for connecting path nodes
Subclasses are responsbible for defining the shape (straight/arc/bezier) and drawing the segment
This class provides an interface for getting thetas at both sides, and holding references to nodes
We also define the constants that apply across all segment types here, like color and thickness
"""

class PathSegmentEntity(SegmentEntity):
    def __init__(self, interactor, first: Entity, second: Entity) -> None:

        

        super().__init__(first, second, 
                         select = Select(self, "segment"),
                         click = ClickLambda(self,FOnDoubleClick = self.onDoubleClick),
                         drawOrder = DrawOrder.SEGMENT)
        
        self.interactor = interactor

        self.isReversed = False

        self.thickness = 3
        self.hitboxThickness = 5
        self.colorForward = [122, 191, 118]
        self.colorForwardH = shade(self.colorForward, 0.9)
        self.colorForwardA = shade(self.colorForward, 0.4)
        self.colorReversed = [191, 118, 118]
        self.colorReversedH = shade(self.colorReversed, 0.9)
        self.colorReversedA = shade(self.colorReversed, 0.4)

    def onDoubleClick(self):
        entities = [self, self.first, self.second]
        self.interactor.setSelectedEntities(entities)

    def reverseSegmentDirection(self):
        self.isReversed = not self.isReversed

    def getColor(self, isActive: bool = False, isHovered: bool = False):

        if self.isReversed:
            if isActive:
                return self.colorReversedA
            elif isHovered:
                return self.colorReversedH
            else:
                return self.colorReversed
        else:
            if isActive:
                return self.colorForwardA
            elif isHovered:
                return self.colorForwardH
            else:
                return self.colorForward
        
    def isVisible(self) -> bool:
        return True