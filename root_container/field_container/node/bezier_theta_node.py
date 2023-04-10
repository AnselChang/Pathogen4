from __future__ import annotations
import math
from typing import TYPE_CHECKING, Callable
from common.draw_order import DrawOrder
from common.reference_frame import PointRef, Ref, VectorRef
from entity_base.listeners.drag_listener import DragLambda

from entity_base.listeners.select_listener import SelectLambda, SelectorType
from root_container.field_container.segment.segment_type import SegmentType
from utility.pygame_functions import shade
if TYPE_CHECKING:
    from root_container.field_container.node.path_node_entity import PathNodeEntity
    from root_container.field_container.segment.path_segment_entity import PathSegmentEntity

from entity_base.abstract_circle_entity import AbstractCircleEntity

"""
FOR BEZIER SEGMENTS ONLY
A PathNodeEntity has two ThetaEntities, for the start and end angles.
Only is visible when all three conditions are met
- the segment or node is selected
- when the segment of that side exists
- is not straight
Can snap to cardinal directions, the opposing ThetaEntity, as well as the angle
that would make the angle at the other side of the segment snap
"""

class BezierThetaNode(AbstractCircleEntity):

    # segmentFunction is either getPrevious or getNext
    def __init__(self, segment: PathSegmentEntity, getNode, isStartAngle):

        self.DISTANCE_TO_NODE = 40

        self.getNode: Callable[[], PathNodeEntity] = getNode # callable function to return associated node
        self.segment = segment
        self.isStartAngle = isStartAngle # true if start angle, false if stop angle

        super().__init__(parent = segment,
            drag = DragLambda(self, selectEntityNotThis = segment, FonStartDrag = self.onStartDrag, FonDrag = self.onDrag, FcanDrag = self.canDrag, FonStopDrag = self.onStopDrag),
            drawOrder = DrawOrder.THETA_NODE
        )

        self.COLOR = [255, 0, 255]
        self.COLOR_H = shade(self.COLOR, 0.9)

        """
        The x and y position is stored as an offset (in inches)
        from the node it is tied to
        """
        self.dx, self.dy = None, None

        self.positionRef: PointRef = None

        self.recomputePosition()

    def isVisible(self) -> bool:

        # If segment itself isn't even visible, then this definitely shouldn't be
        if not self.segment.isVisible():
            return False

        # If segment is not bezier, then no theta control
        if self.segment.getSegmentType() != SegmentType.BEZIER:
            return False
        
        # If neither node nor segment is selected, then no theta control
        return self.segment.isSelfOrNodesSelected()
    
    # initially, offsets are set to 1/3 and 2/3 of the segment
    def getInitialOffset(self) -> tuple:
        percent = (1/3) if self.isStartAngle else (-1/3)
        pos1 = self.segment.getPrevious().getPositionRef()
        vector: VectorRef = self.segment.getNext().getPositionRef() - pos1

        return (vector * percent).fieldRef

    
    # PositionRef is updated on recompute. Used by segment for bezier math
    def getPositionRef(self) -> PointRef:
        return self.positionRef
    
    # Given self.px and self.py, find the absolute locations of the 
    # points. Cache positions as PointRef so segment can access them,
    # but return a tuple in absolute screen coordinates as mandated (for drawing) as well
    def defineCenter(self) -> tuple:

        if self.dx is None:

            # delay calculation for initial locations until segment is actually bezier
            if self.segment.getSegmentType() != SegmentType.BEZIER:
                return 0,0
            
            self.dx, self.dy = self.getInitialOffset()

        nx, ny = self.getNode().getPositionRef().fieldRef
        self.positionRef = PointRef(Ref.FIELD, (nx + self.dx, ny + self.dy))
        print(nx, ny, self.dx, self.dy)

        return self.positionRef.screenRef

    # whenever the position of this node has been recomputed, we send
    # a notification to the segment subscribed to this to recalculate
    # the bezier curve
    def defineOther(self):
        self.notify()
    
    
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