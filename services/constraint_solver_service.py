from __future__ import annotations
import math
from typing import TYPE_CHECKING

from models.path_models.path_segment_state.segment_type import SegmentType
from serialization.serializable import Serializable, SerializedState

if TYPE_CHECKING:
    from models.path_models.path_node_model import PathNodeModel
    from models.path_models.path_node_model import SerializedPathNodeState
    from models.path_models.path_segment_model import PathSegmentModel
    from entities.root_container.field_container.field_entity import FieldEntity

from utility.angle_functions import Direction, equalTheta, equalTheta180, headingDiff, headingDiff180
from utility.line import Line
from utility.math_functions import distancePointToLine, distanceTuples

class SerializedConstraintState(SerializedState):

    def __init__(self, line: Line, nodes: list[SerializedPathNodeState]):
        self.line = line
        self.nodes = nodes

class Constraint(Serializable):

    def serialize(self) -> SerializedConstraintState:
        sNodes = [node.serialize() for node in self.nodes]
        return SerializedConstraintState(self.line, sNodes)

    @staticmethod
    def deserialize(state: SerializedConstraintState) -> 'Constraint':
        nodes = [node.deserialize() for node in state.nodes]
        return Constraint(state.line, nodes)

    def __init__(self, line: Line, nodes: list[PathNodeModel]):
        self.line = line
        self.nodes = nodes

    # make a copy of constraint adding node to node list
    def makeWithNode(self, node: PathNodeModel) -> Constraint:
        nodes = self.nodes.copy()

        if node not in nodes:
            nodes.append(node)
        
        return Constraint(self.line, nodes)
    
    def __repr__(self) -> str:
        return f"Constraint: ({self.line.p1}, {self.line.p2}) {self.nodes}"

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
        self.addConstraint(Line(node.position, theta = Direction.WEST), [node])
        self.addConstraint(Line(node.position, theta = Direction.NORTH), [node])

    # add angular constraint for constraining angles 
    def addAngleConstraint(self, node: PathNodeModel, theta: float):
        self.addConstraint(Line(node.position, theta = theta), [node])

    # snap to a given segment and a node on that segment, snap to the line tangent to the node there
    def addSegmentConstraint(self, segment: PathSegmentModel, node: PathNodeModel):

        assert(segment.getPrevious() is node or segment.getNext() is node)

        if segment.getPrevious() is node:
            angle = segment.getStartTheta()
        else:
            angle = segment.getEndTheta()

        line = Line(point = node.position, theta = angle)

        # for straight segments, both, not one, nodes are collinear
        if segment.getType() == SegmentType.STRAIGHT:
            nodes = [segment.getPrevious(), segment.getNext()]
        else:
            nodes = [node]

        self.addConstraint(line, nodes)

    # snap to the line determined by the two given nodes
    def addLineFromTwoNodesConstraint(self, node1: PathNodeModel, node2: PathNodeModel):
        line = Line(point = node1.position, point2 = node2.position)
        self.addConstraint(line, [node1, node2])

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
    def constrainPosition(self, node: PathNodeModel, position: tuple) -> tuple:

        # constraint snapping is disabled when holding shift
        if self.field.isShiftHeld():
            self._snapped = False
            self._position = position
            self._activeConstraints = []
            return self._position

        THRESHOLD_PIXELS = 4 # how close the node must be to the line to snap (in pixels)

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

        # add node to each of active constraints
        self._activeConstraints = [constraint.makeWithNode(node) for constraint in self._activeConstraints]
        
        return self._position
    
    # run the constraints algorithm on a given theta
    # THIS ASSUMES THAT ALL CONSTRAINT LINES INTERSECT THE POSITION OF THE ANGLE TO BE CONSTRAINED
    def constrainAngle(self, thetaToBeConstrained: float) -> float:
        
        # constraint snapping is disabled when holding shift
        if self.field.isShiftHeld():
            return None

        # find closest theta
        closestTheta = None
        smallestThetaDiff = math.inf
        
        for constraint in self.constraints:
            possibleTheta = constraint.line.theta
            for possibleTheta180 in [possibleTheta, possibleTheta + math.pi]:
                diff = headingDiff(possibleTheta180, thetaToBeConstrained)
                if diff < smallestThetaDiff:
                    smallestThetaDiff = diff
                    closestTheta = possibleTheta180
        print()

        # if can snap to closest theta, do so
        MAXIMUM_SNAPPING_THETA = 0.1
        if equalTheta180(thetaToBeConstrained, closestTheta, tolerance = MAXIMUM_SNAPPING_THETA):
            return closestTheta
        else:
            return None # too far away to snap
    
    # get the position after applying constraints
    def get(self) -> tuple:
        return self._position
    
    def getActiveConstraints(self) -> list[Constraint]:
        return self._activeConstraints
    
    # whether the position is snapped to a constraint
    def snapped(self) -> bool:
        return self._snapped