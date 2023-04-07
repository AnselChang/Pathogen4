from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref

import entity_base.entity as entity
from common.draw_order import DrawOrder
from common.field_transform import FieldTransform

from utility.math_functions import distance
import pygame

"""
An entity for the panel on the right side. Holds other entities inside
"""

class FieldContainer(entity.Entity):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, fieldTransform: FieldTransform):
        super().__init__(parent = entity.ROOT_CONTAINER, drawOrder = DrawOrder.FIELD_BACKGROUND)
        self.fieldTransform = fieldTransform
        self.recomputePosition()

    def defineTopLeft(self) -> tuple:
        return 0, 0

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self.dimensions.SCREEN_HEIGHT
    def defineHeight(self) -> float:
        return self.dimensions.SCREEN_HEIGHT
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):
        self.fieldTransform.draw(screen)