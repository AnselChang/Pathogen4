from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Generic, TypeVar
from data_structures.linked_list import LinkedListNode

from entity_base.entity import Entity
if TYPE_CHECKING:
    from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer

from entity_base.container_entity import Container
from abc import ABC, abstractmethod

"""
A container that has a fixed width/height, postioned relatively based on the parent
VariableGroupContainer. The VariableGroupContainer should read this object's 
width/height to determine this object's absolute position.

To use AbstractVariableContainer, create a AVC as part of a VGC, and set
AVC as parent of your entity. Make sure to set AVC's child as yourself.
Then, call AVC.onChangeInContainerSize() whenever the size of your entity changes.
This will cause the VGC to recompute the position
"""
T = TypeVar('T')
class VariableContainer(Container, LinkedListNode['VariableContainer'], ABC, Generic[T]):

    def __init__(self, parent: VariableGroupContainer, isHorizontal: bool):
        self.isHorizontal = isHorizontal
        self.group: VariableGroupContainer = parent
        self.child: T | Entity = None
        self._POSITION_FROM_VGC = 0

        super().__init__(parent = parent, thisUpdatesParent = True)
        LinkedListNode.__init__(self)

    def setChild(self, child: T):
        self.child: T | Entity = child

    def changeParent(self, newParent: Entity):
        super().changeParent(newParent)
        self.group = newParent
    
    # set by VariableGroupContainer. Size refers to x if isHorizontal, else y
    def setPosition(self, position: int):
        self._POSITION_FROM_VGC = position

    def defineLeftX(self) -> float:
        if self.isHorizontal:
            return self._POSITION_FROM_VGC
        else:
            return self._px(0)

    def defineTopY(self) -> float:
        if not self.isHorizontal:
            return self._POSITION_FROM_VGC
        else:
            return self._py(0)
        
    def defineWidth(self) -> float:
        if self.isHorizontal:
            if self.child is None:
                return 0
            else:
                return self.child.defineWidth()
        else:
            return self._pwidth(1)
        
    def defineHeight(self) -> float:
        if not self.isHorizontal:
            if self.child is None:
                return 0
            else:
                return self.child.defineHeight()
        else:
            return self._pheight(1)
        
    # draw the upper/leftmost entities in the front
    # Sort by leftmost/topmost position, unless overriden by child
    def drawOrderTiebreaker(self) -> float:

        childTiebreaker = self.child.drawOrderTiebreaker()
        if childTiebreaker is not None:
            return childTiebreaker

        return -self._POSITION_FROM_VGC
    
    # override to add more information when logging entity
    def logMoreInfo(self) -> str:
        return self.child.__repr__()