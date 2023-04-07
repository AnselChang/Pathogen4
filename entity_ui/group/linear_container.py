from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity_ui.group.linear_group_container import LinearGroupContainer

from entity_base.entity import Entity
from entity_base.container_entity import Container
from typing import TypeVar, Generic

"""
A single option object for a RadioGroup
"""
T = TypeVar('T')
class LinearContainer(Container, Generic[T]):

    # id is used to distinguish between radio entities
    def __init__(self, group: LinearGroupContainer, id: str):
        super().__init__(parent = group)

        self.group: LinearGroupContainer | T = group
        self.id = id
        self.i = group.add(self)
        self.group.recomputePosition()

    def defineCenter(self) -> tuple:
        if self.group.isHorizontal:
            return self._px((self.i + 0.5) / self.group.N), self._py(0.5)
        else:
            return self._px(0.5), self._py((self.i + 0.5) / self.group.N)
        
    def defineWidth(self) -> float:
        if self.group.isHorizontal:
            return self._pwidth(1) / self.group.N
        else:
            return self._pwidth(1)
        
    def defineHeight(self) -> float:
        if self.group.isHorizontal:
            return self._pheight(1)
        else:
            return self._pheight(1) / self.group.N
        