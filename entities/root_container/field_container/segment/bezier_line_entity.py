from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.field_container.segment.bezier_node_entity import BezierNodeEntity

from entity_base.entity import Entity
import pygame

"""
Draw line between bezier control point and node
"""

class BezierLineEntity(Entity):

    def __init__(self, parent: BezierNodeEntity):
        super().__init__(parent)

        self.controlPoint = parent
        self.field = parent.field
        self.parent = parent

    def isTouching(self, mouse: tuple) -> float:
        return False
    
    def defineAfter(self) -> None:
        self.p1 = [self.CENTER_X, self.CENTER_Y]
        self.p2 = self.field.inchesToMouse(self.parent.getNeighborNode().position)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        if not self.controlPoint.segment.isBezierHovered():
            return
        
        pygame.draw.line(screen, self.controlPoint.getColor(), self.p1, self.p2)
