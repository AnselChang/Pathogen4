from entity_ui.scrollbar.abstract_scrollbar_container import AbstractScrollbarContainer

import pygame

"""
The specific scrollbar defined to be located at the right of the panel
"""
class CommandScrollbar(AbstractScrollbarContainer):

    def __init__(self, parent):

        self.UPPER_MARGIN = 35
        self.LOWER_MARGIN = 3
        self.RIGHT_MARGIN = 2
        self.WIDTH = 10
        
        super().__init__(parent)   

    def defineRightX(self) -> float:
        return self._px(1) - self._ax(self.RIGHT_MARGIN)

    def defineTopY(self) -> float:
        return self._ay(self.UPPER_MARGIN)

    def defineWidth(self) -> float:
        return self._awidth(self.WIDTH)
    
    def defineHeight(self) -> float:
        return self._pheight(1) - self._aheight(self.UPPER_MARGIN) - self._aheight(self.LOWER_MARGIN)