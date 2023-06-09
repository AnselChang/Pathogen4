from common.reference_frame import PointRef

import entity_base.entity as entity

import pygame

"""
A entity that does not change and is always drawn
Not subclassable.
Pass a lambda function that draws the thing you want to the constructor.
EntityManager will automatically draw that thing every frame, respecting drawOrder
"""
class StaticEntity(entity.Entity):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, Fdraw = lambda: None, drawOrder: int = 0) -> None:
        super().__init__(parent = entity.ROOT_CONTAINER, drawOrder = drawOrder)
        self.Fdraw = Fdraw
        self.recomputeEntity()

    def isTouching(self, position: tuple) -> bool:
        return False

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        self.Fdraw()