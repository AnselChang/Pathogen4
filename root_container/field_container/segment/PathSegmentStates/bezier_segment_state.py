from __future__ import annotations
from typing import TYPE_CHECKING
from adapter.arc_adapter import ArcAdapter
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from root_container.field_container.segment.segment_direction import SegmentDirection
import constants
from root_container.field_container.segment.segment_type import SegmentType
from utility.bezier_functions import generate_cubic_points
from utility.bezier_functions_2 import fast_points_cubic_bezier, normalized_points_cubic_bezier
from utility.math_functions import pointTouchingLine, thetaFromPoints
from utility.pygame_functions import drawLine
if TYPE_CHECKING:
    from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
    from root_container.field_container.node.path_node_entity import PathNodeEntity

from abc import ABC, abstractmethod
from enum import Enum, auto
from common.reference_frame import PointRef, Ref
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

        self.points: list[PointRef] = None # the bezier points
        self.THETA1 = None
        self.THETA2 = None

        self.FAST_BEZIER_RESOLUTION = 1 # 5
        self.MOUSE_BEZIER_RESOLUTION = 0.3

    def getAdapter(self) -> PathAdapter:
        return self.adapter
    
    # callback when a node attached to this segment has stopped dragging
    # In this case, recompute bezier but with equidistant points
    def onNodeStopDrag(self):
        self.recomputeBezier(False)
        self.segment.recomputePosition()
    
    # compute bezier curve purely through field ref. but store points as PointRef
    # fast is not normalized. Used when dragging
    # slow is normalized. Used when mouse released
    def recomputeBezier(self, fast: bool = True):
        # sometimes redundant, but must guarantee that the bezier nodes are initialized
        self.segment.bezierTheta1.recomputePosition()
        self.segment.bezierTheta2.recomputePosition()

        # get the four control points
        p0 = self.segment.getPrevious().getPositionRef().fieldRef
        p1 = self.segment.bezierTheta1.getPositionRef().fieldRef
        p2 = self.segment.bezierTheta2.getPositionRef().fieldRef
        p3 = self.segment.getNext().getPositionRef().fieldRef

        
        if fast:
            points = fast_points_cubic_bezier(self.FAST_BEZIER_RESOLUTION, p0, p1, p2, p3)
            # no need to update self.MOUSE_DETECTION_POINTS while dragging
        else:
            points = normalized_points_cubic_bezier(constants.BEIZER_SEGMENT_LENGTH, p0, p1, p2, p3)

            """
            In addition, compute another set of points with much lower resolution.
            This list of points will be used for detecting if the mouse is hovering
            over the segment, which should reduce performance overhead
            """
            self.MOUSE_DETECTION_POINTS = fast_points_cubic_bezier(self.MOUSE_BEZIER_RESOLUTION, p0, p1, p2, p3)

        # to avoid null scenarios, set start and end location as points if length < 2
        if len(points) < 2:
            points = [p0, p3]

        self.points = [PointRef(Ref.FIELD, point) for point in points]

        # calculate start/end theta from control points
        self.THETA1 = thetaFromPoints(p0, p1)
        self.THETA2 = thetaFromPoints(p2, p3)

        self.MIDPOINT: PointRef = self.points[len(self.points) // 2]

    
    def updateAdapter(self) -> None:
        self.recomputeBezier()


    def getStartTheta(self) -> float:
        return self.THETA1

    def getEndTheta(self) -> float:
        return self.THETA2


    # for now, returns if touching the straight line between two nodes
    # but this should be changed to check if touching the arc itself
    def isTouching(self, position: tuple) -> bool:
        x1, y1 = self.segment.getPrevious().getPositionRef().screenRef
        x2, y2 = self.segment.getNext().getPositionRef().screenRef
        return pointTouchingLine(*position, x1, y1, x2, y2, self.segment.hitboxThickness)

    # The midpoint of the list of points in the bezier curve
    def getCenter(self) -> tuple:
        return self.MIDPOINT.screenRef

    # Iterate through list of points and draw thick lines between them
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        color = self.segment.getColor(isActive, isHovered)

        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i].screenRef
            x2, y2 = self.points[i+1].screenRef
            drawLine(screen, color, x1, y1, x2, y2, self.segment.getThickness(), None)

        # Draw every point if selected
        if self.segment.isSelfOrNodesSelected():
            for point in self.points:
                x, y = point.screenRef
                pygame.draw.circle(screen, (0,0,0), (x, y), 1)

