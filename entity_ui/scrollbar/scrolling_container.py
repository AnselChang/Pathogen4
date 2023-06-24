"""
An entity that fits the rect of its parent, and contains a content
container which may be larger in height than itself. If this is the
case, a scrollbar will be scrollable on the right side.

For simplicity, we hardcode that only vertically scrolling is allowed,
at least for now.

Behind the scenes, a ScrollingContainer contains a
- MovingScrollingContainer, which is the container that actually moves vertically
    based on scrollbar, and is slightly smaller in width to make space for scrollbar
    - (Entity) for content, passed in through constructor
- ScrollbarContainer, which contains the scrollbar and draws background
    - ScrollbarEntity, which is draggable and within ScrollbarContainer

Thus, to use this feature for some content, create some container,
and pass in scrollingContainer.getContainer() as parent
"""

from entity_base.container_entity import Container
from entity_base.entity import Entity
from entity_ui.scrollbar.moving_scrolling_container import MovingScrollingContainer
from entity_ui.scrollbar.scrollbar_container import ScrollbarContainer


class ScrollingContainer(Container):
    
    def __init__(self, parent: Entity):

        super().__init__(parent)

        self.SCROLLBAR_WIDTH = 13 # in relative pixels
        self.yOffset = 0 # in relative pixels, 0 means from the top

        self.movingContainer = MovingScrollingContainer(self)
        self.scrollbarContainer = ScrollbarContainer(self)
        self.content = None

    # use return value as parent for content entity
    def getContainer(self) -> Entity:
        return self.movingContainer
    
    # called one time on initialiation
    def _onSetContent(self, content: Entity):
        print("on set content")
        self.content = content
        # when content changes height, need to recompute things
        self.content.thisUpdatesParent = True

    def getContentHeight(self) -> float:
        return self.content.defineHeight()
    
    def setYOffset(self, newYOffset):
        self.yOffset = newYOffset
        print("new y offset", self.yOffset)
        self.recomputeEntity()