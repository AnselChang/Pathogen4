from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from dimensions import Dimensions

from BaseEntity.entity import Entity
from draw_order import DrawOrder

from math_functions import distance
import pygame

"""
The entity that holds all other entities. Set to dimensions size, and recomputes
children when dimensions change
"""

class RootEntity(Entity):

    def __init__(self):
        super().__init__(None, drawOrder = DrawOrder.BACKGROUND)
        self.dimensions.subscribe(onNotify = self.recomputePosition)

    def defineTopLeft(self) -> tuple:
        return 0, 0

    # dimensions set to the full screen size
    def defineWidth(self) -> float:
        return self.dimensions.SCREEN_WIDTH
    def defineHeight(self) -> float:
        return self.dimensions.SCREEN_HEIGHT

    def isVisible(self) -> bool:
        return False

    # Draw screen background
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        screen.fill((255,255,255))