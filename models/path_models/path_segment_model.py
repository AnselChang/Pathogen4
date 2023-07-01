from __future__ import annotations
from typing import TYPE_CHECKING
from adapter.path_adapter import PathAdapter
from adapter.straight_adapter import StraightAdapter
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from models.path_models.segment_direction import SegmentDirection
from root_container.field_container.segment.straight_segment_entity import StraightSegmentEntity
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
        return 0
    
    def getEndTheta(self) -> float:
        return 0
    
    def getDirection(self) -> SegmentDirection:
        return self.direction
    
    def _generateUI(self, fieldEntity: FieldEntity) -> Entity:
        return StraightSegmentEntity(fieldEntity, self)
    
    def __str__(self) -> str:
        return f"PathSegmentModel"