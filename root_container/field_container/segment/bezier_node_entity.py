from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.listeners.drag_listener import DragLambda
from utility.math_functions import distancePointToLine
if TYPE_CHECKING:
    from root_container.field_container.segment.bezier_segment_entity import BezierSegmentEntity

from entity_base.entity import Entity
from entity_base.listeners.hover_listener import HoverLambda

import pygame
from utility.pygame_functions import shade

"""
Moveable control point for bezier curves. There are two of these per curve.
Does not store state, but reads and writes to SegmentModel through BezierSegmentState
"""

class BezierNodeEntity(Entity):

    def __init__(self, segment: BezierSegmentEntity, isFirstControlPoint: bool):

        super().__init__(parent = segment,
            hover = HoverLambda(self),
            drag = DragLambda(self, selectEntityNotThis = segment, FonStartDrag = self.onStartDrag, FonDrag = self.onDrag, FonStopDrag = self.onStopDrag),
        )

        self.field = segment.field
        self.segment = segment

        self.COLOR = [255, 0, 255]
        self.COLOR_H = shade(self.COLOR, 0.9)

        self.RADIUS = 5
        self.RADIUS_H = 6

        self.isFirst = isFirstControlPoint

    def onStartDrag(self, mouse: tuple):
        pass

    def onDrag(self, mouse: tuple):
        pass

    def onStopDrag(self):
        pass

    def defineCenter(self) -> tuple:
        pos = self.segment.getBezierState().getControlPoint1() if self.isFirst else self.segment.getBezierState().getControlPoint2()
        return self.field.inchesToMouse(pos)
    
    def isTouching(self, position: tuple) -> bool:
        MARGIN = 4
        return self.distanceTo(position) <= self.RADIUS + MARGIN
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        RADIUS = self.RADIUS_H if self.hover.isHovering else self.RADIUS
        COLOR = self.COLOR_H if self.hover.isHovering else self.COLOR
        POSITION = [self.CENTER_X, self.CENTER_Y]
        pygame.draw.circle(screen, COLOR, POSITION, RADIUS)