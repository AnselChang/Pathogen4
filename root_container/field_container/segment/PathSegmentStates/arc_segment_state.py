from __future__ import annotations
import math
from typing import TYPE_CHECKING
from adapter.arc_adapter import ArcAdapter, ArcAttributeID
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from root_container.field_container.segment.segment_direction import SegmentDirection

from root_container.field_container.segment.segment_type import PathSegmentType
from utility.angle_functions import deltaInHeading, headingDiff
from utility.format_functions import formatDegrees, formatInches
from utility.math_functions import arcCenterFromTwoPointsAndTheta, arcFromThreePoints, distancePointToLine, distanceTuples, getArcMidpoint, pointTouchingLine, thetaFromArc, thetaFromPoints
from utility.pygame_functions import drawArcFromCenterAngles, drawLine, drawVector
if TYPE_CHECKING:
    from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
    from root_container.field_container.node.path_node_entity import PathNodeEntity

from abc import ABC, abstractmethod
from enum import Enum, auto
from common.reference_frame import PointRef, Ref, ScalarRef, VectorRef
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
        super().__init__(PathSegmentType.ARC, segment)
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

        self.notify()

    # attempt to constraint self.THETA1 and self.THETA2 to the opposing thetas for their nodes
    def constrainTheta(self):
        prevNode = self.segment.getPrevious()
        nextNode = self.segment.getNext()
        prevNode.constraints.resetThetaConstraints(self.THETA1, prevNode.getPositionRef())
        nextNode.constraints.resetThetaConstraints(self.THETA2, nextNode.getPositionRef())

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            return
        
        # HANDLE THETA1

        # attempt to constrain to previous node theta. Note that Constraints already handles the 180 cases
        if prevNode.getPrevious() is not None:
            prevNode.constraints.addThetaConstraint(prevNode.START_THETA)
        
        # attempt to constrain to cardinal directions. Note that Constraints already handles the 180 cases
        prevNode.constraints.addThetaConstraint(0)
        prevNode.constraints.addThetaConstraint(math.pi / 2)

        newTheta1 = prevNode.constraints.getTheta()
        if newTheta1 != self.THETA1:
            # recalculate arc but with newTheta1
            self.THETA1 = newTheta1
            dx = self.p3.fieldRef[0] - self.p1.fieldRef[0]
            dy = self.p3.fieldRef[1] - self.p1.fieldRef[1]
            self.THETA2 = thetaFromArc(self.THETA1, dx, dy)

            if headingDiff(self.THETA1, self.THETA2) < 1e-3:
                # cannot be collinear
                prevNode.constraints.clearThetaConstraints()
            else:
                self.recalculateArcFromTheta()
                self.notify()
                return
        
        # HANDLE THETA2
        # attempt to constrain to previous node theta. Note that Constraints already handles the 180 cases
        if nextNode.getNext() is not None:
            nextNode.constraints.addThetaConstraint(nextNode.END_THETA)
        
        # attempt to constrain to cardinal directions. Note that Constraints already handles the 180 cases
        nextNode.constraints.addThetaConstraint(0)
        nextNode.constraints.addThetaConstraint(math.pi / 2)

        newTheta2 = nextNode.constraints.getTheta()
        if newTheta2 != self.THETA2:
            # recalculate arc but with newTheta1
            self.THETA2 = newTheta2
            dx = self.p3.fieldRef[0] - self.p1.fieldRef[0]
            dy = self.p3.fieldRef[1] - self.p1.fieldRef[1]
            self.THETA1 = thetaFromArc(self.THETA2, dx, dy)

            if headingDiff(self.THETA1, self.THETA2) < 1e-3:
                # cannot be collinear
                prevNode.constraints.clearThetaConstraints()
            else:
                self.recalculateArcFromTheta()
                self.notify()
                return
        
        
        
    # Given: theta1, theta2, self.p1, self.p3.
    # Find: self.p2, self.CENTER, self.RADIUS, self.ARC_LENGTH, self.THETA2
    def recalculateArcFromTheta(self):
        self.CENTER = PointRef(Ref.FIELD, arcCenterFromTwoPointsAndTheta(*self.p1.fieldRef, *self.p3.fieldRef, self.THETA1))
        self.RADIUS = ScalarRef(Ref.FIELD, distanceTuples(self.CENTER.fieldRef, self.p1.fieldRef))

        ct1 = thetaFromPoints(self.CENTER.fieldRef, self.p1.fieldRef)
        ct3 = thetaFromPoints(self.CENTER.fieldRef, self.p3.fieldRef)
        self.START_ANGLE = ct1
        self.STOP_ANGLE = ct3
        deltaAngle = (ct3 - ct1) % (math.pi*2)
        if not self.POSITIVE:
            deltaAngle = (-deltaAngle) % (math.pi*2)
        self.ARC_LENGTH = ScalarRef(Ref.FIELD, deltaAngle * self.RADIUS.fieldRef)

        # brute force finding which direction it is
        p2Theta = ct1 + deltaInHeading(ct3, ct1) / 2
        self.p2 = self.CENTER + VectorRef(Ref.FIELD, magnitude = self.RADIUS.fieldRef, heading = p2Theta)
        if not self.isTouching(self.p2.screenRef):
            self.p2 = self.CENTER + VectorRef(Ref.FIELD, magnitude = self.RADIUS.fieldRef, heading = p2Theta + math.pi)

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

        if self.segment.getDirection() == SegmentDirection.FORWARD:
            icon = ArcIconID.FORWARD_LEFT if self.POSITIVE else ArcIconID.FORWARD_RIGHT
        else:
            icon = ArcIconID.REVERSE_LEFT if self.POSITIVE else ArcIconID.REVERSE_RIGHT
        self.adapter.setIconStateID(icon)

    def getStartTheta(self) -> float:
        return self.THETA1

    def getEndTheta(self) -> float:
        return self.THETA2


    # Checks if it inside the start/stop angle range, and
    # if screenRef of magnitudes are within some margin
    def isTouching(self, mouse: tuple) -> bool:

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
        return abs(dist - self.RADIUS.screenRef) < self.segment.getThickness(True)

    # for now, return midpoint between previous and next nodes. But
    # this should be changed to a point on the arc itself
    def getCenter(self) -> tuple:
        if self.segment.getPrevious() is None or self.segment.getNext() is None:
            return (0, 0)

        return self.p2.screenRef

    # Draw an arc given arc calculations in updateAdapter()
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        # how smooth the arc should be
        RESOLUTION = 1

        color = self.segment.getColor(isActive, isHovered)
        drawArcFromCenterAngles(screen, self.START_ANGLE, self.STOP_ANGLE, self.POSITIVE,
                                color, self.CENTER.screenRef, self.RADIUS.screenRef, 
                                width = self.segment.getThickness(),
                                numSegments = self.ARC_LENGTH.screenRef * RESOLUTION
                                )



