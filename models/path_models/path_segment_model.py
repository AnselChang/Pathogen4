from __future__ import annotations
import math
from typing import TYPE_CHECKING
from adapter.path_adapter import PathAdapter, PathAttributeID
from adapter.straight_adapter import StraightAdapter
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from models.path_models.path_segment_state.abstract_segment_state import AbstractSegmentState
from models.path_models.path_segment_state.straight_segment_state import StraightSegmentState
from models.path_models.segment_direction import SegmentDirection
from root_container.field_container.segment.straight_segment_entity import StraightSegmentEntity
from utility.format_functions import formatDegrees, formatInches
from utility.math_functions import distanceTuples, thetaFromPoints
if TYPE_CHECKING:
    from root_container.field_container.field_entity import FieldEntity
    from models.path_models.path_node_model import PathNodeModel
    from models.path_models.path_model import PathModel
    from entity_base.entity import Entity


from models.path_models.path_element_model import PathElementModel


class PathSegmentModel(PathElementModel):
    
    def __init__(self, pathModel: PathModel):
        super().__init__(pathModel)

        self.direction = SegmentDirection.FORWARD

        self.states: list[AbstractSegmentState] = [
            StraightSegmentState(self),
        ]

        self.currentState = self.states[0]

        self.generateUI()


    """
    UPDATE methods that update values based on model state
    """

    # update thetas based on segment states and segment direction
    def updateThetas(self):

        # need to recompute state thetas first
        self.currentState.onUpdate()

        self.START_THETA = self.currentState.getStartTheta()
        self.END_THETA = self.currentState.getEndTheta()

        # if segment is reversed, flip thetas
        if self.getDirection() == SegmentDirection.REVERSE:
            self.START_THETA = (self.START_THETA + math.pi) % (2 * math.pi)
            self.END_THETA = (self.END_THETA + math.pi) % (2 * math.pi)

        self.getAdapter().set(PathAttributeID.THETA1, self.START_THETA, formatDegrees(self.START_THETA))
        self.getAdapter().set(PathAttributeID.THETA2, self.END_THETA, formatDegrees(self.END_THETA))

    # called when the distance of the segment is changed
    def updateDistance(self):
        distance = self.currentState.getDistance()

        # if segment is reversed, negate distance
        if self.getDirection() == SegmentDirection.REVERSE:
            distance *= -1

        self.getAdapter().set(PathAttributeID.DISTANCE, distance, formatInches(distance))
    
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

    # called when a node attached to segment is moved
    def onNodePositionChange(self, node: PathNodeModel):
        # assert that node is attached to segment
        assert(node == self.getPrevious() or node == self.getNext())

        print("onNodePositionChange")

        # update segment start/end thetas
        self.updateThetas()
        self.getPrevious().onThetaChange()
        self.getNext().onThetaChange()

        # update segment distance
        self.updateDistance()

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

    """
    GETTER METHODS THAT READ FROM MODEL. DO NOT MODIFY MODEL OR SEND NOTIFICATIONS
    """

    def getAdapter(self) -> PathAdapter:
        return self.currentState.getAdapter()
 
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
    
    def getOther(self, node: PathNodeModel) -> PathNodeModel:
        if node == self.getPrevious():
            return self.getNext()
        elif node == self.getNext():
            return self.getPrevious()
        else:
            raise Exception("Node not attached to segment")
    
    """
    PRIVATE METHODS
    """
    
    def _generateUI(self, fieldEntity: FieldEntity) -> Entity:
        return StraightSegmentEntity(fieldEntity, self)
    
    def __str__(self) -> str:
        return f"PathSegmentModel"