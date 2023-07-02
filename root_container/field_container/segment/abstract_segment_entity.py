from __future__ import annotations
from typing import TYPE_CHECKING
from entity_base.listeners.hover_listener import HoverLambda
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

class AbstractSegmentEntity(Entity):
    def __init__(self, field: FieldEntity, model: PathSegmentModel):
        self.model = model
        self.field = field
        super().__init__(parent = field,
                         hover = HoverLambda(self),
                         drawOrder = DrawOrder.SEGMENT)

        self.THICKNESS = 3
        self.HOVER_THICKNESS = 5

        self.colorForward = [122, 210, 118]
        self.colorForwardH = shade(self.colorForward, 0.92)
        self.colorForwardA = shade(self.colorForward, 0.7)
        self.colorReversed = [191, 118, 118]
        self.colorReversedH = shade(self.colorReversed, 0.92)
        self.colorReversedA = shade(self.colorReversed, 0.7)

    def defineAfter(self) -> None:
        self.beforePos = self.field.inchesToMouse(self.model.getBeforePos())
        self.afterPos = self.field.inchesToMouse(self.model.getAfterPos())