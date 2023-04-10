import itertools
from entity_base.entity import Entity

from common.dimensions import Dimensions
from common.draw_order import DrawOrder
from utility.angle_functions import deltaInHeading, parallelTheta

from utility.line import Line
from common.reference_frame import PointRef, Ref, ScalarRef
from utility.math_functions import distanceTuples, clipLineToBox, distanceTuples, hypo, thetaFromPoints
from utility.pygame_functions import drawDottedLine
import pygame, math

"""
Handle constraints for dragging path nodes
A constraint is defined as a line in which the selected node can be "snapped" to
For every line that is sufficiently close to the mouse, it is added as a constraint
Once all the constraints are added, the final position is calculated.
For 0 constraints: position is unchanged
For 1 constraints: snap to that line
For 2 constraints: snap to the intersection of the two lines

Also draws the constraints
"""

class Constraints(Entity):

    # if distance to line is less than pixel threshold, snap to line
    def __init__(self, parent, pixelThreshold: int):

        super().__init__(
            parent,
            drawOrder = DrawOrder.CONSTRAINT_LINES
        )
        
        self.positionConstraints: list[Line] = []
        self.thetaConstraints: list[float] = []
        self.PIXEL_THRESHOLD = pixelThreshold

        self.visiblePosition = False
        self.visibleTheta = False

        self.recomputePosition()

    def clear(self):
        self.clearThetaConstraints()
        self.clearPositionConstraints()

    def clearThetaConstraints(self):
        self.thetaConstraints.clear()

    def clearPositionConstraints(self):
        self.positionConstraints.clear()

    def showPosition(self):
        self.visiblePosition = True

    def hidePosition(self):
        self.visiblePosition = False

    def showTheta(self):
        self.visibleTheta = True

    def hideTheta(self):
        self.visibleTheta = False  

    def resetPositionConstraints(self, mouse: PointRef):
        self.mouse = mouse
        self.positionConstraints.clear()
        self.thetaConstraints.clear()

    # The constraint is some other node with an angle to snap to
    def addPositionConstraint(self, other: PointRef, theta: float):

        # a maximum of two linear constraints can be satisfied in 2d space
        if len(self.positionConstraints) > 2:
            return

        line = Line(other.fieldRef, theta)

        closestPointToMouseFieldRef = line.closestPoint(self.mouse.fieldRef)
        fieldDistance = distanceTuples(self.mouse.fieldRef, closestPointToMouseFieldRef)
        screenDistance = ScalarRef(Ref.FIELD, fieldDistance).screenRef

        # avoid the scenario where the closest point to the line is the other node itself
        if distanceTuples(closestPointToMouseFieldRef, other.fieldRef) < 1:
            return

        if screenDistance < self.PIXEL_THRESHOLD:
            self.positionConstraints.append(line)

    # whether there exists at least one constraint node can snap to
    def snappable(self) -> bool:
        return len(self.positionConstraints) > 0

    # Get the position after constraints
    def getPosition(self) -> PointRef:

        if len(self.positionConstraints) == 0:
            # no constraints applied
            return self.mouse
        

        if len(self.positionConstraints) == 1:
            # Single constraint
            new = self.positionConstraints[0].closestPoint(self.mouse.fieldRef)
        else:
            # Two constraints. New position is the intersection of the two linear constraints
            new = self.positionConstraints[0].intersection(self.positionConstraints[1])

            # intersecting lines cannot be super close to parallel
            # the intersection must be reasonably close to initial position
            if new is None or distanceTuples(self.mouse.fieldRef, new) > self.PIXEL_THRESHOLD:
                new = self.positionConstraints[0].closestPoint(self.mouse.fieldRef)
                del self.positionConstraints[1]

        return PointRef(Ref.FIELD, new)
    
    def resetThetaConstraints(self, myTheta: float, position: PointRef):
        self.myTheta = myTheta
        self.position = position
        self.thetaConstraintFound = False
        self.thetaConstraints.clear()
    
    # reset, constrain, and get all-in-one
    def addThetaConstraint(self, thetaToSnap: float):

        if self.thetaConstraintFound:
            return

        THETA_SNAP_TOLERANCE = 0.05

        # check both 0 and 180 degree positions
        for targetTheta in [thetaToSnap, thetaToSnap + math.pi]:
            if abs(deltaInHeading(self.myTheta, targetTheta)) < THETA_SNAP_TOLERANCE:
                self.myTheta = targetTheta
                self.thetaConstraints.append(Line(self.position.fieldRef, targetTheta))
                self.thetaConstraintFound = True
                return

    def getTheta(self) -> float:
        return self.myTheta

    def hasConstraints(self) -> bool:
        return len(self.positionConstraints) > 0 or len(self.thetaConstraints) > 0
    
    # Find whether a constraint's line is identical to the one specified positionFieldRef and theta
    def hasConstraint(self, positionFieldRef, theta) -> bool:
        for constraint in itertools.chain(self.positionConstraints, self.thetaConstraints):
            pointToLineAngle = thetaFromPoints(constraint.point, positionFieldRef)
            if parallelTheta(pointToLineAngle, theta, 0.01) and parallelTheta(constraint.theta, theta, 0.01):
                return True
        return False
    
    def isVisible(self) -> bool:
        return self.visiblePosition or self.visibleTheta

    def isTouching(self, position: PointRef) -> bool:
        return False
    
    def _point(self, startPoint, distance, theta):
        return startPoint[0] + distance * math.cos(theta), startPoint[1] + distance * math.sin(theta)

    # draw all constraint lines
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        if self.interactor.selected.moreThanOne():
            return

        visible = []
        if self.visiblePosition:
            visible.extend(self.positionConstraints)
        if self.visibleTheta:
            visible.extend(self.thetaConstraints)

        dist = hypo(self.dimensions.FIELD_WIDTH, self.dimensions.SCREEN_HEIGHT)
        for line in visible:
            point = PointRef(Ref.FIELD, line.point).screenRef

            pointA = self._point(point, dist, line.theta)
            pointB = self._point(point, dist, line.theta + 3.1415)

            drawDottedLine(screen, (30,255,30), pointA, pointB, length = 12, fill = 0.5, width = 2)
