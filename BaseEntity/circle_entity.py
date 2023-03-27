from BaseEntity.entity import Entity
from reference_frame import PointRef, Ref, VectorRef
from BaseEntity.EntityFunctions.drag_function import DragLambda
from BaseEntity.EntityFunctions.select_function import Select
from pygame_functions import drawTransparentCircle
import pygame

class CircleEntity(Entity):

    def __init__(self, position: PointRef, radius: int, color: tuple, id: str):
        super().__init__(
            drag = DragLambda(FdragOffset = lambda offset: self.move(offset)),
            select = Select(id)
            )
        self.position = position
        self.radius = radius
        self.color = color

    def move(self, offset: VectorRef):
        self.position += offset

    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        return self.distanceTo(position) <= self.radius
    
    def distanceTo(self, position: PointRef) -> float:
        return (position - self.position).magnitude(Ref.SCREEN)

    def getPosition(self) -> PointRef:
        return self.position

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        alpha = 200 if isHovered else 255
        drawTransparentCircle(screen, self.position.screenRef, self.radius, self.color, alpha)

        # draw border if active
        if isActive:
            pygame.draw.circle(screen, (0,0,0), self.position.screenRef, self.radius, 2)

    def toString(self) -> str:
        return "Circle"