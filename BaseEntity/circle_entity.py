from BaseEntity.entity import Entity
from reference_frame import PointRef, Ref
import pygame


class CircleEntity(Entity):

    def __init__(self, position: PointRef, radius: int, color: tuple):
        super().__init__()
        self.position = position
        self.radius = radius
        self.color = color

    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        return (position - self.position).magnitude(Ref.SCREEN) <= self.radius

    def getPosition(self) -> PointRef:
        return self.position

    def draw(self, screen: pygame.Surface, isActive: bool) -> bool:
        r = self.radius + (20 if isActive else 0)
        pygame.draw.circle(screen, self.color, self.position.screenRef, r, width=0)

    def toString(self) -> str:
        return "Circle"