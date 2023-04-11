from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from common.draw_order import DrawOrder
from common.font_manager import DynamicFont, FontID
from common.image_manager import ImageID

if TYPE_CHECKING:
    from root_container.panel_container.command_block.function.function_group_selector import FunctionGroupSelector


from entity_base.entity import Entity
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.hover_listener import HoverLambda
from entity_ui.group.linear_container import LinearContainer
from utility.pygame_functions import drawLine, drawText, shade
import pygame

"""
Rect is defined by parent LinearContainer, which is part of a DynamicGroupContainer
"""

class FunctionOptionEntity(Entity):

    # i is used for positioning. Active option is 0, after that it's 1, 2, ...
    # For active option, pass in dynamic text. Otherwise, pass in static text
    def __init__(self, parent: LinearContainer, text: str, font: DynamicFont, color: tuple,
                 isFirst: bool, isLast: bool, onClick: Callable[[], str],
                 leftTextOffset: int, cornerRadius: int
                 ):

        super().__init__(parent = parent,
            click = ClickLambda(self, FonLeftClick = lambda mouse: onClick(text)),
            hover = HoverLambda(self)
            )

        # dictionary for hovered / not hovered color
        self.color = {
            True: shade(color, 0.8),
            False: color
        }
        self.text = text
        self.font = font
        self.isFirst = isFirst
        self.isLast = isLast
        self.leftTextOffset = leftTextOffset
        self.cornerRadius = cornerRadius

        self.recomputePosition()
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        tl, tr, bl, br = 0, 0, 0, 0
        r = self.cornerRadius
        if self.isFirst:
            tl = r
            tr = r
        if self.isLast:
            bl = r
            br = r

        h = 0 if self.isLast else 1 # prevent any gaps between options
        rect = [self.LEFT_X, self.TOP_Y, self.WIDTH, self.HEIGHT+h]
        pygame.draw.rect(screen, self.color[isHovered], rect,
                        border_top_left_radius = tl,
                        border_top_right_radius = tr,
                        border_bottom_left_radius = bl,
                        border_bottom_right_radius = br
                        )
        drawText(screen, self.font.get(), self.text, (0,0,0),
                 x = self.LEFT_X + self._awidth(self.leftTextOffset),
                 y = self.CENTER_Y,
                 alignX = 0,
                 alignY = 0.5
                 )


