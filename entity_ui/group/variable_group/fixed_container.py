from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Generic, TypeVar
from data_structures.linked_list import LinkedListNode

from entity_base.entity import Entity
if TYPE_CHECKING:
    from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer

from entity_base.container_entity import Container
from abc import ABC, abstractmethod

"""
A container with fixed dimensions positioned relatively according to VGC
"""
class FixedContainer(Container, ABC):

    def __init__(self, parent: VariableGroupContainer, isHorizontal: bool, getSize: lambda: int):
        self.isHorizontal = isHorizontal
        self._POSITION_FROM_VGC = 0
        self.getSize = getSize

        super().__init__(parent = parent)

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
            return self.getSize()
        else:
            return self._pwidth(1)
        
    def defineHeight(self) -> float:
        if not self.isHorizontal:
            return self.getSize()
        else:
            return self._pheight(1)
        
    # draw the upper/leftmost entities in the front
    # Sort by leftmost/topmost position, unless overriden by child
    def drawOrderTiebreaker(self) -> float:
        return -self._POSITION_FROM_VGC
