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
        BezierNodeEntity(self, True)
        BezierNodeEntity(self, False)

    def defineCenter(self) -> tuple:
        return self.field.inchesToMouse(self.model.getCenterInches())

    def isTouching(self, position: tuple) -> bool:
        beforeUI = self.model.getPrevious().ui
        x1, y1 = beforeUI.CENTER_X, beforeUI.CENTER_Y
        afterUI = self.model.getNext().ui
        x2, y2 = afterUI.CENTER_X, afterUI.CENTER_Y
        return pointTouchingLine(*position, x1, y1, x2, y2, self.HOVER_THICKNESS)

    def getBezierState(self) -> BezierSegmentState:
        return self.model.getState()

    def defineAfter(self) -> None:
        super().defineAfter()
        pass

    def draw(self, screen, isActive, isHovering):
        
        color = self.getColor()

