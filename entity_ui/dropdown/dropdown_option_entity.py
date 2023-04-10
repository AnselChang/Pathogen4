from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from common.draw_order import DrawOrder
from common.font_manager import FontID

from entity_base.entity import Entity
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.hover_listener import HoverLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType
from entity_ui.dropdown.dropdown_icon_container import DropdownIconContainer
from utility.pygame_functions import drawLine, drawText
if TYPE_CHECKING:
    from entity_ui.dropdown.dropdown_container import DropdownContainer

import pygame

class DropdownOptionEntity(Entity):

    # i is used for positioning. Active option is 0, after that it's 1, 2, ...
    # For active option, pass in dynamic text. Otherwise, pass in static text
    def __init__(self, dropdownContainer: DropdownContainer, i: int, staticText: str = None,
                 dynamicText: Callable = None, visible = lambda: True, isLast = False):

        if dynamicText is None:
            self.getText = lambda staticText=staticText: staticText
        else:
            self.getText = dynamicText

        t = self.getText

        super().__init__(parent = dropdownContainer,
            click = ClickLambda(self, FonLeftClick = lambda mouse, i=i, t=t: dropdownContainer.onOptionClick(i, t())),
            hover = HoverLambda(self)
            )
        self.dropdownContainer = dropdownContainer
        self.i = i
        self.visible = visible
        
        self.isFirst = (i == 0)
        self.isLast = isLast

        self.recomputePosition()

        if i == 0:
            DropdownIconContainer(self, dropdownContainer)

        
    def isVisible(self) -> bool:
        return super().isVisible() and self.visible()

    def defineCenterX(self) -> float:
        return self._px(0.5)
    
    def defineTopY(self) -> float:
        return self._py(0) + self._aheight(self.i * self.dropdownContainer.getOptionHeight())
    
    def defineWidth(self) -> float:
        return self._pwidth(1)
    
    def defineHeight(self) -> float:
        return self._aheight(self.dropdownContainer.getOptionHeight())
    
    def drawOnSurface(self, surface, font):
        
        if self.hover.isHovering:
            color = [176, 200, 250] if self.isFirst else [52, 132, 240]
        else:
            color = [196, 219, 250]

        x = self.LEFT_X - self._px(0)
        y = self.TOP_Y - self._py(0)

        #drawLine(surface, (0,0,0), x, y, x + 200, y, 1)

        tl, tr, bl, br = 0, 0, 0, 0
        r = self.dropdownContainer.CORNER_RADIUS
        if self.isFirst:
            tl = r
            tr = r
        if self.isLast or (self.isFirst and self.dropdownContainer.isFullyCollapsed()):
            bl = r
            br = r

        h = 0 if self.isLast else 1 # prevent any gaps between options
        pygame.draw.rect(surface, color, (x, y, self.WIDTH, self.HEIGHT+h),
                        border_top_left_radius = tl,
                        border_top_right_radius = tr,
                        border_bottom_left_radius = bl,
                        border_bottom_right_radius = br
                         )
        drawText(surface, font, self.getText(), (0,0,0),
                 x = x + self._awidth(self.dropdownContainer.TEXT_LEFT_OFFSET),
                 y = y + self.HEIGHT/2,
                 alignX = 0,
                 alignY = 0.5
                 )


