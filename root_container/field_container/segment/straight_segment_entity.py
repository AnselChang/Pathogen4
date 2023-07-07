from __future__ import annotations
from typing import TYPE_CHECKING
from models.path_models.segment_direction import SegmentDirection

from root_container.field_container.segment.abstract_segment_entity import AbstractSegmentEntity
if TYPE_CHECKING:
    from models.path_models.path_segment_model import PathSegmentModel

from root_container.field_container.field_entity import FieldEntity


from entity_base.listeners.drag_listener import DragLambda
from utility.math_functions import isInsideBox, pointTouchingLine

from entity_base.entity import Entity


from common.draw_order import DrawOrder
from utility.pygame_functions import shade, drawLine
import pygame

"""
View in MVC model for drawing arcs. References segment model and straight state model
"""

class StraightSegmentEntity(AbstractSegmentEntity):
    def __init__(self, field: FieldEntity, model: PathSegmentModel):
        super().__init__(field, model)

    def defineCenter(self) -> tuple:
        return self.field.inchesToMouse(self.model.getCenterInches())


    def isTouching(self, position: tuple) -> bool:
        beforeUI = self.model.getPrevious().ui
        x1, y1 = beforeUI.CENTER_X, beforeUI.CENTER_Y
        afterUI = self.model.getNext().ui
        x2, y2 = afterUI.CENTER_X, afterUI.CENTER_Y
        return pointTouchingLine(*position, x1, y1, x2, y2, self.HOVER_THICKNESS)

    def draw(self, screen, isActive, isHovering):

        color = self.getColor()

        # draw segment from beforePos to afterPos
        drawLine(screen, color, *self.beforePos, *self.afterPos, self.THICKNESS)