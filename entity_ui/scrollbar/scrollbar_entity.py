from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.entity import Entity
from entity_base.listeners.hover_listener import HoverLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType
from entity_base.listeners.drag_listener import DragLambda

from data_structures.observer import Observable
from utility.math_functions import isInsideBox2, clamp

if TYPE_CHECKING:
    from entity_ui.scrollbar.scrolling_container import ScrollingContainer

import pygame

class ScrollbarEntity(Entity, Observable):

    def __init__(self, parent, scrollbarContainer: ScrollingContainer):

        super().__init__(
            parent = parent,
            select = SelectLambda(self, "scroll", type = SelectorType.SOLO),
            drag = DragLambda(self,
                              FonStartDrag = self.onStartDrag,
                              FonDrag = self.onDrag),
            hover = HoverLambda(self)
        )

        self.scrollbarContainer = scrollbarContainer

    def defineTopY(self) -> tuple:
        return self._py(0) + self._aheight(self.scrollbarContainer.yOffset)
    
    def defineCenterX(self) -> float:
        return self._px(0.5)

    def defineWidth(self) -> float:
        return self._mwidth(2) # margin of 2 pixels
    
    def defineHeight(self) -> float:

        contentHeight = self.scrollbarContainer.getContentHeight()

        if contentHeight == 0:
            ratio = 1
        else:
            ratio = min(1, self._pheight(1) / contentHeight)
        return self._pheight(1) * ratio

    def onStartDrag(self, mouse: tuple):
        self.mouseStartY = mouse[1]
        self.startOffsetY = self.scrollbarContainer.yOffset

    def getMaxOffset(self, contentHeight):
        return max(0, contentHeight - self.scrollbarContainer.HEIGHT)

    def onDrag(self, mouse: tuple):
        newYOffset = self.startOffsetY + (mouse[1] - self.mouseStartY)

        newYOffset = max(0, newYOffset)

        contentHeight = self.scrollbarContainer.getContentHeight()
        newYOffset = min(self.getMaxOffset(contentHeight), newYOffset)

        self.scrollbarContainer.setYOffset(newYOffset)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        color = [140,140,140] if self.hover.isHovering else [160,160,160]
        pygame.draw.rect(screen, color, self.RECT)