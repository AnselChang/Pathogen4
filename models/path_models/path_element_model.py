from __future__ import annotations
from typing import TYPE_CHECKING

from models.path_models.path_model import PathModel
if TYPE_CHECKING:
    from root_container.field_container.field_entity import FieldEntity
    from entity_base.entity import Entity

from typing import Generic, TypeVar
from data_structures.linked_list import LinkedListNode

"""
A PathNodeEntity or PathSegment entity
"""

T = TypeVar('T')
class PathElementModel(LinkedListNode[T], Generic[T]):
    def __init__(self, pathModel: PathModel):
        
        self.path = pathModel
        self.ui: Entity = None

    def _generateUI(self, fieldEntity: FieldEntity) -> Entity:
        raise NotImplementedError()

    def recomputeUI(self):

        assert(self.path.fieldEntity is not None)

        if self.ui is None:
            self.ui = self._generateUI(self.path.fieldEntity)
        
        self.ui.recomputeEntity()

    def deleteUI(self):
        self.ui.entities.removeEntity(self.ui)
        self.ui = None