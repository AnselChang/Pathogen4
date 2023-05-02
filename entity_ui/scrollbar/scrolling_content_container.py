from common.draw_order import DrawOrder
from data_structures.observer import Observer
from entity_base.container_entity import Container
from entity_ui.scrollbar.scrollbar_entity import ScrollbarEntity
from root_container.panel_container.command_scrolling.command_scrollbar import AbstractScrollbarContainer

class ScrollingContentContainer(Container, Observer):

    def __init__(self, parentContainer, scrollbarContainer: AbstractScrollbarContainer, drawOrder = DrawOrder.FRONT):
        
        super().__init__(parent = parentContainer, drawOrder = drawOrder)

        self.scrollbar = scrollbarContainer.scrollbar
        self.scrollbar.subscribe(self, onNotify = self.recomputePosition)

    def defineTopLeft(self) -> tuple:
        return self._px(0), self._py(0) + self.scrollbar.getScrollOffset()

    def defineWidth(self) -> float:
        return self._pwidth(1)
    
    def defineHeight(self) -> float:
        return self._pheight(1)
    
    def setContentHeight(self, contentHeight: int):
        self.scrollbar.setContentHeight(contentHeight)