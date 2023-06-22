from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.image.image_state import ImageState
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from entity_base.container_entity import Container
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.hover_listener import HoverLambda

from entity_base.image.image_entity import ImageEntity

from common.image_manager import ImageManager, ImageID
from common.dimensions import Dimensions

from common.draw_order import DrawOrder
from common.reference_frame import PointRef, Ref
from utility.pygame_functions import drawSurface
from utility.math_functions import distance
import pygame

# trash button for custom commands
class TrashEntity(Container):

    def __init__(self, parentHeader, onDelete = lambda: None):
        
        super().__init__(parent = parentHeader)

        state = ImageState(0, ImageID.TRASH_OFF, imageOnHoveredID = ImageID.TRASH_ON)
        ImageEntity(self, state, onClick = lambda mouse: onDelete())

    def defineCenter(self) -> tuple:
        return self._px(1) - self._awidth(20), self._py(0.5)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self._pheight(0.6) # yes, this is height not width. square trash can
    def defineHeight(self) -> float:
        return self._pheight(0.6)