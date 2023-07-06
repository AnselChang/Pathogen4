from __future__ import annotations
from typing import TYPE_CHECKING

from root_container.field_container.segment.abstract_segment_entity import AbstractSegmentEntity
from root_container.field_container.segment.bezier_node_entity import BezierNodeEntity
if TYPE_CHECKING:
    from models.path_models.path_segment_model import PathSegmentModel
    from models.path_models.path_segment_state.bezier_segment_state import BezierSegmentState

from root_container.field_container.field_entity import FieldEntity


from entity_base.listeners.drag_listener import DragLambda
from utility.math_functions import isInsideBox, pointTouchingLine

from entity_base.entity import Entity


from common.draw_order import DrawOrder
from utility.pygame_functions import drawArcFromCenterAngles, shade, drawLine
import pygame

"""
View in MVC model for drawing beziers. References segment model and arc state model
"""

class BezierSegmentEntity(AbstractSegmentEntity):
    def __init__(self, field: FieldEntity, model: PathSegmentModel):
        super().__init__(field, model)

        # create bezier control points
        self.control1 = BezierNodeEntity(self, True)
        self.control2 = BezierNodeEntity(self, False)

    def defineCenter(self) -> tuple:
        return self.field.inchesToMouse(self.model.getCenterInches())

    def isTouching(self, position: tuple) -> bool:
        
        # sliding window for making lines across points
        # Increases effective hitbox size
        WINDOW_SIZE = 5

        # loop through each segment
        for i in range(len(self.mousePoints) - WINDOW_SIZE):
            x1, y1 = self.mousePoints[i]
            x2, y2 = self.mousePoints[i+WINDOW_SIZE]
            if pointTouchingLine(*position, x1, y1, x2, y2, self.HOVER_THICKNESS):
                return True

        return False

    def getBezierState(self) -> BezierSegmentState:
        return self.model.getState()

    def defineAfter(self) -> None:
        super().defineAfter()
        
        pointsInches = self.getBezierState().getBezierPoints()
        self.points = [self.field.inchesToMouse(point) for point in pointsInches]

        mousePointsInches = self.getBezierState().getBezierMousePoints()
        self.mousePoints = [self.field.inchesToMouse(point) for point in mousePointsInches]

    # return if self, nodes, or control points are hovered
    def isBezierHovered(self) -> bool:

        beforeNode = self.model.getPrevious().ui
        afterNode = self.model.getNext().ui

        if self.hover.isHovering or self.select.isSelected: # segment is hovering or selected
            return True
        elif beforeNode.hover.isHovering or afterNode.hover.isHovering: # nodes are hovering
            return True
        elif self.control1.hover.isHovering or self.control2.hover.isHovering: # control points are hovering
            return True
        
        return False

    def draw(self, screen, isActive, isHovering):
        
        color = self.getColor()

        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i+1]
            drawLine(screen, color, x1, y1, x2, y2, self.THICKNESS, None)

        # Draw every point if selected
        if self.model.getBezierState().SLOW_POINTS is not None and self.isBezierHovered():
            for point in self.points:
                pygame.draw.circle(screen, (0,0,0), point, 1)

