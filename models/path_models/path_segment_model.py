from __future__ import annotations
import math
from typing import TYPE_CHECKING
from adapter.path_adapter import PathAdapter, PathAttributeID
from adapter.straight_adapter import StraightAdapter
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from models.path_models.path_segment_state.abstract_segment_state import AbstractSegmentState, SerializedSegmentStateState
from models.path_models.path_segment_state.arc_segment_state import ArcSegmentState
from models.path_models.path_segment_state.bezier_segment_state import BezierSegmentState
from models.path_models.path_segment_state.segment_type import SegmentType
from models.path_models.path_segment_state.straight_segment_state import StraightSegmentState
from models.path_models.segment_direction import SegmentDirection
from entities.root_container.field_container.segment.arc_segment_entity import ArcSegmentEntity
from entities.root_container.field_container.segment.bezier_segment_entity import BezierSegmentEntity
from entities.root_container.field_container.segment.straight_segment_entity import StraightSegmentEntity
from services.constraint_solver_service import ConstraintSolver
from utility.format_functions import formatDegrees, formatInches
from utility.math_functions import distanceTuples, thetaFromPoints
if TYPE_CHECKING:
    from entities.root_container.field_container.field_entity import FieldEntity
    from models.path_models.path_node_model import PathNodeModel
    from models.path_models.path_model import PathModel
    from entity_base.entity import Entity


from models.path_models.path_element_model import PathElementModel, SerializedPathElementState

class SerializedPathSegmentState(SerializedPathElementState):

    def __init__(self, direction: SegmentDirection, states: dict[SegmentType, SerializedSegmentStateState], current: SegmentType):
        self.direction = direction
        self.states = states
        self.current = current

    def _deserialize(self, pathModel: PathModel) -> 'PathNodeModel':
        segment = PathSegmentModel(pathModel)
        segment.direction = self.direction

        segment.states = {}
        for key, value in self.states.items():
            segment.states[key] = value.deserialize(segment)

        segment.currentStateType = self.current
        return segment
    
    def makeAdapterDeserialized(self):
        for state in self.states.values():
            state.adapter.makeDeserialized()

