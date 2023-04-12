from __future__ import annotations
from typing import TYPE_CHECKING
from adapter.bezier_adapter import BezierAdapter, BezierAttributeID
from common.image_manager import ImageID
from data_structures.observer import Observer
from entity_base.image.image_state import ImageState
from root_container.field_container.segment.segment_direction import SegmentDirection
import constants
from root_container.field_container.segment.segment_type import PathSegmentType
from utility.bezier_functions import generate_cubic_points
from utility.bezier_functions_2 import fast_points_cubic_bezier, normalized_points_cubic_bezier
from utility.format_functions import formatDegrees, formatInches
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

class BezierIconID(Enum):
    BEZIER = auto()

class BezierSegmentState(PathSegmentState, Observer):
    def __init__(self, segment: PathSegmentEntity | LinkedListNode) -> None:
        super().__init__(PathSegmentType.BEZIER, segment)
        self.adapter = BezierAdapter([
            ImageState(BezierIconID.BEZIER, ImageID.BEZIER),
        ])

        self.points: list[PointRef] = None # the bezier points in fieldRef
        self.MOUSE_DETECTION_POINTS = None # the mouse bezier points in screenRef


        self.THETA1 = None
        self.THETA2 = None

        self.FAST_BEZIER_RESOLUTION = 1 # 5
        self.MOUSE_BEZIER_RESOLUTION = 0.3
        

        # every time the screen shifts, recompute the mouse detection points
        self.segment.transform.subscribe(self, onNotify = self.onScreenRefChange)

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

        self.START_POINT = p0
        self.END_POINT = p3

        if fast:
            points = fast_points_cubic_bezier(self.FAST_BEZIER_RESOLUTION, p0, p1, p2, p3)
            # no need to update self.MOUSE_DETECTION_POINTS while dragging
        else:
            points = normalized_points_cubic_bezier(constants.BEIZER_SEGMENT_LENGTH, p0, p1, p2, p3)

        # to avoid null scenarios, set start and end location as points if length < 2
        if len(points) < 2:
            points = [p0, p3]

        self.points = [PointRef(Ref.FIELD, point) for point in points]

        # calculate start/end theta from control points
        self.THETA1 = thetaFromPoints(p0, p1)
        self.THETA2 = thetaFromPoints(p2, p3)

        self.MIDPOINT: PointRef = self.points[len(self.points) // 2]

        if fast:
            self.recomputeMouseDetectionPoints()

    def onScreenRefChange(self):
        if self.segment.getSegmentType() == PathSegmentType.BEZIER:
            self.recomputeMouseDetectionPoints()

    # called anytime the bezier nodes are shifted IN SCREEN COORDINATES
    def recomputeMouseDetectionPoints(self):
        # get the four control points
        p0 = self.segment.getPrevious().getPositionRef().screenRef
        p1 = self.segment.bezierTheta1.getPositionRef().screenRef
        p2 = self.segment.bezierTheta2.getPositionRef().screenRef
        p3 = self.segment.getNext().getPositionRef().screenRef

        self.MOUSE_DETECTION_POINTS = fast_points_cubic_bezier(self.MOUSE_BEZIER_RESOLUTION, p0, p1, p2, p3)
    
    def updateAdapter(self) -> None:
        self.recomputeBezier()

        self.adapter.set(BezierAttributeID.X1, self.START_POINT[0], formatInches(self.START_POINT[0]))
        self.adapter.set(BezierAttributeID.Y1, self.START_POINT[1], formatInches(self.START_POINT[1]))
        self.adapter.set(BezierAttributeID.X2, self.END_POINT[0], formatInches(self.END_POINT[0]))
        self.adapter.set(BezierAttributeID.Y2, self.END_POINT[1], formatInches(self.END_POINT[1]))

        self.adapter.set(BezierAttributeID.THETA1, self.THETA1, formatDegrees(self.THETA1))
        self.adapter.set(BezierAttributeID.THETA2, self.THETA2, formatDegrees(self.THETA2))

        self.adapter.setIconStateID(BezierIconID.BEZIER)


    def getStartTheta(self) -> float:
        return self.THETA1

    def getEndTheta(self) -> float:
        return self.THETA2


    # Use the low-res self.MOUSE_DETECTION_POINTS
    # Check if mouse is touching any of those lines
    def isTouching(self, position: tuple) -> bool:

        # sliding window for making lines across points
        # Increases effective hitbox size
        WINDOW_SIZE = 5

        # loop through each segment
        for i in range(len(self.MOUSE_DETECTION_POINTS) - WINDOW_SIZE):
            x1, y1 = self.MOUSE_DETECTION_POINTS[i]
            x2, y2 = self.MOUSE_DETECTION_POINTS[i+WINDOW_SIZE]
            if pointTouchingLine(*position, x1, y1, x2, y2, self.segment.getThickness(True)):
                return True

        return False

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

