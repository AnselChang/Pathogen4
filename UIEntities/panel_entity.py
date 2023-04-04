from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from dimensions import Dimensions

from BaseEntity.entity import Entity
from draw_order import DrawOrder

from math_functions import distance
import pygame

"""
An entity for the panel on the right side. Holds other entities inside
"""

class PanelEntity(Entity):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, dimensions: Dimensions, color) -> None:
        super().__init__(DrawOrder = DrawOrder.PANEL_BACKGROUND)
        self.dimensions = dimensions
        self.color = color

    # override
    def isTouching(self, position: tuple) -> bool:
        return False

    # override
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        x, y = self.dimensions.FIELD_WIDTH, 0
        width, height = self.dimensions.PANEL_WIDTH, self.dimensions.SCREEN_HEIGHT
        pygame.draw.rect(screen, self.color, (x, y, width, height))

    # draw rect specified by x, y, width, height. For testing only probably
    def drawRect(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0,0,0), [self.LEFT_X, self.TOP_Y, self.WIDTH, self.HEIGHT])

    
    # THESE METHODS ARE IMPLEMENTED BY SUBCLASS TO SPECIFY RELATIVE POSITION
    def recomputePosition(self):
        self.WIDTH = self.getWidth()
        self.HEIGHT = self.getHeight()
        self.CENTER_X, self.CENTER_Y = self.getCenter()
        self.LEFT_X, self.TOP_Y = self.getTopLeft()

        # Now that this entity position is recomputed, make sure children recompute too
        self.notify()

    # impl EITHER getCenter OR getTopLeft
    def getCenter(self) -> tuple:
        lx, ty = self.getTopLeft()
        return lx + self.WIDTH / 2, ty + self.HEIGHT / 2

    def getTopLeft(self) -> tuple:
        cx, cy = self.getCenter()
        return cx - self.WIDTH / 2, cy - self.HEIGHT / 2


    # must impl both of these if want to contain other entity
    def getWidth(self) -> float:
        return 0
    def getHeight(self) -> float:
        return 0

    # THESE ARE UTILITY METHODS THAT CAN BE USED TO SPECIFY RELATIVE POSITIONS ABOVE

    # get relative x as a percent of parent horizontal span
    def _px(self, px):
        if self._parent is None:
            raise Exception("No parent")
        return self._parent.LEFT_X + self._parent.WIDTH / 2
    
    # get relative x as a percent of parent horizontal span
    def _py(self, py):
        if self._parent is None:
            raise Exception("No parent")
        return self._parent.TOP_Y + self._parent.HEIGHT / 2
    
    # get relative width as a percent of parent horizontal span
    def _pwidth(self, pwidth):
        if self._parent is None:
            raise Exception("No parent")
        return self._parent.WIDTH * pwidth
    
    # get relative height as a percent of parent vertical span
    def _pheight(self, pheight):
        if self._parent is None:
            raise Exception("No parent")
        return self._parent.HEIGHT * pheight
    
    # Get width given a margin (on both sides) from parent horizontal span
    def _mwidth(self, margin):
        if self._parent is None:
            raise Exception("No parent")
        return self._parent.WIDTH - margin * 2

    # Get height given a margin (on both sides) from parent vertical span
    def _mheight(self, margin):
        if self._parent is None:
            raise Exception("No parent")
        return self._parent.HEIGHT - margin * 2