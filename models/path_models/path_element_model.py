"""
A PathNodeEntity or PathSegment entity
"""

from typing import Generic, TypeVar
from data_structures.linked_list import LinkedListNode
from entity_base.entity import Entity

T = TypeVar('T')
class PathElementModel(LinkedListNode[T], Generic[T]):
    def __init__(self):
        self.ui: Entity = None

    def _generateUI(self) -> Entity:
        raise NotImplementedError()

    def recomputeUI(self):
        if self.ui is None:
            self.ui = self._generateUI()
        
        self.ui.recomputeEntity()

    def deleteUI(self):
        self.ui.entities.removeEntity(self.ui)
        self.ui = None