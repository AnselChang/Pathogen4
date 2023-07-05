from __future__ import annotations
import math
from typing import TYPE_CHECKING
from utility.line import Line
from utility.math_functions import hypo

from utility.pygame_functions import drawDottedLine
from entity_base.entity import Entity

if TYPE_CHECKING:
    from root_container.field_container.node.path_node_entity import PathNodeEntity

"""
Draws all the constraint lines for a node
"""
class ConstraintLines(Entity):

    def __init__(self, parent: PathNodeEntity):
        super().__init__(parent = parent, drawOrderRecursive = False)

        self.entity = parent
        self.model = parent.model
        self.field = parent.field

    # cannot interact with constraint lines
    def isTouching(self, mouse: tuple) -> float:
        return False
    
    def _point(self, startPoint, distance, theta):
        return startPoint[0] + distance * math.cos(theta), startPoint[1] + distance * math.sin(theta)
    
    def defineAfter(self) -> None:

        dist = hypo(self.field.WIDTH, self.field.HEIGHT)
        
        self.pixelLines: list[Line] = []
        for constraint in self.model.getConstraints():
            point = self.field.inchesToMouse(constraint.line.p1)
            theta = constraint.line.theta

            p1 = self._point(point, dist, theta)
            p2 = self._point(point, dist, theta + math.pi)

            self.pixelLines.append(Line(point = p1, point2 = p2))
    
    # draw the constraint lines, if any
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        # only draw when mouse is hovering over node
        if not self.entity.hover.isHovering:
            return
        
        for line in self.pixelLines:
            drawDottedLine(screen, (30,255,30), line.p1, line.p2, length = 12, fill = 0.5, width = 2)