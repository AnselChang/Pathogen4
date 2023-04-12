from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref

from common.dimensions import Dimensions
from data_structures.observer import Observer

from entity_base.container_entity import Container
from common.draw_order import DrawOrder

from utility.math_functions import distance
import pygame

"""
The entity that holds all other entities. Set to dimensions size, and recomputes
children when dimensions change
"""

class RootContainer(Container, Observer):

    def __init__(self):
        super().__init__(None, drawOrder = DrawOrder.BACKGROUND)
        self.dimensions.subscribe(self, onNotify = self.recomputePosition)
        self.recomputePosition()

    def defineTopLeft(self) -> tuple:
        return 0, 0

    # dimensions set to the full screen size
    def defineWidth(self) -> float:
        return self.dimensions.SCREEN_WIDTH
    def defineHeight(self) -> float:
        return self.dimensions.SCREEN_HEIGHT

    def isVisible(self) -> bool:
        return True

    # Draw screen background
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        screen.fill((255,255,255))