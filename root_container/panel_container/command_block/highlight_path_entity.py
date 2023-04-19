from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.image.image_state import ImageState
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from entity_base.container_entity import Container

from entity_base.image.image_entity import ImageEntity

from common.image_manager import ImageID

from common.draw_order import DrawOrder
from utility.pygame_functions import drawSurface
from utility.math_functions import distance
import pygame

"""
When clicked, jump to the corresponding node or segment.
Does not exist for custom commands, which has a trash button instead
"""
class HighlightPathEntity(Container):

    def __init__(self, parentHeader, onHighlight = lambda: None):
        
        super().__init__(parent = parentHeader)
        state = ImageState(0, ImageID.REVEAL_COMMAND)
        ImageEntity(self, state, drawOrder = DrawOrder.WIDGET, onClick = onHighlight)

    def defineCenter(self) -> tuple:
        return self._px(1) - self._awidth(20), self._py(0.5)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self._pheight(0.6) # yes, this is height not width. square trash can
    def defineHeight(self) -> float:
        return self._pheight(0.6)