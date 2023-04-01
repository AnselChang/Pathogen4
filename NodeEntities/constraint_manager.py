from Geometry.line import Line
from reference_frame import PointRef, Ref, ScalarRef
from math_functions import distanceTuples

"""
Handle constraints for dragging path nodes
A constraint is defined as a line in which the selected node can be "snapped" to
For every line that is sufficiently close to the mouse, it is added as a constraint
Once all the constraints are added, the final position is calculated.
For 0 constraints: position is unchanged
For 1 constraints: snap to that line
For 2 constraints: snap to the intersection of the two lines
"""

class ConstraintManager:

    # if distance to line is less than pixel threshold, snap to line
    def __init__(self, mouse: PointRef, pixelThreshold: int):
        self.mouse = mouse
        self.constraints: list[Line] = []

        self.PIXEL_THRESHOLD = pixelThreshold

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
                return self.mouse

        return PointRef(Ref.FIELD, new)