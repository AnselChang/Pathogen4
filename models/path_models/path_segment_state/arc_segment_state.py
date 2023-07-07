from __future__ import annotations
from enum import Enum, auto
import math
from typing import TYPE_CHECKING
from adapter.arc_adapter import ArcAdapter
from adapter.path_adapter import PathAttributeID
from adapter.straight_adapter import StraightAdapter
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState

from models.path_models.path_segment_state.abstract_segment_state import AbstractSegmentState
from models.path_models.path_segment_state.segment_type import SegmentType
from models.path_models.segment_direction import SegmentDirection
from utility.format_functions import formatInches
from utility.math_functions import addTuples, arcCenterFromTwoPointsAndTheta, arcFromThreePoints, distanceTuples, divideTuple, midpoint, pointPlusVector, thetaFromPoints, vectorFromThetaAndMagnitude

if TYPE_CHECKING:
    from models.path_models.path_segment_model import PathSegmentModel

"""
For arc segments.
"""

class ArcIconID(Enum):
    FORWARD_LEFT = auto()
    FORWARD_RIGHT = auto()
    REVERSE_LEFT = auto()
    REVERSE_RIGHT = auto()

class ArcSegmentState(AbstractSegmentState):

    def __init__(self, model: PathSegmentModel):

        adapter = ArcAdapter([
            ImageState(ArcIconID.FORWARD_LEFT, ImageID.CURVE_LEFT_FORWARD),
            ImageState(ArcIconID.FORWARD_RIGHT, ImageID.CURVE_RIGHT_FORWARD),
            ImageState(ArcIconID.REVERSE_LEFT, ImageID.CURVE_LEFT_REVERSE),
            ImageState(ArcIconID.REVERSE_RIGHT, ImageID.CURVE_RIGHT_REVERSE),
        ])

        super().__init__(model, adapter, SegmentType.ARC)

        # perpendicular distance from midpoint to self, signed, in inches
        self.perpDistance = 1 # initially, we start with a small amount of curve 

    def getPerpDistance(self) -> float:
        return self.perpDistance
    
    def getArcMidpoint(self) -> tuple:
        return self.arcMidpoint
    
    def getCenter(self) -> tuple:
        return self.CENTER
    
    def getRadius(self) -> float:
        return self.RADIUS
    
    def getStartAngle(self) -> float:
        return self.START_ANGLE
    
    def getStopAngle(self) -> float:
        return self.STOP_ANGLE
    
    def getPositive(self) -> bool:
        return self.POSITIVE
    
    def getArcLength(self) -> float:
        return self.ARC_LENGTH

    # set perp distance for arc, attempt to snap if possible, and update model state
    def setPerpDistance(self, perpDistance: float):

        startTheta, endTheta = self._getThetasFromPerpDistance(perpDistance)
        newStartTheta = self.model.getConstrainedStartTheta(startTheta)
        newEndTheta = self.model.getConstrainedEndTheta(endTheta)


        if newStartTheta is not None:
            perpDistance = self._getPerpDistanceFromTheta(newStartTheta, perpDistance, isStartTheta = True)
        elif newEndTheta is not None:
            perpDistance = self._getPerpDistanceFromTheta(newEndTheta, perpDistance, isStartTheta = False)


        # prevent arc from ever being perfectly straight, which causes division issues
        #print(perpDistance)
        MIN_MAGNITUDE = 0.005 * self.model.DISTANCE
        if abs(perpDistance) < MIN_MAGNITUDE:
            perpDistance = MIN_MAGNITUDE if perpDistance > 0 else -MIN_MAGNITUDE

        # finally update perp distance in model after trying to snap
        self.perpDistance = perpDistance

        # recalculate this segment and adjacent nodes
        self.model.updateThetas()
        self.model.getPrevious().onThetaChange()
        self.model.getNext().onThetaChange()

        self.model.recomputeUI()

    # Given the two node positions and some HYPOTHETICAL theta for the first node,
    # determine the perp distance which would satisfy an arc with those constraints
    def _getPerpDistanceFromTheta(self, theta: float, oldPerpDistance: float, isStartTheta: bool) -> float:

        beforePos = self.model.getPrevious().getPosition()
        afterPos = self.model.getNext().getPosition()

        if not isStartTheta:
            beforePos, afterPos = afterPos, beforePos
            theta += math.pi

        # get center and radius of resultant arc
        center = arcCenterFromTwoPointsAndTheta(*beforePos, *afterPos, theta)
        print(center)
        radius = distanceTuples(beforePos, center)

        # calculate the angles from center to before/pos
        angleToBefore = thetaFromPoints(center, beforePos)
        angleToAfter = thetaFromPoints(center, afterPos)

        #print(angleToBefore * 180 / math.pi, angleToAfter * 180 / math.pi)

        # find what position the arc midpoint would be
        angleToArcMidpoint = (angleToBefore + angleToAfter ) / 2
        vector = vectorFromThetaAndMagnitude(angleToArcMidpoint, radius)
        arcMidpoint = addTuples(center, vector)
       
        # determine perpDistance by distance between arc midpoint, and midpoint between two nodes
        nodeMidpoint = midpoint(beforePos, afterPos)
        unsignedPerpDistance = distanceTuples(nodeMidpoint, arcMidpoint)

        # hacky solution to figure out sign. there's probably math to do this the proper way.
        if oldPerpDistance > 0:
            return unsignedPerpDistance
        else: return -unsignedPerpDistance
    
    # given a HYPOTEHTICAL perp distance, return midpoint of arc
    def _getArcMidpointFromPerpDistance(self, perpDistance) -> float:
        before = self.model.getBeforePos()
        after = self.model.getAfterPos()
        mid = midpoint(before, after)
        theta = thetaFromPoints(before, after) + math.pi/2
        return pointPlusVector(mid, perpDistance, theta)    
    
    # Given a HYPOTHETICAL perp distance, return start and end thetas
    def _getThetasFromPerpDistance(self, perpDistance: float) -> tuple:

        before = self.model.getBeforePos()
        after = self.model.getAfterPos()

        arcMidpoint = self._getArcMidpointFromPerpDistance(perpDistance)
        center, radius = arcFromThreePoints(before, arcMidpoint, after)
        
         # (C)enter (T)heta for theta from center to point 1/2/3
        ct1 = thetaFromPoints(center, before)
        ct2 = thetaFromPoints(center, arcMidpoint)
        ct3 = thetaFromPoints(center, after)

        # need to figure out if clockwise or counterclockwise arc
        # determine by checking if passing 2 between 1 and 3
        # do this by shifting perspective to ct1 -> 0, and
        # mod from 0 to 2pi. note % is always sign of denom
        rct2 = (ct2 - ct1) % (math.pi*2)
        rtc3 = (ct3 - ct1) % (math.pi*2)

        positive = rct2 < rtc3

        deltaAngle = rtc3
        if not positive:
            deltaAngle = (-deltaAngle) % (math.pi*2)

        if positive:
            startTheta = ct1 + math.pi/2
            endTheta = ct3 + math.pi/2
        else:
            startTheta = ct1 - math.pi/2
            endTheta = ct3 - math.pi/2

        return startTheta, endTheta


    # Update current arc midpoint
    def _updateMidpoint(self):
        self.arcMidpoint = self._getArcMidpointFromPerpDistance(self.perpDistance)
        
    def _update(self) -> tuple: # returns [startTheta, endTheta]

        self._updateMidpoint()

        before = self.model.getBeforePos()
        after = self.model.getAfterPos()

        self.CENTER, self.RADIUS = arcFromThreePoints(before, self.arcMidpoint, after)
        self.adapter.set(PathAttributeID.XCENTER, self.CENTER[0], formatInches(self.CENTER[0]))
        self.adapter.set(PathAttributeID.YCENTER, self.CENTER[1], formatInches(self.CENTER[1]))
        self.adapter.set(PathAttributeID.RADIUS, self.RADIUS, formatInches(self.RADIUS))

        # (C)enter (T)heta for theta from center to point 1/2/3
        ct1 = thetaFromPoints(self.CENTER, before)
        ct2 = thetaFromPoints(self.CENTER, self.arcMidpoint)
        ct3 = thetaFromPoints(self.CENTER, after)

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
        self.ARC_LENGTH = deltaAngle * self.RADIUS
        self.adapter.set(PathAttributeID.ARC_LENGTH, self.ARC_LENGTH, formatInches(self.ARC_LENGTH))

        self.START_ANGLE = ct1
        self.STOP_ANGLE = ct3

        if self.POSITIVE:
            startTheta = ct1 + math.pi/2
            endTheta = ct3 + math.pi/2
        else:
            startTheta = ct1 - math.pi/2
            endTheta = ct3 - math.pi/2

        return startTheta, endTheta
        
    def _defineCenterInches(self) -> tuple:
        return self.arcMidpoint
    
    def _updateIcon(self):

        if self.model.getDirection() == SegmentDirection.FORWARD:
            icon = ArcIconID.FORWARD_LEFT if self.POSITIVE else ArcIconID.FORWARD_RIGHT
        else:
            icon = ArcIconID.REVERSE_LEFT if self.POSITIVE else ArcIconID.REVERSE_RIGHT
        self.adapter.setIconStateID(icon)