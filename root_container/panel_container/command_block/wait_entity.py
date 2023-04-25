from __future__ import annotations
from enum import Enum
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

class WaitID(Enum):
    WAIT = 0
    NO_WAIT = 1

"""
Wait-for-complete entity for custom commands.
If set to WAIT, command will wait for completion before executing next command.
If set to NO_WAIT, command will run this command and the next concurrently through multithreading.
"""
class WaitEntity(Container):

    def __init__(self, parentHeader):
        
        super().__init__(parent = parentHeader)

        stateWait = ImageState(WaitID.WAIT, ImageID.WAIT, "Wait for completion: Enabled")
        stateNoWait = ImageState(WaitID.NO_WAIT, ImageID.NO_WAIT, "Wait for completion: Disabled")
        ImageEntity(self, [stateWait, stateNoWait], 
                    onClick = self.onClick,
                    getStateID = self.getStateID
                    )
        
        # default state is to wait for completion
        self.state: WaitID = WaitID.WAIT
        
    # toggle wait and no wait
    def onClick(self, mouse: tuple):
        if self.state == WaitID.WAIT:
            self.state = WaitID.NO_WAIT
        else:
            self.state = WaitID.WAIT

    def getStateID(self) -> int:
        return self.state

    def defineCenter(self) -> tuple:
        return self._px(1) - self._awidth(43), self._py(0.5)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self.defineHeight()
    def defineHeight(self) -> float:
        return self._pheight(0.55)