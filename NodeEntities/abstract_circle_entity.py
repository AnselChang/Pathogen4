from abc import abstractmethod
from BaseEntity.entity import Entity
from reference_frame import PointRef, Ref, VectorRef
from BaseEntity.EntityListeners.drag_listener import DragListener
from BaseEntity.EntityListeners.click_listener import ClickListener
from BaseEntity.EntityListeners.select_listener import SelectListener
import pygame

class AbstractCircleEntity(Entity):

    def __init__(self, radius: int, hoveredRadius: int):
        self.radius = radius
        self.radiusH = hoveredRadius

    @abstractmethod
    def getColor(self) -> tuple:
        pass

    # get the hitbox rect approximately spanning the circle
    def getHitbox(self) -> pygame.Rect:

        hitbox = pygame.Rect(0, 0, self.radius * 1.5, self.radius * 1.5)
        hitbox.center = self.CENTER_X, self.CENTER_Y
        return hitbox

    def isTouching(self, position: PointRef) -> bool:
        MARGIN = 4
        return self.distanceTo(position) <= self.radius + MARGIN

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        r = self.radiusH if isHovered else self.radius
        pos = self.CENTER_X, self.CENTER_Y

        # draw circle
        pygame.draw.circle(screen, self.getColor(), pos, r)

        # draw border if active
        if isActive:
            pygame.draw.circle(screen, (0,0,0), pos, r, 2)
