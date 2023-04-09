from __future__ import annotations
import math
from typing import TYPE_CHECKING
from adapter.arc_adapter import ArcAdapter, ArcAttributeID
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from root_container.field_container.segment.segment_direction import SegmentDirection

from root_container.field_container.segment.segment_type import SegmentType
from utility.angle_functions import deltaInHeading
from utility.format_functions import formatDegrees, formatInches
from utility.math_functions import arcCenterFromTwoPointsAndTheta, arcFromThreePoints, distancePointToLine, distanceTuples, getArcMidpoint, pointTouchingLine, thetaFromArc, thetaFromPoints
from utility.pygame_functions import drawArcFromCenterAngles, drawLine, drawVector
if TYPE_CHECKING:
    from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
    from root_container.field_container.node.path_node_entity import PathNodeEntity

from abc import ABC, abstractmethod
from enum import Enum, auto
from common.reference_frame import PointRef, Ref, ScalarRef
from entity_base.entity import Entity
from data_structures.linked_list import LinkedListNode
from adapter.path_adapter import PathAdapter
from root_container.field_container.segment.path_segment_state import PathSegmentState

import pygame

"""
An arc segment is controlled by a CurveNode which lies at the perpendicular bisector
of the two nodes.
"""

class ArcIconID(Enum):
    FORWARD_LEFT = auto()
    FORWARD_RIGHT = auto()
    REVERSE_LEFT = auto()
    REVERSE_RIGHT = auto()

