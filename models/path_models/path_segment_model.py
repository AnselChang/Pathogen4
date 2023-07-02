from __future__ import annotations
import math
from typing import TYPE_CHECKING
from adapter.path_adapter import PathAdapter, PathAttributeID
from adapter.straight_adapter import StraightAdapter
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from models.path_models.segment_direction import SegmentDirection
from root_container.field_container.segment.straight_segment_entity import StraightSegmentEntity
from utility.format_functions import formatInches
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

        self.adapter = StraightAdapter([
            ImageState(SegmentDirection.FORWARD, ImageID.STRAIGHT_FORWARD),
            ImageState(SegmentDirection.REVERSE, ImageID.STRAIGHT_REVERSE),
        ])

        self.generateUI()


    """
    UPDATE methods that update values based on model state
    """

    # update thetas based on current node positions and segment direction
    def updateThetas(self):
        before = self.getBeforePos()
        after = self.getAfterPos()
        self.START_THETA = thetaFromPoints(before, after)
        self.END_THETA = thetaFromPoints(before, after)

        # if segment is reversed, flip thetas
        if self.getDirection() == SegmentDirection.REVERSE:
            self.START_THETA = (self.START_THETA + math.pi) % (2 * math.pi)
            self.END_THETA = (self.END_THETA + math.pi) % (2 * math.pi)

    """
    CALLBACK METHODS FOR WHEN THINGS NEED TO BE UPDATED
    """

    # called when the distance of the segment is changed
    def onDistanceChange(self):
        distance = distanceTuples(self.getBeforePos(), self.getAfterPos())
        self.adapter.set(PathAttributeID.DISTANCE, distance, formatInches(distance))
    
    # called when a node attached to segment is moved
    def onNodePositionChange(self, node: PathNodeModel):
        # assert that node is attached to segment
        assert(node == self.getPrevious() or node == self.getNext())

        # update segment start/end thetas
        self.updateThetas()
        self.getPrevious().onThetaChange()
        self.getNext().onThetaChange()

        # update segment distance
        self.onDistanceChange()

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
        return self.adapter
 
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
    
    """
    PRIVATE METHODS
    """
    
    def _generateUI(self, fieldEntity: FieldEntity) -> Entity:
        return StraightSegmentEntity(fieldEntity, self)
    
    def __str__(self) -> str:
        return f"PathSegmentModel"