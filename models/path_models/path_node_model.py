from __future__ import annotations
from typing import TYPE_CHECKING
from adapter.turn_adapter import TurnAdapter
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState
from models.path_models.path_element_model import PathElementModel
from root_container.field_container.node.path_node_entity import TurnDirection
from serialization.serializable import SerializedState
if TYPE_CHECKING:
    from models.path_models.path_model import PathModel

from data_structures.linked_list import LinkedListNode

class SerializedPathNodeModel(SerializedState):
    def __init__(self):
        pass

class PathNodeModel(PathElementModel):
        
    def __init__(self, pathModel: PathModel, initialPosition: tuple, temporary = False):

        super().__init__()

        self.path = pathModel
        self.position: tuple = initialPosition
        self.adapter = TurnAdapter([
            ImageState(TurnDirection.RIGHT, ImageID.TURN_RIGHT),
            ImageState(TurnDirection.LEFT, ImageID.TURN_LEFT)
        ])

        # A bit like a "hover" node. If user doesn't successfully place it,
        # it will be deleted. Visually it is semi-transparent to indicate this.
        self.temporary = temporary
        self.lastDragPositionValid = False

        self.dragging = True
        SNAPPING_POWER = 5 # in pixels
        self.constraints = Constraints(fieldContainer, SNAPPING_POWER)

    def getAdapter(self) -> TurnAdapter:
        return self.adapter