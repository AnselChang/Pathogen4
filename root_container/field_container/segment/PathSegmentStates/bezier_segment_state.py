from __future__ import annotations
from typing import TYPE_CHECKING
from adapter.arc_adapter import ArcAdapter
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from root_container.field_container.segment.segment_direction import SegmentDirection

from root_container.field_container.segment.segment_type import SegmentType
from utility.math_functions import pointTouchingLine
from utility.pygame_functions import drawLine
if TYPE_CHECKING:
    from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
    from root_container.field_container.node.path_node_entity import PathNodeEntity

from abc import ABC, abstractmethod
from enum import Enum, auto
from common.reference_frame import PointRef
from entity_base.entity import Entity
from data_structures.linked_list import LinkedListNode
from adapter.path_adapter import PathAdapter
from root_container.field_container.segment.path_segment_state import PathSegmentState

import pygame

"""
A bezier segment is controlled by two nodes and their BezierThetaEntities
"""

class ArcIconID(Enum):
    FORWARD_LEFT = auto()
    FORWARD_RIGHT = auto()
    REVERSE_LEFT = auto()
    REVERSE_RIGHT = auto()

class BezierSegmentState(PathSegmentState):
    def __init__(self, segment: PathSegmentEntity | LinkedListNode) -> None:
        super().__init__(SegmentType.BEZIER, segment)
        self.adapter = ArcAdapter([
            ImageState(ArcIconID.FORWARD_LEFT, ImageID.CURVE_LEFT_FORWARD),
            ImageState(ArcIconID.FORWARD_RIGHT, ImageID.CURVE_RIGHT_FORWARD),
            ImageState(ArcIconID.REVERSE_LEFT, ImageID.CURVE_LEFT_REVERSE),
            ImageState(ArcIconID.REVERSE_RIGHT, ImageID.CURVE_RIGHT_REVERSE),
        ])

        self.THETA1 = None
        self.THETA2 = None

    def getAdapter(self) -> PathAdapter:
        return self.adapter

    
    def updateAdapter(self) -> None:
        # If its the first time, set the initial theta to be the angles if
        # the segment was a straight line
        if self.THETA1 is None:
            self.THETA1 = (self.segment.getNext().getPositionRef() - self.segment.getPrevious().getPositionRef()).theta()
        self.THETA2 = self.THETA1


    def getStartTheta(self) -> float:
        return self.THETA1

    def getEndTheta(self) -> float:
        return self.THETA2


    # for now, returns if touching the straight line between two nodes
    # but this should be changed to check if touching the arc itself
    def isTouching(self, position: PointRef) -> bool:
        x1, y1 = self.segment.getPrevious().getPositionRef().screenRef
        x2, y2 = self.segment.getNext().getPositionRef().screenRef
        return pointTouchingLine(*position, x1, y1, x2, y2, self.segment.hitboxThickness)

    # for now, return midpoint between previous and next nodes. But
    # this should be changed to a point on the arc itself
    def getCenter(self) -> tuple:
        if self.segment.getPrevious() is None or self.segment.getNext() is None:
            return (0, 0)

        fpos = self.segment.getPrevious().getPositionRef()
        spos = self.segment.getNext().getPositionRef()
        return (fpos + (spos - fpos) / 2).screenRef

    # for now, draw a line between previous and next nodes. But
    # this should be changed to draw the arc itself
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        x1, y1 = self.segment.getPrevious().getPositionRef().screenRef
        x2, y2 = self.segment.getNext().getPositionRef().screenRef

        drawLine(screen, self.segment.getColor(isActive, isHovered), x1, y1, x2, y2, self.segment.thickness, None)

