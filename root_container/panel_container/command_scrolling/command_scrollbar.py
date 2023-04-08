from entity_ui.scrollbar.abstract_scrollbar_container import AbstractScrollbarContainer

import pygame

"""
The specific scrollbar defined to be located at the right of the panel
"""
class CommandScrollbar(AbstractScrollbarContainer):

    def __init__(self, parent):

        self.RIGHT_MARGIN = 4
        
        super().__init__(parent)
        self.recomputePosition()

    def defineRightX(self) -> float:
        return self._px(1) - self._awidth(self.RIGHT_MARGIN)

    def defineTopY(self) -> float:
        return self._py(0.02)
    
    def defineBottomY(self) -> float:
        return self._py(0.98)

    def defineWidth(self) -> float:
        return self._pwidth(0.05)
    