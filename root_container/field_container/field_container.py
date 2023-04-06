from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref

from entity_base.entity import Entity
from common.draw_order import DrawOrder

from utility.math_functions import distance
import pygame

"""
An entity for the panel on the right side. Holds other entities inside
"""

class FieldContainer(Entity):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, color) -> None:
        super().__init__(drawOrder = DrawOrder.PANEL_BACKGROUND)
        self.color = color

    # override
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pygame.draw.rect(screen, self.color, *self.RECT)

    # THESE METHODS ARE IMPLEMENTED BY SUBCLASS TO SPECIFY RELATIVE POSITION
    def recomputePosition(self):
        self.WIDTH = self.defineWidth()
        self.HEIGHT = self.defineHeight()
        self.CENTER_X, self.CENTER_Y = self.defineCenter()
        self.LEFT_X, self.TOP_Y = self.defineTopLeft()

        # Now that this entity position is recomputed, make sure children recompute too
        self.notify()

    def defineTopLeft(self) -> tuple:
        return self.dimensions.FIELD_WIDTH, 0

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self.dimensions.PANEL_WIDTH
    def defineHeight(self) -> float:
        return self.dimensions.SCREEN_HEIGHT