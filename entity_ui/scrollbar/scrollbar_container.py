from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.entity import Entity
from entity_ui.scrollbar.scrollbar_entity import ScrollbarEntity
if TYPE_CHECKING:
    from entity_ui.scrollbar.scrolling_container import ScrollingContainer

from entity_base.container_entity import Container

"""
Defined to be on the right side of the ScrollingContainer.
Contains a ScrollbarEntity
"""

class ScrollbarContainer(Container):

    def __init__(self, parent: ScrollingContainer):
        super().__init__(parent)
        self.scrollingContainer = parent

        self.scrollbarEntity = ScrollbarEntity(self, parent)
    
    def defineWidth(self) -> float:
        return self._awidth(self.scrollingContainer.SCROLLBAR_WIDTH)
    
    def defineHeight(self) -> float:
        return self._pheight(1)
    
    # align to the right side
    def defineRightX(self) -> float:
        return self._px(1)
    
    # align to the top side
    def defineTopY(self) -> float:
        return self._py(0)