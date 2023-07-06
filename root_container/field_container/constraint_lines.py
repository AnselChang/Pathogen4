from __future__ import annotations
import math
from typing import TYPE_CHECKING
from common.draw_order import DrawOrder
from utility.line import Line
from utility.math_functions import hypo

from utility.pygame_functions import drawDottedLine
from entity_base.entity import Entity
from root_container.field_container.node.i_path_node_entity import IPathNodeEntity

if TYPE_CHECKING:
    from root_container.field_container.field_entity import FieldEntity
    from root_container.field_container.node.path_node_entity import PathNodeEntity


"""
Draws all the constraint lines for the hovered node, or nothing if no node is hovered
"""
class ConstraintLinesEntity(Entity):

    def __init__(self, parent: FieldEntity):
        super().__init__(parent = parent, drawOrder = DrawOrder.FRONT)

        self.field = parent

    # get hovered PathNodeEntity, or None if none are hovered
    def getHoveredNode(self) -> PathNodeEntity | None:
        hovered = self.interactor.getHoveredEntity()
        if isinstance(hovered, IPathNodeEntity):
            return hovered
        return None

    # cannot interact with constraint lines
    def isTouching(self, mouse: tuple) -> float:
        return False
    
    def _point(self, startPoint, distance, theta):
        return startPoint[0] + distance * math.cos(theta), startPoint[1] + distance * math.sin(theta)
    
    def defineAfter(self) -> None:
        self.dist = hypo(self.field.WIDTH, self.field.HEIGHT)
        
    
    # draw the constraint lines, if any
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        # only draw when mouse is hovering over node
        hoveredNode = self.getHoveredNode()
        if hoveredNode is None:
            return
        
        for constraint in hoveredNode.model.getConstraints():
            point = self.field.inchesToMouse(constraint.line.p1)
            theta = constraint.line.theta

            p1 = self._point(point, self.dist, theta)
            p2 = self._point(point, self.dist, theta + math.pi)
        
            drawDottedLine(screen, (30,255,30), p1, p2, length = 12, fill = 0.5, width = 2)