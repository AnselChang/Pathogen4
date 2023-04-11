from __future__ import annotations
from typing import TYPE_CHECKING
from common.font_manager import FontID
from entity_base.container_entity import Container
from entity_base.listeners.hover_listener import HoverLambda
from root_container.panel_container.command_block.function.function_selector_icon import FunctionSelectorIcon
from utility.pygame_functions import shade
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from entity_base.entity import Entity
from entity_base.text_entity import TextEntity, TextAlign
from common.draw_order import DrawOrder
import pygame


# trash button for custom commands
class FunctionNameEntity(Entity):

    def __init__(self, parentHeader, parentCommand: CommandBlockEntity):
        
        self.parentCommand = parentCommand
        super().__init__(parent = parentHeader,
                         hover = HoverLambda(self),
                         drawOrder = DrawOrder.FUNCTION_NAME_BACKGROUND)
        
        self.dx = 19 # delta for text from left edge
        self.textEntity = None
        self.recomputePosition()

        self.CORNER_RADIUS = 5

        self.textEntity = TextEntity(self,
                   fontID = FontID.FONT_NORMAL,
                   fontSize = 18,
                   textFunction = lambda: parentCommand.getFunctionName() + "()",
                   align = TextAlign.LEFT,
                   drawOrder = DrawOrder.FUNCTION_NAME,
                   dx = self.dx
                   )
        
        FunctionSelectorIcon(self, parentCommand)

        self.recomputePosition()

    def defineLeftX(self) -> tuple:
        return self._px(0) + self._pheight(1)
    
    def defineCenterY(self) -> float:
        return self._py(0.5)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:

        if self.textEntity is None:
            return 0

        RIGHT_MARGIN = 5
        return self._awidth(self.dx + RIGHT_MARGIN) + self.textEntity.getTextWidth() # yes, this is height not width. square icon
    def defineHeight(self) -> float:
        return self._pheight(0.8)
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):

        s = 1 if isHovered else 1.1
        color = shade(self.parentCommand.getColor(), s)
        pygame.draw.rect(screen, color, self.RECT,
                         border_radius = self.CORNER_RADIUS
                         )