from __future__ import annotations
from typing import TYPE_CHECKING
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
Acts as a "context" class in the state design pattern. Owns PathSegmentState objects
that define behavior for straight/arc/bezier shapes. Easy to switch between states
We also define the constants that apply across all segment types here, like color and thickness
"""

class StraightSegmentEntity(Entity):
    def __init__(self, field: FieldEntity, model: PathSegmentModel):
        self.model = model
        self.field = field
        super().__init__(parent = field, drawOrder = DrawOrder.SEGMENT)


        self.COLOR = (0, 255, 0)
        self.THICKNESS = 3
        self.HOVER_THICKNESS = 5

    def defineAfter(self) -> None:
        self.beforePos = self.field.inchesToMouse(self.model.getBeforePos())
        self.afterPos = self.field.inchesToMouse(self.model.getAfterPos())

    def isTouching(self, position: tuple) -> bool:
        beforeUI = self.model.getPrevious().ui
        x1, y1 = beforeUI.CENTER_X, beforeUI.CENTER_Y
        afterUI = self.model.getNext().ui
        x2, y2 = afterUI.CENTER_X, afterUI.CENTER_Y
        return pointTouchingLine(*position, x1, y1, x2, y2, self.HOVER_THICKNESS)

    def draw(self, screen, isActive, isHovering):
        
        # draw segment from beforePos to afterPos
        drawLine(screen, self.COLOR, *self.beforePos, *self.afterPos, self.THICKNESS)