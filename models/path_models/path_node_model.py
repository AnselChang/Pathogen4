from __future__ import annotations
from typing import TYPE_CHECKING
from adapter.path_adapter import PathAttributeID

from models.path_models.segment_direction import SegmentDirection
from services.constraint_solver_service import Constraint, ConstraintSolver
from utility.angle_functions import deltaInHeading, equalTheta
from utility.format_functions import formatDegrees
if TYPE_CHECKING:
    from models.path_models.path_model import PathModel
    from models.path_models.path_segment_model import PathSegmentModel
    from utility.line import Line

from enum import Enum
from adapter.turn_adapter import TurnAdapter
from common.image_manager import ImageID
from entity_base.entity import Entity
from entity_base.image.image_state import ImageState
from models.path_models.path_element_model import PathElementModel
from root_container.field_container.field_entity import FieldEntity
from root_container.field_container.node.path_node_entity import PathNodeEntity
from serialization.serializable import SerializedState
import math

class SerializedPathNodeModel(SerializedState):
    def __init__(self):
        pass

class TurnDirection(Enum):
    RIGHT = 0
    LEFT = 1

class PathNodeModel(PathElementModel):
        
    def __init__(self, pathModel: PathModel, initialPosition: tuple, temporary = False):

        super().__init__(pathModel)

        self.position: tuple = initialPosition
        self.adapter = TurnAdapter([
            ImageState(TurnDirection.RIGHT, ImageID.TURN_RIGHT),
            ImageState(TurnDirection.LEFT, ImageID.TURN_LEFT)
        ])

        # A bit like a "hover" node. If user doesn't successfully place it,
        # it will be deleted. Visually it is semi-transparent to indicate this.
        self.temporary = temporary

        self.TURN_ENABLED = None

        self.generateUI()

    """
    UPDATE methods that update values based on model state
    """

    # Called during onStartDrag for a path node. Generates a list of constraint lines
    # which will be used to constrain the path node's position during dragging.
    def initConstraints(self):

        self.constraintSolver = ConstraintSolver(self.field)

        # if previous/next node exists, snap to cardinal directions for it
        if self.getPrevious() is not None:
            prevNode = self.getPrevious().getPrevious()
            self.constraintSolver.addCardinalConstraints(prevNode)

            # if prev prev node exists, snap to cardinal directions for it too
            if prevNode.getPrevious() is not None:
                self.constraintSolver.addCardinalConstraints(prevNode.getPrevious().getPrevious())

        if self.getNext() is not None:
            nextNode = self.getNext().getNext()
            self.constraintSolver.addCardinalConstraints(nextNode)

            # if next next node exists, snap to cardinal directions for it too
            if nextNode.getNext() is not None:
                self.constraintSolver.addCardinalConstraints(nextNode.getNext().getNext())

        # snap to previous segment
        if self.getPrevious() is not None:
            node = self.getPrevious().getPrevious()
            segment = node.getPrevious()
            if segment is not None:
                self.constraintSolver.addSegmentConstraint(segment, node)

        # snap to next segment
        if self.getNext() is not None:
            node = self.getNext().getNext()
            segment = node.getNext()
            if segment is not None:
                self.constraintSolver.addSegmentConstraint(segment, node)

        # snap to line defined by previous and next nodes
        if self.getPrevious() is not None and self.getNext() is not None:
            prevNode = self.getPrevious().getPrevious()
            nextNode = self.getNext().getNext()
            self.constraintSolver.addLineFromTwoNodesConstraint(prevNode, nextNode)

        

    """
    CALLBACK METHODS FOR WHEN THINGS NEED TO BE UPDATED
    """

    def onInit(self):
        self.onThetaChange()

    # called when the start or end theta of this node has changed
    def onThetaChange(self):

        theta1 = self.getStartTheta()
        theta2 = self.getEndTheta()

        oldTurnEnabled = self.TURN_ENABLED
        self.TURN_ENABLED = not equalTheta(theta1, theta2, 0.01)
        self.adapter.setTurnEnabled(self.TURN_ENABLED)

        # set adapter theta
        self.adapter.set(PathAttributeID.THETA1, theta1, formatDegrees(theta1, 1))
        self.adapter.set(PathAttributeID.THETA2, theta2, formatDegrees(theta2, 1))
        
        # set adapter icon
        direction = deltaInHeading(theta1, theta2)
        self.adapter.setIconStateID(TurnDirection.LEFT if direction >= 0 else TurnDirection.RIGHT)

        if oldTurnEnabled != self.TURN_ENABLED:
            self.recomputeUI()

    def onPositionChange(self):
        # update segments attached to node, if any
        if self.getPrevious() is not None:
            self.getPrevious().onNodePositionChange(self)
        if self.getNext() is not None:
            self.getNext().onNodePositionChange(self)

        # recompute node ui
        self.recomputeUI()
    
    """
    SETTER METHODS THAT MODIFY MODEL AND THEN SEND NOTIF TO UPDATE UI
    """
    # Set the position of the node, which will update neighbor segments and recompute node
    def setPosition(self, position: tuple):
        self.position = position
        self.onPositionChange()

    # sets the position of the node, but applies constraints first
    def setAndConstrainPosition(self, position: tuple):

        # first remove all existing constraints on current node
        self.path.constraints.removeAllConstraintsWithNode(self)

        constrainedPosition = self.constraintSolver.constrainPosition(self, position)

        # add any snapped constraints to global constraints model
        for constraint in self.constraintSolver.getActiveConstraints():
            self.path.constraints.addConstraint(constraint)

        self.setPosition(constrainedPosition)

    def makePermanent(self):
        self.temporary = False
    """
    GETTER METHODS THAT READ FROM MODEL. DO NOT MODIFY MODEL OR SEND NOTIFICATIONS
    """

    def getAdapter(self) -> TurnAdapter:
        return self.adapter
    
    def getPrevious(self) -> PathSegmentModel:
        return super().getPrevious()

    def getNext(self) -> PathSegmentModel:
        return super().getNext()
    
    def getPosition(self) -> tuple:
        return self.position

    def isTemporary(self) -> bool:
        return self.temporary
    
    def isFirstNode(self) -> bool:
        return self.getPrevious() is None
    
    def isLastNode(self) -> bool:
        return self.getNext() is None
    
    def isTurnEnabled(self) -> bool:
        return self.TURN_ENABLED
    
    # get all the constraint lines to be displayed when node is hovered
    def getConstraints(self) -> list[Constraint]:
        return self.path.constraints.getConstraintsWithNode(self)
    
    # gets the theta when robot approaches node before turning
    def getStartTheta(self):
        if self.getPrevious() is None:
            if self.getNext() is None:
                return 0
            else:
                return self.getEndTheta()
        else:
            return self.getPrevious().getEndTheta()

    # gets the theta when robot leaves node after turning
    def getEndTheta(self):
        if self.getNext() is None:
            if self.getPrevious() is None:
                return 0
            else:
                return self.getStartTheta()
        else:
            return self.getNext().getStartTheta()
    
    def _generateUI(self, fieldEntity: FieldEntity) -> Entity:
        return PathNodeEntity(fieldEntity, self)
    
    def __str__(self) -> str:
        return f"PathNodeModel at ({self.position[0]:2f}, {self.position[1]:2f})"