from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer

from root_container.panel_container.command_scrolling.command_scrollbar import CommandScrollbar
from root_container.panel_container.command_scrolling.static_command_content_container import StaticCommandContentContainer
from entity_ui.scrollbar.scrolling_content_container import ScrollingContentContainer

from data_structures.observer import Observable

"""
Deals with creating the command scrollbar, the scrolling container storing the commands,
and facilitating interaction between the two
Subscribers recieve a notification when scroller moves
"""

class CommandScrollingHandler(Observable):
    
    def __init__(self, panel: BlockTabContentsContainer):

        # The scrollbar component and entity itself on the right of the panel
        self._commandScrollbar = CommandScrollbar(panel)

        # The unmoving container indicating the bounding box of all the commands.
        # Command block width is set to this
        self._staticContainer = StaticCommandContentContainer(panel)

        # Scrolling container starts off the same location as static container, but is y offset by scrollbar realtime
        self._scrollingContainer = ScrollingContentContainer(self._staticContainer, self._commandScrollbar)
        
    # Get the scrolling container, which should be set as parent of first CommandInserter
    # That way, the commands move with the scrolling container
    def getScrollingContainer(self) -> ScrollingContentContainer:
        return self._scrollingContainer
    
    # Call this to update the scrollbar with the new content height
    def setContentHeight(self, contentHeight: int):
        self._commandScrollbar.scrollbar.setContentHeight(contentHeight)

    def setManualScrollbarPosition(self, y: int):
        self._commandScrollbar.scrollbar.setManualOffset(y)