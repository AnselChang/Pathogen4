from entity_ui.scrollbar.abstract_scrollbar_container import AbstractScrollbarContainer

import pygame

"""
The specific scrollbar defined to be located at the right of the panel
"""
class CommandScrollbar(AbstractScrollbarContainer):

    def __init__(self, parent):

        self.UPPER_MARGIN = 35
        self.LOWER_MARGIN = 20
        self.RIGHT_MARGIN = 4
        
        super().__init__(parent)
        self.recomputePosition()

    def defineRightX(self) -> float:
        return self._px(1) - self._awidth(self.RIGHT_MARGIN)

    def defineTopY(self) -> float:
        return self._ay(self.UPPER_MARGIN)

    def defineWidth(self) -> float:
        return self._pwidth(0.05)
    
    def defineHeight(self) -> float:
        return self._pheight(1) - self._aheight(self.UPPER_MARGIN) - self._aheight(self.LOWER_MARGIN)