class PathSegmentModel(PathElementModel):

    def makeAdapterSerialized(self):
        for state in self.states.values():
            state.adapter.makeSerialized()

    def _serialize(self) -> SerializedPathSegmentState:
        sStates: dict[SegmentType, SerializedSegmentStateState] = {}
        for key, value in self.states.items():
            sStates[key] = value.serialize()

        return SerializedPathSegmentState(self.direction, sStates, self.currentStateType)
    
    def __init__(self, pathModel: PathModel):
        super().__init__(pathModel)

        self.direction = SegmentDirection.FORWARD

        self.states: dict[SegmentType, AbstractSegmentState] = {
            SegmentType.STRAIGHT: StraightSegmentState(self),
            SegmentType.ARC: ArcSegmentState(self),
            SegmentType.BEZIER: BezierSegmentState(self)
        }

        self.currentStateType = SegmentType.STRAIGHT
        self.bConstraints = None # before theta constraint solver
        self.aConstraints = None # after theta constraint solver

        self.generateUI()


    """
    UPDATE methods that update values based on model state
    """

    # update thetas based on segment states and segment direction
    def updateThetas(self):

        # need to recompute state thetas first
        self.getState().onUpdate()

        self.START_THETA = self.getState().getStartTheta()
        self.END_THETA = self.getState().getEndTheta()

        # if segment is reversed, flip thetas
        if self.getDirection() == SegmentDirection.REVERSE:
            self.START_THETA = (self.START_THETA + math.pi) % (2 * math.pi)
            self.END_THETA = (self.END_THETA + math.pi) % (2 * math.pi)

        self.getAdapter().set(PathAttributeID.THETA1, self.START_THETA, formatDegrees(self.START_THETA))
        self.getAdapter().set(PathAttributeID.THETA2, self.END_THETA, formatDegrees(self.END_THETA))

    # called when the distance of the segment is changed
    def updateDistance(self):
        self.DISTANCE = distanceTuples(self.getPrevious().getPosition(), self.getNext().getPosition())
        # if segment is reversed, negate distance
        if self.getDirection() == SegmentDirection.REVERSE:
            self.DISTANCE *= -1

        self.getAdapter().set(PathAttributeID.DISTANCE, self.DISTANCE, formatInches(self.DISTANCE))
    
    # Update adapter for endpoint position
    def updateEndpointPosition(self, node: PathNodeModel):

        # new endpoint position
        pos = node.getPosition()

        # update the correct endpoint
        if self.getPrevious() == node:
            x, y = PathAttributeID.X1, PathAttributeID.Y1
        else:
            x, y = PathAttributeID.X2, PathAttributeID.Y2

        # set adapter
        self.getAdapter().set(x, pos[0], formatInches(pos[0]))
        self.getAdapter().set(y, pos[1], formatInches(pos[1]))

    """
    CALLBACK METHODS FOR WHEN THINGS NEED TO BE UPDATED
    """

    def onInit(self):
        self.updateThetas()
        self.updateDistance()
        self.updateEndpointPosition(self.getPrevious())
        self.updateEndpointPosition(self.getNext())

        self.getPrevious().onThetaChange()
        self.getNext().onThetaChange()

    def onInitSegmentOnly(self):
        self.updateThetas()
        self.updateDistance()
        self.updateEndpointPosition(self.getPrevious())
        self.updateEndpointPosition(self.getNext())

    # called when a node attached to segment is moved
    def onNodePositionChange(self, node: PathNodeModel = None):
        # assert that node is attached to segment
        assert(node is None or node == self.getPrevious() or node == self.getNext())

        # update segment start/end thetas
        self.updateThetas()
        self.getPrevious().onThetaChange()
        self.getNext().onThetaChange()

        # update segment distance
        self.updateDistance()

        
        if node is None:
            self.updateEndpointPosition(self.getPrevious())
            self.updateEndpointPosition(self.getNext())
            self.getPrevious().onThetaChange()
            self.getNext().onThetaChange()
        else:
            # update endpoint that changed
            self.updateEndpointPosition(node)
            # update the other endpoint's angle
            self.getOther(node).onThetaChange()

        # redraw segment ui. No need to update segment model as
        # segment endpoint positions are just refs to node models
        self.recomputeUI()

    """
    SETTER METHODS THAT MODIFY MODEL AND THEN SEND NOTIF TO UPDATE UI
    """

    def setState(self, type: SegmentType):

        assert(type in self.states)
        self.currentStateType = type

        # callback for state change
        self.getState().onSwitchToState()

        self.onInit()

        # regenerate ui with new state
        self.generateUI()
        self.recomputeUI()

        command = self.path.getCommandFromPath(self)
        command.setNewAdapter(self.getAdapter())
        command.rebuild()
        command.ui.recomputeEntity()

        # absolutely atrocious code to dig through interactor shit to
        # sustain menu across changing segment entity
        self.ui.interactor.removeAllEntities()
        self.ui.interactor.addEntity(self.ui)

    def toggleDirection(self):
        if self.direction == SegmentDirection.FORWARD:
            self.direction = SegmentDirection.REVERSE
        else:
            self.direction = SegmentDirection.FORWARD
        self.getState()._updateIcon()

        self.updateThetas()
        self.getPrevious().onThetaChange()
        self.getNext().onThetaChange()

    """
    GETTER METHODS THAT READ FROM MODEL. DO NOT MODIFY MODEL OR SEND NOTIFICATIONS
    """

    def getState(self) -> AbstractSegmentState:
        return self.states[self.currentStateType]
    
    def getStraightState(self) -> StraightSegmentState:
        return self.states[SegmentType.STRAIGHT]
    
    def getArcState(self) -> ArcSegmentState:
        return self.states[SegmentType.ARC]
    
    def getBezierState(self) -> BezierSegmentState:
        return self.states[SegmentType.BEZIER]

    def getAdapter(self) -> PathAdapter:
        return self.getState().getAdapter()
 
    def getPrevious(self) -> PathNodeModel:
        return super().getPrevious()

    def getNext(self) -> PathNodeModel:
        return super().getNext()
    
    def getBeforePos(self) -> tuple:
        return self.getPrevious().getPosition()
    
    def getAfterPos(self) -> tuple:
        return self.getNext().getPosition()
    
    def getStartTheta(self) -> float:
        return self.START_THETA
    
    def getEndTheta(self) -> float:
        return self.END_THETA
    
    def getDirection(self) -> SegmentDirection:
        return self.direction
    
    def getType(self) -> SegmentType:
        return self.getState().getType()
    
    def getCenterInches(self) -> tuple:
        return self.getState()._defineCenterInches()
    
    def getOther(self, node: PathNodeModel) -> PathNodeModel:
        if node == self.getPrevious():
            return self.getNext()
        elif node == self.getNext():
            return self.getPrevious()
        else:
            raise Exception("Node not attached to segment")
    
    # initialize constraint solver for snapping to before node with angle (arc/bezier)
    def initBeforeThetaConstraints(self):
        self.bConstraints = ConstraintSolver(self.field)

        prevNode = self.getPrevious()

        # snap to cardinal directions for itself
        self.bConstraints.addCardinalConstraints(prevNode)

        # if segment before prevNode exists, snap to segment end angle
        prevSegment = prevNode.getPrevious()
        if prevSegment is not None:
            prevAngle = prevSegment.getEndTheta()
            self.bConstraints.addAngleConstraint(prevNode, prevAngle)

    # initialize constraint solver for snapping to after node with angle (arc/bezier)
    def initAfterThetaConstraints(self):
        self.aConstraints = ConstraintSolver(self.field)

        prevNode = self.getPrevious()

        # snap to cardinal directions for itself
        self.aConstraints.addCardinalConstraints(prevNode)

        # if segment before prevNode exists, snap to segment end angle
        prevSegment = prevNode.getPrevious()
        if prevSegment is not None:
            prevAngle = prevSegment.getEndTheta()
            self.aConstraints.addAngleConstraint(prevNode, prevAngle)


    # given a hypothetical start theta, return the "snapped" version if close enough
    # return None if no snapping
    def getConstrainedStartTheta(self, startTheta: float) -> float | None:
        snappedTheta = self.bConstraints.constrainAngle(startTheta)

        if snappedTheta is None:
            # nothing to snap
            return None
        else:
            # can snap
            return snappedTheta
        
    # given a hypothetical start theta, return the "snapped" version if close enough
    # return None if no snapping
    def getConstrainedEndTheta(self, endTheta: float) -> float | None:
        snappedTheta = self.aConstraints.constrainAngle( endTheta)

        if snappedTheta is None:
            # nothing to snap
            return None
        else:
            # can snap
            return snappedTheta
        
    
    """
    PRIVATE METHODS
    """
    
    def _generateUI(self, fieldEntity: FieldEntity) -> Entity:
        if self.getType() == SegmentType.STRAIGHT:
            return StraightSegmentEntity(fieldEntity, self)
        elif self.getType() == SegmentType.ARC:
            return ArcSegmentEntity(fieldEntity, self)
        elif self.getType() == SegmentType.BEZIER:
            return BezierSegmentEntity(fieldEntity, self)
        else:
            raise Exception("Invalid segment type")
    
    def __str__(self) -> str:
        return f"PathSegmentModel"