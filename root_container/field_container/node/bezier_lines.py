from __future__ import annotations
from typing import TYPE_CHECKING
from common.draw_order import DrawOrder
from common.reference_frame import *
from entity_base.entity import Entity
from root_container.field_container.segment.segment_type import SegmentType

from utility.pygame_functions import drawDottedLine, shade
if TYPE_CHECKING:
    from root_container.field_container.segment.path_segment_entity import PathSegmentEntity

import pygame

"""
Owned by a PathSegmentEntity.
Draws lines from previous node, to start bezier theta, to stop bezier theta,
to next node
Visible only when segment is selected, or the previous/next nodes
"""
class BezierLines(Entity):

    # segmentFunction is either getPrevious or getNext
    def __init__(self, segment: PathSegmentEntity):

        self.segment = segment

        super().__init__(parent = segment, drawOrder = DrawOrder.BEFORE_NODE_SEGMENT)

        self.recomputePosition()

    def isTouching(self, point: tuple) -> bool:
        return False
    
    def isVisible(self):

        if self.segment.getSegmentType() != SegmentType.BEZIER:
            return False
        
        return self.segment.isSelfOrNodesSelected()
    
    def drawLine(self, screen, p1, p2):
        color = [255, 0, 255]
        drawDottedLine(screen, color, p1, p2, length = 5, fill = 0.3, width = 1)

    # draw the two lines if conditions are met.
    # In addition, check if there is already a constraint. if so, don't draw
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):

        prevNode = self.segment.getPrevious().getPositionRef().screenRef
        bezier1 = [self.segment.bezierTheta1.CENTER_X, self.segment.bezierTheta1.CENTER_Y]
        bezier2 = [self.segment.bezierTheta2.CENTER_X, self.segment.bezierTheta2.CENTER_Y]
        nextNode = self.segment.getNext().getPositionRef().screenRef

        self.drawLine(screen, prevNode, bezier1)
        self.drawLine(screen, bezier1, bezier2)
        self.drawLine(screen, bezier2, nextNode)