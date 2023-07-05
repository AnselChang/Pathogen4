from __future__ import annotations
from typing import TYPE_CHECKING
from utility.line import Line

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
    
    def defineAfter(self) -> None:
        
        self.pixelLines: list[Line] = []
        for line in self.model.getConstraints():
            p1 = self.field.inchesToMouse(line.p1)
            p2 = self.field.inchesToMouse(line.p2)
            self.pixelLines.append(Line(point = p1, point2 = p2))
    
    # draw the constraint lines, if any
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        print("a")
        # only draw when mouse is hovering over node
        if not self.entity.hover.isHovering:
            return
        
        for line in self.pixelLines:
            print(line)
            drawDottedLine(screen, (30,255,30), line.p1, line.p2, length = 12, fill = 0.5, width = 2)