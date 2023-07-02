from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from root_container.field_container.field_entity import FieldEntity
    from entity_base.entity import Entity
    from models.path_models.path_model import PathModel
    from models.command_models.command_model import CommandModel

from typing import Generic, TypeVar
from data_structures.linked_list import LinkedListNode

"""
A PathNodeEntity or PathSegment entity
"""

T = TypeVar('T')
class PathElementModel(LinkedListNode[T], Generic[T]):
    def __init__(self, pathModel: PathModel):

        super().__init__()
        
        self.path = pathModel
        self.field = pathModel.fieldEntity
        self.ui: Entity = None

    def getCommand(self) -> CommandModel:
        return self.path.getCommandFromPath(self)

    def _generateUI(self, fieldEntity: FieldEntity) -> Entity:
        raise NotImplementedError()
    
    def generateUI(self):
        assert(self.path.fieldEntity is not None)
        self.ui = self._generateUI(self.path.fieldEntity)

    def recomputeUI(self):
        self.ui.recomputeEntity()

    def deleteUI(self):
        self.ui.entities.removeEntity(self.ui)
        self.ui = None