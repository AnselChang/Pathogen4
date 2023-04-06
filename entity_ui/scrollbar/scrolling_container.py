from entity_base.container_entity import Container
from entity_ui.scrollbar.scrollbar_entity import ScrollbarEntity
from entity_ui.scrollbar.scrollbar_container_entity import ScrollbarContainerEntity

class ScrollingContainer(Container):

    def __init__(self, parentContainer, scrollbarContainer: ScrollbarContainerEntity):
        
        super().__init__(parent = parentContainer)

        self.scrollbar = scrollbarContainer.scrollbar
        self.scrollbar.subscribe(onNotify = self.recomputePosition)

    def defineTopLeft(self) -> tuple:
        return self._px(0), self._py(0) + self.scrollbar.getScrollOffset()

    def defineWidth(self) -> float:
        return self._pwidth(1)
    
    def defineHeight(self) -> float:
        return self._pheight(1)