class ArcSegmentState(PathSegmentState):
    def __init__(self, segment: PathSegmentEntity | LinkedListNode) -> None:
        super().__init__(SegmentType.ARC, segment)
        self.adapter = ArcAdapter([
            ImageState(ArcIconID.FORWARD_LEFT, ImageID.CURVE_LEFT_FORWARD),
            ImageState(ArcIconID.FORWARD_RIGHT, ImageID.CURVE_RIGHT_FORWARD),
            ImageState(ArcIconID.REVERSE_LEFT, ImageID.CURVE_LEFT_REVERSE),
            ImageState(ArcIconID.REVERSE_RIGHT, ImageID.CURVE_RIGHT_REVERSE),
        ])

    def getAdapter(self) -> PathAdapter:
        return self.adapter
    
    def recalculateArcFromArcCurveNode(self):

        # find 3 points with field reference frame
        self.p1 = self.segment.getPrevious().getPositionRef()
        self.p2 = self.segment.arcNode.positionRef
        self.p3 = self.segment.getNext().getPositionRef()

        # compute center and radius of arc
        c, r = arcFromThreePoints(self.p1.fieldRef, self.p2.fieldRef, self.p3.fieldRef)
        self.CENTER = PointRef(Ref.FIELD, c)
        self.RADIUS = ScalarRef(Ref.FIELD, r)

        # (C)enter (T)heta for theta from center to point 1/2/3
        ct1 = thetaFromPoints(self.CENTER.fieldRef, self.p1.fieldRef)
        ct2 = thetaFromPoints(self.CENTER.fieldRef, self.p2.fieldRef)
        ct3 = thetaFromPoints(self.CENTER.fieldRef, self.p3.fieldRef)

        # need to figure out if clockwise or counterclockwise arc
        # determine by checking if passing 2 between 1 and 3
        # do this by shifting perspective to ct1 -> 0, and
        # mod from 0 to 2pi. note % is always sign of denom
        rct2 = (ct2 - ct1) % (math.pi*2)
        rtc3 = (ct3 - ct1) % (math.pi*2)
        
        self.CT1 = ct1
        self.CT2 = ct2
        self.CT3 = ct3
        self.POSITIVE = rct2 < rtc3

        deltaAngle = rtc3
        if not self.POSITIVE:
            deltaAngle = (-deltaAngle) % (math.pi*2)
        self.ARC_LENGTH = ScalarRef(Ref.FIELD, deltaAngle * self.RADIUS.fieldRef)

        self.START_ANGLE = ct1
        self.STOP_ANGLE = ct3

        if self.POSITIVE:
            self.THETA1 = ct1 + math.pi/2
            self.THETA2 = ct3 + math.pi/2
        else:
            self.THETA1 = ct1 - math.pi/2
            self.THETA2 = ct3 - math.pi/2

    # attempt to constraint self.THETA1 and self.THETA2 to the opposing thetas for their nodes
    def constrainTheta(self):
        prevNode = self.segment.getPrevious()
        newTheta1 = prevNode.constraints.handleThetaConstraint(prevNode.getPositionRef(), self.THETA1, prevNode.START_THETA)
        if newTheta1 != self.THETA1:
            # recalculate arc but with newTheta1
            self.recalculateArcFromTheta1(newTheta1)
            print("snap")
            return
        
        # Only if snapping to previous failed, try snapping to next
        nextNode = self.segment.getNext()
        newTheta2 = nextNode.constraints.handleThetaConstraint(nextNode.getPositionRef(), self.THETA2, nextNode.END_THETA)
        if newTheta2 != self.THETA2:
            # recalculate arc but with newTheta2
            self.recalculateArcFromTheta2(newTheta2)
            return
        
        
    # Given: theta1, self.p1, self.p3.
    # Find: self.p2, self.CENTER, self.RADIUS, self.ARC_LENGTH, self.THETA2
    def recalculateArcFromTheta1(self, theta1: float):
        self.THETA1 = theta1
        self.CENTER = PointRef(Ref.FIELD, arcCenterFromTwoPointsAndTheta(*self.p1.fieldRef, *self.p3.fieldRef, theta1))
        self.RADIUS = ScalarRef(Ref.FIELD, distanceTuples(self.CENTER.fieldRef, self.p1.fieldRef))

        # two possible midpoints
        m1, m2 = getArcMidpoint(*self.p1.fieldRef, *self.p3.fieldRef, self.RADIUS.fieldRef)

        # THIS IS PROBLEM, NOT PICKING RIGHT P2 PROBABLY
        # pick the one closer to the original midpoint. definitely not the best way to do it, but it's the easiest
        if distanceTuples(m1, self.p2.fieldRef) < distanceTuples(m2, self.p2.fieldRef):
            self.p2 = PointRef(Ref.FIELD, m1)
        else:
            self.p2 = PointRef(Ref.FIELD, m2)

        ct1 = thetaFromPoints(self.CENTER.fieldRef, self.p1.fieldRef)
        ct3 = thetaFromPoints(self.CENTER.fieldRef, self.p3.fieldRef)
        self.START_ANGLE = ct1
        self.STOP_ANGLE = ct3
        deltaAngle = (ct3 - ct1) % (math.pi*2)
        if not self.POSITIVE:
            deltaAngle = (-deltaAngle) % (math.pi*2)
        self.ARC_LENGTH = ScalarRef(Ref.FIELD, deltaAngle * self.RADIUS.fieldRef)

        dx = self.p3.fieldRef[0] - self.p1.fieldRef[0]
        dy = self.p3.fieldRef[1] - self.p1.fieldRef[1]
        self.THETA2 = thetaFromArc(self.THETA1, dx, dy)

        # now, force ArcCurveNode to this new position
        d = distancePointToLine(*self.p2.fieldRef, *self.p3.fieldRef, *self.p1.fieldRef, True)
        self.segment.arcNode.setPerpDistance(d)


    def recalculateArcFromTheta2(self, theta2: float):
        pass


    """
    ADAPTER MUST SET:
        X1, Y1, X2, Y2
        XCENTER, YCENTER,
        RADIUS, ARC_LENGTH
        THETA1, THETA2
    """
    def updateAdapter(self) -> None:

        self.recalculateArcFromArcCurveNode()

        # Set positions
        self.adapter.set(ArcAttributeID.X1, self.p1.fieldRef[0], formatInches(self.p1.fieldRef[0]))
        self.adapter.set(ArcAttributeID.Y1, self.p1.fieldRef[1], formatInches(self.p1.fieldRef[1]))
        self.adapter.set(ArcAttributeID.X2, self.p3.fieldRef[0], formatInches(self.p3.fieldRef[0]))
        self.adapter.set(ArcAttributeID.Y2, self.p3.fieldRef[1], formatInches(self.p3.fieldRef[1]))

        self.adapter.set(ArcAttributeID.XCENTER, self.CENTER.fieldRef[0], formatInches(self.CENTER.fieldRef[0]))
        self.adapter.set(ArcAttributeID.YCENTER, self.CENTER.fieldRef[1], formatInches(self.CENTER.fieldRef[1]))
        self.adapter.set(ArcAttributeID.RADIUS, self.RADIUS.fieldRef, formatInches(self.RADIUS.fieldRef))

        self.adapter.set(ArcAttributeID.ARC_LENGTH, self.ARC_LENGTH.fieldRef, formatInches(self.ARC_LENGTH.fieldRef))

        self.adapter.set(ArcAttributeID.THETA1, self.THETA1, formatDegrees(self.THETA1))
        self.adapter.set(ArcAttributeID.THETA2, self.THETA2, formatDegrees(self.THETA2))


    def getStartTheta(self) -> float:
        return self.THETA1

    def getEndTheta(self) -> float:
        return self.THETA2


    # Checks if it inside the start/stop angle range, and
    # if screenRef of magnitudes are within some margin
    def isTouching(self, mouse: tuple) -> bool:

        HITBOX_THICKNESS = 7 # in raw pixels

        ctm = thetaFromPoints(self.CENTER.screenRef, mouse)
        rctm = (ctm - self.CT1) % (math.pi*2)
        rtc3 = (self.CT3 - self.CT1) % (math.pi*2)
        angleInside = rtc3 < rctm

        if self.POSITIVE:
            angleInside = not angleInside

        if not angleInside:
            return False

        # not in start/stop angle range
        # check if mouse is within radius
        dist = distanceTuples(self.CENTER.screenRef, mouse)
        return abs(dist - self.RADIUS.screenRef) < HITBOX_THICKNESS

    # for now, return midpoint between previous and next nodes. But
    # this should be changed to a point on the arc itself
    def getCenter(self) -> tuple:
        if self.segment.getPrevious() is None or self.segment.getNext() is None:
            return (0, 0)

        return self.p2.screenRef

    # Draw an arc given arc calculations in updateAdapter()
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        # how smooth the arc should be
        RESOLUTION = 10

        color = self.segment.getColor(isActive, isHovered)
        drawArcFromCenterAngles(screen, self.START_ANGLE, self.STOP_ANGLE, self.POSITIVE,
                                color, self.CENTER.screenRef, self.RADIUS.screenRef, 
                                width = self.segment.thickness,
                                numSegments = self.ARC_LENGTH.screenRef * RESOLUTION
                                )
        
        # draw theta directions for testing
        drawVector(screen, *self.p1.screenRef, self.THETA1, 30)
        drawVector(screen, *self.p3.screenRef, self.THETA2, 30)

        pygame.draw.circle(screen, (0,0,255), self.p2.screenRef, 5)


