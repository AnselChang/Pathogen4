from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.entity import Entity
if TYPE_CHECKING:
    from root_container.panel_container.panel_container import PanelContainer

from common.draw_order import DrawOrder
from entity_base.entity import Entity
from utility.pygame_functions import getGradientSurface
import pygame

"""
Gradient below tabs and above commands
"""

class AbstractGradientSeparator(Entity):

    def __init__(self, parentPanel: PanelContainer, invert: bool, percentFullyOpaque: float = 1):

        self.parentPanel = parentPanel
        self.invert = invert
        self.percent = percentFullyOpaque

        super().__init__(parentPanel, drawOrder = DrawOrder.GRADIENT_SEPARATOR)
        self.recomputePosition()

    def isVisible(self) -> bool:
        return True
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        c1 = (*self.parentPanel.color, 255)
        c2 = (*self.parentPanel.color, 0)

        if not self.invert:
            yGradient = self.TOP_Y + self.HEIGHT * self.percent
            yOpaque = self.TOP_Y
        else:
            yGradient = self.TOP_Y
            yOpaque = self.TOP_Y + self.HEIGHT * self.percent
        screen.blit(getGradientSurface(self.WIDTH, self.HEIGHT * (1 - self.percent), c1, c2, invert = self.invert), (self.LEFT_X, yGradient)),
        pygame.draw.rect(screen, c1, (self.LEFT_X, yOpaque, self.WIDTH, self.HEIGHT * self.percent))

class TabsCommandsSeparator(AbstractGradientSeparator):

    def __init__(self, parent: PanelContainer):
        super().__init__(parent, False, percentFullyOpaque = 0.75)
        self.recomputePosition()

    def defineTopLeft(self) -> tuple:
        return self._px(0), self._py(0)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self._pwidth(1)
    def defineHeight(self) -> float:
        return self._pheight(0.08)