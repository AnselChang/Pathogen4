from __future__ import annotations
from typing import TYPE_CHECKING

from serialization.serializable import Serializable, SerializedState
from services.constraint_solver_service import SerializedConstraintState

if TYPE_CHECKING:
    from services.constraint_solver_service import Constraint
    from models.path_models.path_node_model import PathNodeModel
    from utility.line import Line

"""
Stores all the active constraints that currently exist on the path

Each constraint is stored as the line and the list of nodes on that line

Dragging a node to snap should add a constraint here, and likewise
dragging it away should remove the constraint

Main purpose is for displaying constraint lines when hovering over relevant nodes

Fully serializable
"""

class SerializedConstraintsState(SerializedState):
    def __init__(self, sConstraints: list[SerializedConstraintState]):
        self.sConstraints = sConstraints

class ConstraintModel(Serializable):

    def serialize(self) -> SerializedConstraintsState:
        sConstraints = [constraint.serialize() for constraint in self.constraints]
        return SerializedConstraintsState(sConstraints)

    @staticmethod
    def deserialize(state: SerializedConstraintsState) -> 'ConstraintModel':
        constraints = [Constraint.deserialize(sConstraint) for sConstraint in state.sConstraints]
        constraintModel = ConstraintModel()
        constraintModel.constraints = constraints
        return constraintModel

    def __init__(self):
        self.constraints: list[Constraint] = []

    # add a singular constraint for when a node has been snapped
    def addConstraint(self, constraint: Constraint):
        self.constraints.append(constraint)

    # useful when node has been moved and all constraints for node must be reset again (and re-added if it snaps again)
    def removeAllConstraintsWithNode(self, node: PathNodeModel):
        self.constraints = [constraint for constraint in self.constraints if node not in constraint.nodes]

    # get lines for all constraints that contain the given node, useful for display when hovering over node
    def getConstraintsWithNode(self, node: PathNodeModel) -> list[Constraint]:
        return [constraint for constraint in self.constraints if node in constraint.nodes]