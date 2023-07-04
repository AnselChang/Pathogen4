from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.path_models.path_node_model import PathNodeModel
    from root_container.field_container.field_entity import FieldEntity

from utility.angle_functions import Direction
from utility.line import Line
from utility.math_functions import distancePointToLine, distanceTuples

class Constraint:

    def __init__(self, line: Line, nodes: list[PathNodeModel]):
        self.line = line
        self.nodes = nodes

class ConstraintSolver:

    def __init__(self, fieldEntity: FieldEntity):
        self.resetConstraints()
        self.field = fieldEntity

    def resetConstraints(self):
        self.constraints: list[Constraint] = []
        self._position = None
        self._snapped = None
        self._activeConstraints: list[Constraint] = []

    # add a constraint given a line and list of nodes defining constraint
    def addConstraint(self, line: Line, nodes: list[PathNodeModel]):
        self.constraints.append(Constraint(line, nodes))

    # add four cardinal constraints based on node
    def addCardinalConstraints(self, node: PathNodeModel):
        self.addConstraint(Line(node.position, theta = Direction.NORTH), [node])
        self.addConstraint(Line(node.position, theta = Direction.EAST), [node])
        self.addConstraint(Line(node.position, theta = Direction.SOUTH), [node])
        self.addConstraint(Line(node.position, theta = Direction.WEST), [node])

    # return a subset of self.constraints that is nearby the given point within some threshold
    def filterNearbyConstraints(self, position: tuple, distance: float) -> list[Constraint]:
        nearbyConstraints = []
        for constraint in self.constraints:
            p1 = constraint.line.p1
            p2 = constraint.line.p2
            if distancePointToLine(*position, *p1, *p2) < distance:
                nearbyConstraints.append(constraint)
        return nearbyConstraints

    # runs the constraints algorithm on the given point
    # also return the position
    def constrain(self, position: tuple) -> tuple:

        THRESHOLD_PIXELS = 3 # how close the node must be to the line to snap (in pixels)

        # filter nearby constraints
        thresholdInches = self.field.scalarMouseToInches(THRESHOLD_PIXELS)
        constraints = self.filterNearbyConstraints(position, thresholdInches)

        # if there are no constraints, then do not change position
        if len(constraints) == 0:
            self._snapped = False
            self._position = position
            self._activeConstraints = []
        elif len(constraints) == 1:
            # Snap to single constraint
            self._snapped = True
            self._position = constraints[0].line.closestPoint(position)
            self._activeConstraints = constraints[0:1]
        else:
            # Snap to the first two constraints
            # Two constraints. New position is the intersection of the two linear constraints
            self._snapped = True
            self._position = constraints[0].line.intersection(constraints[1].line)
            self._activeConstraints = constraints[0:2]

            # intersecting lines cannot be super close to parallel
            # the intersection must be reasonably close to initial position
            if self._position is None or distanceTuples(position, self._position) > thresholdInches*1.5:
                # Snap to single constraint
                self._position = constraints[0].line.closestPoint(position)
                self._activeConstraints = constraints[0:1]
        
        return self._position
    
    # get the position after applying constraints
    def get(self) -> tuple:
        return self._position
    
    def getActiveConstraints(self) -> list[Constraint]:
        return self._activeConstraints
    
    # whether the position is snapped to a constraint
    def snapped(self) -> bool:
        return self._snapped