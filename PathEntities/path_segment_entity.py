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
    def __init__(self, first: Entity, second: Entity, drag: Drag = None, select: Select = None, click: Click = None) -> None:

        

        super().__init__(first, second, drag = drag, select = select, drawOrder = DrawOrder.SEGMENT,
                         click = ClickLambda(self, FonRightClick = self.reverseSegmentDirection)
                         )
        
        self.isReversed = False

        self.thickness = 3
        self.hitboxThickness = 5
        self.colorForward = [122, 191, 118]
        self.colorForwardH = shade(self.colorForward, 0.9)
        self.colorReversed = [191, 118, 118]
        self.colorReversedH = shade(self.colorReversed, 0.9)

    def reverseSegmentDirection(self):
        self.isReversed = not self.isReversed

    def getColor(self, isHovered: bool = False):

        if self.isReversed:
            return self.colorReversedH if isHovered else self.colorReversed
        else:
            return self.colorForwardH if isHovered else self.colorForward
        
    def isVisible(self) -> bool:
        return True