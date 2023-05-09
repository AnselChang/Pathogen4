from __future__ import annotations
from typing import TYPE_CHECKING
from common.draw_order import DrawOrder
from common.reference_frame import *
from entity_base.entity import Entity

from utility.pygame_functions import drawDottedLine, shade
if TYPE_CHECKING:
    from root_container.field_container.node.path_node_entity import PathNodeEntity

import pygame

"""
Draws dotted lines for the start and stop angles of the node.
Draws both angles if node is selected.
Draws start angle if previous segment is selected.
Draws stop angle if next segment is selected.
"""
class NodeLine(Entity):

    # segmentFunction is either getPrevious or getNext
    def __init__(self, pathNode: PathNodeEntity):

        self.pathNode = pathNode

        super().__init__(parent = pathNode, drawOrder = DrawOrder.THETA_LINE)

    def isTouching(self, point: tuple) -> bool:
        return False

    # draw the two lines if conditions are met.
    # In addition, check if there is already a constraint. if so, don't draw
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):


        r = self.dimensions.FIELD_DIAGONAL
        pos = self.pathNode.getPositionRef()
        prevSegment = self.pathNode.getPrevious()
        
        if prevSegment is not None and (self.pathNode.select.isSelected or prevSegment.select.isSelected):
            theta1 = prevSegment.getEndTheta()

            if not self.pathNode.constraints.hasConstraint(pos.fieldRef, theta1):
                # only draw if there isn't already green constraints indicator
                extended = pos.screenRef[0] + r*math.cos(theta1), pos.screenRef[1] + r*math.sin(theta1)
                drawDottedLine(screen, (0,0,0), pos.screenRef, extended, length = 10, fill = 0.5, width = 1)