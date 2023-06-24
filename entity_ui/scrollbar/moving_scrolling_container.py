from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.entity import Entity
if TYPE_CHECKING:
    from entity_ui.scrollbar.scrolling_container import ScrollingContainer

from entity_base.container_entity import Container

"""
Defined inside a ScrollingContainer.
Width is equal to ScrollingContainer minus scrollbar.
Y is defined as the top Y of ScrollingContainer plus some y offset.
"""

class MovingScrollingContainer(Container):
    
    def __init__(self, parent: ScrollingContainer):
        super().__init__(parent, thisUpdatesParent = True)
        self.scrollingContainer = parent

    # called when child is constructed with this as parent
    def onAddChild(self, child: Entity):
        self.scrollingContainer._onSetContent(child)

    # Y is defined as the top Y of ScrollingContainer plus some y offset.
    def defineWidth(self) -> float:
        return self._pwidth(1) - self._awidth(self.scrollingContainer.SCROLLBAR_WIDTH)
    
    # Height does not matter
    def defineHeight(self) -> float:
        return 0
    
    # align with left of ScrollingContainer
    def defineLeftX(self) -> float:
        return self._px(0)
    
    # align with top of ScrollingContainer
    def defineTopY(self) -> float:
        return self._py(0) - self.scrollingContainer.yOffset