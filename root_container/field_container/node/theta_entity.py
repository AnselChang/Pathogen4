from __future__ import annotations
import math
from typing import TYPE_CHECKING
from common.draw_order import DrawOrder
from common.reference_frame import Ref
from entity_base.listeners.drag_listener import DragLambda

from entity_base.listeners.select_listener import SelectLambda, SelectorType
from root_container.field_container.segment.segment_type import SegmentType
from utility.pygame_functions import shade
if TYPE_CHECKING:
    from root_container.field_container.node.path_node_entity import PathNodeEntity
    from root_container.field_container.segment.path_segment_entity import PathSegmentEntity

from entity_base.abstract_circle_entity import AbstractCircleEntity

"""
A PathNodeEntity has two ThetaEntities, for the start and end angles.
Only is visible when all three conditions are met
- the segment or node is selected
- when the segment of that side exists
- is not straight
Can snap to cardinal directions, the opposing ThetaEntity, as well as the angle
that would make the angle at the other side of the segment snap
"""

class ThetaEntity(AbstractCircleEntity):

    # segmentFunction is either getPrevious or getNext
    def __init__(self, pathNode: PathNodeEntity, isBeforeTheta: bool):

        self.DISTANCE_TO_NODE = 40

        self.node = pathNode
        self.isBeforeTheta = isBeforeTheta
        super().__init__(parent = pathNode,
            select = SelectLambda(self, "theta", type = SelectorType.SOLO),
            drag = DragLambda(self, FonStartDrag = self.onStartDrag, FonDrag = self.onDrag, FcanDrag = self.canDrag, FonStopDrag = self.onStopDrag),
            drawOrder = DrawOrder.THETA_NODE
        )

        self.COLOR = [255, 0, 255]
        self.COLOR_H = shade(self.COLOR, 0.9)

        self.recomputePosition()

    def getSegment(self) -> PathSegmentEntity:
        return self.node.getPrevious() if self.isBeforeTheta else self.node.getNext()

    def isVisible(self) -> bool:

        # If node itself isn't even visible, then this definitely shouldn't be
        if not self.node.isVisible():
            return False

        segment: PathSegmentEntity = self.getSegment()
        
        # If no segment, then no theta control
        if segment is None:
            return False
        
        # If segment is straight, then no theta control
        if segment.getSegmentType() == SegmentType.STRAIGHT:
            return False
        
        # If neither node nor segment is selected, then no theta control
        if not self.node.select.isSelected and not segment.select.isSelected:
            otherNode = segment.getOther(self.node)
            if otherNode is None or not otherNode.select.isSelected:
                otherSegment = self.node.getOther(segment)
                if otherSegment is None or not otherSegment.select.isSelected:
                    return False
        
        # If all conditions are met, then theta control is visible
        return True
    
    def defineCenter(self) -> tuple:
        segment: PathSegmentEntity = self.getSegment()

        # no segment exists, so just return the center of the path node.
        # it won't be visible anyway
        if segment is None:
            return self._px(0.5), self._py(0.5)

        r = self._awidth(self.DISTANCE_TO_NODE)

        # To avoid theta control overlapping with the node, we need to
        # shrink distsance as r approaches segmentDistance
        segmentDistance = segment.getLinearDistance(Ref.SCREEN)
        if r > segmentDistance / 2.5:
            r = segmentDistance / 2.5

        x, y = self._px(0.5), self._py(0.5)
        theta = segment.getThetaAtNode(self.node)

        # flip theta if this is the start theta for visual consistency
        if self.isBeforeTheta:
            theta += math.pi

        return x + r * math.cos(theta), y + r * math.sin(theta)
    
    def getColor(self, isHovered: bool = False) -> tuple:
        return self.COLOR_H if isHovered else self.COLOR

    def getRadius(self, isHovered: bool = False) -> float:
        return 6 if isHovered else 5

    def onStartDrag(self, mouse: tuple):
        pass

    def canDrag(self, mouse: tuple) -> bool:
        return True

    def onDrag(self, mouse: tuple):
        pass

    def onStopDrag(self):
        pass