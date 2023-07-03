from __future__ import annotations
from typing import TYPE_CHECKING
from models.path_models.segment_direction import SegmentDirection

from root_container.field_container.segment.abstract_segment_entity import AbstractSegmentEntity
from root_container.field_container.segment.arc_node_entity import ArcNodeEntity
if TYPE_CHECKING:
    from models.path_models.path_segment_model import PathSegmentModel
    from models.path_models.path_segment_state.arc_segment_state import ArcSegmentState

from root_container.field_container.field_entity import FieldEntity


from entity_base.listeners.drag_listener import DragLambda
from utility.math_functions import isInsideBox, pointTouchingLine

from entity_base.entity import Entity


from common.draw_order import DrawOrder
from utility.pygame_functions import drawArcFromCenterAngles, shade, drawLine
import pygame

"""
Acts as a "context" class in the state design pattern. Owns PathSegmentState objects
that define behavior for straight/arc/bezier shapes. Easy to switch between states
We also define the constants that apply across all segment types here, like color and thickness
"""

class ArcSegmentEntity(AbstractSegmentEntity):
    def __init__(self, field: FieldEntity, model: PathSegmentModel):
        super().__init__(field, model)

        # node located at midpoint of arc to control curvature
        ArcNodeEntity(self)

    def defineCenter(self) -> tuple:
        return self.field.inchesToMouse(self.model.getCenterInches())


    def isTouching(self, position: tuple) -> bool:
        beforeUI = self.model.getPrevious().ui
        x1, y1 = beforeUI.CENTER_X, beforeUI.CENTER_Y
        afterUI = self.model.getNext().ui
        x2, y2 = afterUI.CENTER_X, afterUI.CENTER_Y
        return pointTouchingLine(*position, x1, y1, x2, y2, self.HOVER_THICKNESS)

    def getArcState(self) -> ArcSegmentState:
        return self.model.getState()

    def defineAfter(self) -> None:
        super().defineAfter()
    
        arcState = self.getArcState()

        self.START_ANGLE = arcState.getStartAngle()
        self.STOP_ANGLE = arcState.getStopAngle()
        self.POSITIVE = arcState.getPositive()
        self.CENTER = self.field.inchesToMouse(arcState.getCenter())
        self.RADIUS = self.field.scalarInchesToMouse(arcState.getRadius())
        self.ARC_LENGTH = self.field.scalarInchesToMouse(arcState.getArcLength())

    def draw(self, screen, isActive, isHovering):

        if self.model.getDirection() == SegmentDirection.FORWARD:
            color = self.colorForwardH if self.hover.isHovering else self.colorForward
        else:
            color = self.colorReversedH if self.hover.isHovering else self.colorReversed
        

        # Draw arc based on ArcSegmentState
        RESOLUTION = 1 # how smooth the arc should be
        thickness = self.HOVER_THICKNESS if self.hover.isHovering else self.THICKNESS
        drawArcFromCenterAngles(screen, self.START_ANGLE, self.STOP_ANGLE, self.POSITIVE,
                                color, self.CENTER, self.RADIUS, 
                                width = thickness,
                                numSegments = self.ARC_LENGTH * RESOLUTION
                                )
