from __future__ import annotations
from typing import TYPE_CHECKING

from models.path_models.segment_direction import SegmentDirection
if TYPE_CHECKING:
    from models.path_models.path_model import PathModel
    from models.path_models.path_segment_model import PathSegmentModel

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
        self.lastDragPositionValid = False

        self.generateUI()

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
    
    def _generateUI(self, fieldEntity: FieldEntity) -> Entity:
        return PathNodeEntity(fieldEntity, self)
    
    # gets the start theta, adjusted for segment direction.
    # returns None if there is no previous node
    def getStartTheta(self):
        if self.getPrevious() is None:
            if self.getNext() is None:
                return None
            else:
                return self.getStopTheta()
        
        theta = self.getPrevious().getEndTheta()
        if self.getPrevious().getDirection() == SegmentDirection.REVERSE:
            theta = (theta + math.pi) % (math.pi*2)
        return theta

    # gets the stop theta, adjusted for segment direction.
    # returns None if there is no next node
    def getEndTheta(self):
        if self.getNext() is None:
            if self.getPrevious() is None:
                return None
            else:
                return self.getStartTheta()
        
        theta = self.getNext().getStartTheta()
        if self.getNext().getDirection() == SegmentDirection.REVERSE:
            theta = (theta + math.pi) % (math.pi*2)
        return theta
    
    def __str__(self) -> str:
        return f"PathNodeModel at ({self.position[0]:2f}, {self.position[1]:2f})"