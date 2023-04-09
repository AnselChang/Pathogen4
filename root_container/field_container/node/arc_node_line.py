from __future__ import annotations
import math
from typing import TYPE_CHECKING
from common.draw_order import DrawOrder
from common.reference_frame import *
from entity_base.entity import Entity
from entity_base.listeners.drag_listener import DragLambda

from entity_base.listeners.select_listener import SelectLambda, SelectorType
from root_container.field_container.segment.segment_type import SegmentType
from utility.pygame_functions import drawDottedLine, shade
if TYPE_CHECKING:
    from root_container.field_container.node.path_node_entity import PathNodeEntity
    from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
    from root_container.field_container.node.arc_curve_node import ArcCurveNode
import pygame

"""
Drawn from the ArcCurveNode to the midpoint.
Dotted line drawn behind the nodes and segments.
Same color as ArcCurveNode
"""
class ArcNodeLine(Entity):

    # segmentFunction is either getPrevious or getNext
    def __init__(self, arcCurveNode: ArcCurveNode):

        self.arcCurveNode = arcCurveNode

        super().__init__(parent = arcCurveNode, drawOrder = DrawOrder.THETA_LINE)

        self.recomputePosition()

    # return cached position in screen coordinates
    def defineCenter(self) -> tuple:
        a = self.arcCurveNode.positionRef
        b = self.arcCurveNode.segmentMidpoint
        pos = (a + (b - a) / 2).screenRef

        # cache positions for drawing
        self.a = a.screenRef
        self.b = b.screenRef
        return pos


    # draw from self.a to self.b, which is from the arcCurveNode to the midpoint
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):

        color = self.arcCurveNode.COLOR_H if isHovered else self.arcCurveNode.COLOR
        drawDottedLine(screen, color, self.a, self.b, length = 10, fill = 0.5, width = 1)
        pygame.draw.circle(screen, (0,0,0), self.a, 10)
        pygame.draw.circle(screen, (0,0,0), self.b, 10)