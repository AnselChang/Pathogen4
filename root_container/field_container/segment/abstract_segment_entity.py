from __future__ import annotations
from typing import TYPE_CHECKING
from entity_base.listeners.hover_listener import HoverLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType
from models.path_models.segment_direction import SegmentDirection
if TYPE_CHECKING:
    from models.path_models.path_segment_model import PathSegmentModel

from root_container.field_container.field_entity import FieldEntity


from entity_base.listeners.drag_listener import DragLambda
from utility.math_functions import addTuples, isInsideBox, pointTouchingLine, subtractTuples

from entity_base.entity import Entity


from common.draw_order import DrawOrder
from utility.pygame_functions import shade, drawLine
import pygame

"""
Abstract view class for drawing segments. State is not stored here but
is in model
"""

class AbstractSegmentEntity(Entity):
    def __init__(self, field: FieldEntity, model: PathSegmentModel):
        self.model = model
        self.field = field
        super().__init__(parent = field,
                         hover = HoverLambda(self),
                         select = SelectLambda(self, "segment", type = SelectorType.SOLO,
                            FonSelect = lambda i: self.onSelect,
                            FonDeselect = lambda i: self.onDeselect,
                                               ),
                         drag = DragLambda(self,
                                           FonStartDrag = self.onStartDrag,
                                           FcanDrag = self.canDrag,
                                           FonDrag = self.onDrag,
                                           FonStopDrag = self.onStopDrag
                                           ),
                         drawOrder = DrawOrder.SEGMENT)

        self.THICKNESS = 4
        self.HOVER_THICKNESS = 6

        self.colorForward = [122, 210, 118]
        self.colorForwardH = shade(self.colorForward, 0.92)
        self.colorForwardA = shade(self.colorForward, 0.7)
        self.colorReversed = [191, 118, 118]
        self.colorReversedH = shade(self.colorReversed, 0.92)
        self.colorReversedA = shade(self.colorReversed, 0.7)

    def defineAfter(self) -> None:
        self.beforePos = self.field.inchesToMouse(self.model.getBeforePos())
        self.afterPos = self.field.inchesToMouse(self.model.getAfterPos())

    def onStartDrag(self, mouse: tuple):
        self.nodeStartPosition = []
        for node in [self.model.getPrevious(), self.model.getNext()]:
            self.nodeStartPosition.append(node.getPosition())

    def canDrag(self, mouse: tuple) -> bool:

        offset = [mouse[0] - self.drag.startX, mouse[1] - self.drag.startY]
        offset = self.field.mouseToInchesScaleOnly(offset)

        self.nodeGoalPosition = []
        for i, node in enumerate([self.model.getPrevious(), self.model.getNext()]):
            newPos = addTuples(self.nodeStartPosition[i], offset)
            self.nodeGoalPosition.append(newPos)
            if not self.model.field.inBoundsInches(newPos):
                return False
        return True

    # When dragging, determine if either node is snappable. If so, do it
    def onDrag(self, mouse: tuple):


        for i, node in enumerate([self.model.getPrevious(), self.model.getNext()]):
            node.setPosition(self.nodeGoalPosition[i])

    def onSelect(self):
        pass

    def onDeselect(self):
        pass

    def onStopDrag(self):
        pass

    def getColor(self) -> tuple:
        forward = self.model.getDirection() == SegmentDirection.FORWARD

        if self.select.isSelected:
            return self.colorForwardA if forward else self.colorReversedA
        elif self.hover.isHovering:
            return self.colorForwardH if forward else self.colorReversedH
        else:
            return self.colorForward if forward else self.colorReversed