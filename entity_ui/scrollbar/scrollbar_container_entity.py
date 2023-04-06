from entity_base.entity import Entity
from entity_ui.scrollbar.scrollbar_entity import ScrollbarEntity

from global.draw_order import DrawOrder

from data_structures.observer import Observable
from utility.math_functions import isInsideBox2

import pygame

class ScrollbarContainerEntity(Entity):

    def __init__(self, panelEntity):

        super().__init__(parent = panelEntity, drawOrder = DrawOrder.SCROLLBAR_BACKGROUND)

        self.UPPER_MARGIN = 35
        self.LOWER_MARGIN = 3
        self.RIGHT_MARGIN = 2
        self.WIDTH = 10

        self.scrollbar = ScrollbarEntity()
        self.entities.addEntity(self.scrollbar, self)

        self.recomputePosition()

    def defineRightX(self) -> float:
        return self._px(1) - self._ax(self.RIGHT_MARGIN)

    def defineTopY(self) -> float:
        return self._ay(self.UPPER_MARGIN)

    def defineWidth(self) -> float:
        return self._awidth(self.WIDTH)
    
    def defineHeight(self) -> float:
        return self._pheight(1) - self._aheight(self.UPPER_MARGIN) - self._aheight(self.LOWER_MARGIN)