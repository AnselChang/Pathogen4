from __future__ import annotations
from typing import TYPE_CHECKING

from serialization.serializable import Serializable, SerializedState

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

class SerializedPathElementState(SerializedState):

    def _deserialize(self, pathModel: PathModel) -> PathElementModel:
        raise NotImplementedError()
    
    def makeDeserialized(self, pathModel: PathModel):
        self.DESERIALIZED = self._deserialize(pathModel)

    def makeAdapterDeserialized(self):
        raise NotImplementedError

    def deserialize(self) -> PathElementModel:
        return self.DESERIALIZED

T = TypeVar('T')
class PathElementModel(Serializable, LinkedListNode[T], Generic[T]):

    def _serialize(self) -> SerializedPathElementState:
        raise NotImplementedError()

    def makeSerialized(self):
        self.SERIALIZED = self._serialize()

    def makeAdapterSerialized(self):
        raise NotImplementedError()

    def serialize(self) -> SerializedPathElementState:
        return self.SERIALIZED

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

        if self.ui is not None:
            self.deleteUI()

        self.ui = self._generateUI(self.path.fieldEntity)

    def recomputeUI(self):
        self.ui.recomputeEntity()

    def deleteUI(self):
        self.ui.entities.removeEntity(self.ui)
        self.ui = None