from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Commands.command_block_entity import CommandBlockEntity

from BaseEntity.container_entity import ContainerEntity
from BaseEntity.EntityListeners.click_listener import ClickLambda
from BaseEntity.EntityListeners.hover_listener import HoverLambda

from UIEntities.Generic.image_entity import ImageEntity

from image_manager import ImageManager, ImageID
from dimensions import Dimensions

from draw_order import DrawOrder
from reference_frame import PointRef, Ref
from pygame_functions import drawSurface
from math_functions import distance
import pygame

# trash button for custom commands
class TrashEntity(ContainerEntity):

    def __init__(self, parentCommand: CommandBlockEntity, onDelete = lambda: None):
        
        super().__init__(parent = parentCommand)

        ImageEntity(self, imageID = ImageID.TRASH_OFF, imageIDHovered = ImageID.TRASH_ON, drawOrder = DrawOrder.WIDGET, onClick = onDelete)

    def defineCenter(self) -> tuple:
        return self._px(1) - self._ax(60), self._py(0.5)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self._pheight(0.8) # yes, this is height not width. square icon
    def defineHeight(self) -> float:
        return self._pheight(0.8)