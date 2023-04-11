from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from common.draw_order import DrawOrder
from common.font_manager import DynamicFont, FontID

from entity_base.entity import Entity
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.hover_listener import HoverLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType
from entity_ui.dropdown.dropdown_icon_container import DropdownIconContainer
from utility.pygame_functions import drawLine, drawText, getText
if TYPE_CHECKING:
    from entity_ui.dropdown.dropdown_container import DropdownContainer

import pygame

class DropdownOptionEntity(Entity):

    # i is used for positioning. Active option is 0, after that it's 1, 2, ...
    # For active option, pass in dynamic text. Otherwise, pass in static text
    def __init__(self, dropdownContainer: DropdownContainer, i: int, font: DynamicFont,
                 colorSelectedHovered, colorSelected, colorHovered, colorOff, staticText: str = None,
                 dynamicText: Callable = None, visible = lambda: True, isLast = False):

        if dynamicText is None:
            self.getText = lambda staticText=staticText: staticText
        else:
            self.getText = dynamicText

        self.colorSelectedHovered = colorSelectedHovered
        self.colorSelected = colorSelected
        self.colorHovered = colorHovered
        self.colorOff = colorOff

        self.font = font
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
            

        
    def isVisible(self) -> bool:

        return super().isVisible() and self.visible()
    
    def defineBefore(self):
        surface = getText(self.font.get(), self.getText(), (0,0,0))
        self.textWidth = surface.get_width()
        self.textHeight = surface.get_height()

    def getTextWidth(self) -> float:
        return self.textWidth
    
    def getTextHeight(self) -> float:
        return self.textHeight

    def defineCenterX(self) -> float:
        return self._px(0.5)
    
    def defineTopY(self) -> float:
        return self._py(0) + self.i * self.dropdownContainer.optionHeight
    
    def defineWidth(self) -> float:
        return self._pwidth(1)
    
    def defineHeight(self) -> float:
        return self.dropdownContainer.optionHeight
    
    # Higher number is drawn in the front.
    # We want to draw the lowest y coordinate in the front
    def drawOrderTiebreaker(self) -> float:
        return -self.dropdownContainer.TOP_Y

    
    def drawOnSurface(self, surface):

        if not self.isVisible():
            return

        if self.isFirst:
            color = self.colorSelectedHovered if self.hover.isHovering else self.colorSelected
        else:
            color = self.colorHovered if self.hover.isHovering else self.colorOff

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
        alpha = int(round(self.getOpacity() * 255))
        pygame.draw.rect(surface, (*color, alpha), (x, y, self.WIDTH, self.HEIGHT+h),
                        border_top_left_radius = tl,
                        border_top_right_radius = tr,
                        border_bottom_left_radius = bl,
                        border_bottom_right_radius = br
                         )
        drawText(surface, self.font.get(), self.getText(), (0,0,0, alpha),
                 x = x + self._awidth(self.dropdownContainer.TEXT_LEFT_OFFSET),
                 y = y + self.HEIGHT/2,
                 alignX = 0,
                 alignY = 0.5,
                 opacity = self.getOpacity()
                 )


