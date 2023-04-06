from BaseEntity.entity import Entity

from dimensions import Dimensions
from draw_order import DrawOrder

from Geometry.line import Line
from reference_frame import PointRef, Ref, ScalarRef
from math_functions import distanceTuples, clipLineToBox, distanceTuples, hypo
from pygame_functions import drawDottedLine
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
    def __init__(self, pixelThreshold: int, dimensions: Dimensions):

        super().__init__(
            drawOrder = DrawOrder.CONSTRAINT_LINES
        )

        self.dimensions = dimensions
        
        self.constraints: list[Line] = []
        self.PIXEL_THRESHOLD = pixelThreshold

        self.visible = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def clear(self):
        self.constraints.clear()

    def reset(self, mouse: PointRef):
        self.mouse = mouse
        self.clear()

    # The constraint is some other node with an angle to snap to
    def addConstraint(self, other: PointRef, theta: float):

        # a maximum of two linear constraints can be satisfied in 2d space
        if len(self.constraints) > 2:
            return

        line = Line(other.fieldRef, theta)

        closestPointToMouseFieldRef = line.closestPoint(self.mouse.fieldRef)
        fieldDistance = distanceTuples(self.mouse.fieldRef, closestPointToMouseFieldRef)
        screenDistance = ScalarRef(Ref.FIELD, fieldDistance).screenRef

        # avoid the scenario where the closest point to the line is the other node itself
        if distanceTuples(closestPointToMouseFieldRef, other.fieldRef) < 1:
            return

        if screenDistance < self.PIXEL_THRESHOLD:
            self.constraints.append(line)

    # Get the position after constraints
    def get(self) -> PointRef:

        if len(self.constraints) == 0:
            # no constraints applied
            return self.mouse
        

        if len(self.constraints) == 1:
            # Single constraint
            new = self.constraints[0].closestPoint(self.mouse.fieldRef)
        else:
            # Two constraints. New position is the intersection of the two linear constraints
            new = self.constraints[0].intersection(self.constraints[1])

            # intersecting lines cannot be super close to parallel
            # the intersection must be reasonably close to initial position
            if new is None or distanceTuples(self.mouse.fieldRef, new) > self.PIXEL_THRESHOLD:
                new = self.constraints[0].closestPoint(self.mouse.fieldRef)
                del self.constraints[1]

        return PointRef(Ref.FIELD, new)
    
    def isVisible(self) -> bool:
        return self.visible

    def isTouching(self, position: PointRef) -> bool:
        return False

    def getPosition(self) -> PointRef:
        return PointRef()

    # draw all constraint lines
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        for line in self.constraints:
            point = PointRef(Ref.FIELD, line.point)
            
            startPoint, pointA = clipLineToBox(point.screenRef, line.theta, 0,0,self.dimensions.FIELD_WIDTH, self.dimensions.SCREEN_HEIGHT)

            distance = distanceTuples(startPoint, pointA)
            otherDistance = hypo(self.dimensions.FIELD_WIDTH, self.dimensions.SCREEN_HEIGHT) - distance

            theta = line.theta + 3.1415
            pointB = startPoint[0] + otherDistance * math.cos(theta), startPoint[1] + otherDistance * math.sin(theta)

            drawDottedLine(screen, (0,0,0), pointA, pointB, 2, 4)
