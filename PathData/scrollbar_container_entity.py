from BaseEntity.entity import Entity
from PathData.scrollbar_entity import ScrollbarEntity

from draw_order import DrawOrder

from Observers.observer import Observable
from math_functions import isInsideBox2

import pygame

class ScrollbarContainerEntity(Entity):

    def __init__(self):

        super().__init__(drawOrder = DrawOrder.SCROLLBAR_BACKGROUND)

        self.UPPER_MARGIN = 35
        self.LOWER_MARGIN = 3
        self.RIGHT_MARGIN = 2

        self.entities.addEntity(ScrollbarEntity(), self)

        self.recomputePosition()

    def defineTopLeft(self) -> tuple:
        x = self.dimensions.SCREEN_HEIGHT - self._ax(self.WIDTH + self.RIGHT_MARGIN)
        return x, self._ay(self.y)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        WIDTH = 10
        return self._awidth(WIDTH)
    
    def defineHeight(self) -> float:
        return self.dimensions.SCREEN_HEIGHT - self.UPPER_MARGIN - self.LOWER_MARGIN