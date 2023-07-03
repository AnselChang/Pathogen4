from __future__ import annotations
import math
from typing import TYPE_CHECKING
from adapter.path_adapter import PathAdapter, PathAttributeID
from adapter.straight_adapter import StraightAdapter
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from models.path_models.path_segment_state.abstract_segment_state import AbstractSegmentState
from models.path_models.path_segment_state.arc_segment_state import ArcSegmentState
from models.path_models.path_segment_state.segment_type import SegmentType
from models.path_models.path_segment_state.straight_segment_state import StraightSegmentState
from models.path_models.segment_direction import SegmentDirection
from root_container.field_container.segment.arc_segment_entity import ArcSegmentEntity
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

        self.states: dict[SegmentType, AbstractSegmentState] = {
            SegmentType.STRAIGHT: StraightSegmentState(self),
            SegmentType.ARC: ArcSegmentState(self),
        }

        self.currentStateType = SegmentType.STRAIGHT

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
        self.ui.interactor.selected.activeMenu = self.ui.interactor.selected.menuManager.createMenuForEntity(self.ui)

    def toggleDirection(self):
        if self.direction == SegmentDirection.FORWARD:
            self.direction = SegmentDirection.REVERSE
        else:
            self.direction = SegmentDirection.FORWARD

        self.updateThetas()
        self.getPrevious().onThetaChange()
        self.getNext().onThetaChange()

    """
    GETTER METHODS THAT READ FROM MODEL. DO NOT MODIFY MODEL OR SEND NOTIFICATIONS
    """

    def getState(self) -> AbstractSegmentState:
        return self.states[self.currentStateType]

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
    
    """
    PRIVATE METHODS
    """
    
    def _generateUI(self, fieldEntity: FieldEntity) -> Entity:
        if self.getType() == SegmentType.STRAIGHT:
            return StraightSegmentEntity(fieldEntity, self)
        if self.getType() == SegmentType.ARC:
            return ArcSegmentEntity(fieldEntity, self)
        
    
    def __str__(self) -> str:
        return f"PathSegmentModel"