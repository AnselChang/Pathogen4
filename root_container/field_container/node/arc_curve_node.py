from __future__ import annotations
import math
from typing import TYPE_CHECKING
from common.draw_order import DrawOrder
from common.reference_frame import *
from data_structures.observer import Observable
from entity_base.listeners.drag_listener import DragLambda

from entity_base.listeners.select_listener import SelectLambda, SelectorType
from root_container.field_container.node.arc_node_line import ArcNodeLine
from root_container.field_container.segment.segment_type import PathSegmentType
from utility.math_functions import distancePointToLine
from utility.pygame_functions import shade
if TYPE_CHECKING:
    from root_container.field_container.node.path_node_entity import PathNodeEntity
    from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
    from root_container.field_container.segment.PathSegmentStates.arc_segment_state import ArcSegmentState


from entity_base.abstract_circle_entity import AbstractCircleEntity

"""
FOR ARC SEGMENTS ONLY
A PathSegmentEntity owns an ArcCurveEntity, which lies at its perpendicular bisector
Only is visible when all three conditions are met
- the segment or node is selected
- when the segment of that side exists
- is not straight
Can snap to cardinal directions, the opposing ThetaEntity, as well as the angle
that would make the angle at the other side of the segment snap
"""

class ArcCurveNode(AbstractCircleEntity, Observable):

    # segmentFunction is either getPrevious or getNext
    def __init__(self, segment: PathSegmentEntity, arcSegmentState: ArcSegmentState):

        self.segment = segment
        self.arc = arcSegmentState

        super().__init__(parent = segment,
            drag = DragLambda(self, selectEntityNotThis = segment, FonStartDrag = self.onStartDrag, FonDrag = self.onDrag, FcanDrag = self.canDrag, FonStopDrag = self.onStopDrag),
            drawOrder = DrawOrder.THETA_NODE
        )

        self.COLOR = [255, 128, 0]
        self.COLOR_H = shade(self.COLOR, 0.9)

        # perpendicular distance from midpoint to self, signed
        # in field ref (inches)
        self.perpDistance = 10
        self.recomputePositionRef()

        # handles drawing the line from the segment midpoint to this
        ArcNodeLine(self)

    def isVisible(self) -> bool:

        # If segment itself isn't even visible, then this definitely shouldn't be
        if not self.segment.isVisible():
            return False
        
        # If segment is not arc, then no theta control
        if self.segment.getSegmentType() != PathSegmentType.ARC:
            return False
        
        # If segment or neighboring nodes are not selected, then no theta control
        return self.segment.isSelfOrNodesSelected()
    
    # recompute arc curve position given perpDistance
    def recomputePositionRef(self):
        # A and B are PointRef of neighboring nodes
        self.A = self.segment.getPrevious().getPositionRef()
        self.B = self.segment.getNext().getPositionRef()

        # M is midpoint between A and B
        self.segmentMidpoint: PointRef = self.A + (self.B - self.A) / 2

        # Theta from M to P (position)
        theta = (self.B - self.A).theta() + math.pi/2
        self.positionRef = self.segmentMidpoint + VectorRef(Ref.FIELD, magnitude = self.perpDistance, heading = theta)
        self.recomputePosition()

    # return cached position in screen coordinates
    def defineCenter(self) -> tuple:
        return self.positionRef.screenRef
    
    def getColor(self, isHovered: bool = False) -> tuple:
        return self.COLOR_H if isHovered else self.COLOR

    def getRadius(self, isHovered: bool = False) -> float:
        return 6 if isHovered else 5

    def onStartDrag(self, mouse: tuple):
        self.segment.getPrevious().constraints.showTheta()
        self.segment.getNext().constraints.showTheta()

    def canDrag(self, mouse: tuple) -> bool:
        return True

    def onDrag(self, mouse: tuple):
        mouseRef = PointRef(Ref.SCREEN, mouse)
        self.setPerpDistance(distancePointToLine(*mouseRef.fieldRef, *self.B.fieldRef, *self.A.fieldRef, True))
        self.recomputePositionRef()

        self.arc.recalculateArcFromArcCurveNode()
        self.arc.constrainTheta()
        self.segment.onReshape()

    def setPerpDistance(self, perpDistance: float):
        # prevent arc from ever being perfectly straight, which causes division issues
        #print(perpDistance)
        MIN_MAGNITUDE = 1e-2
        if abs(perpDistance) < MIN_MAGNITUDE:
            #print("as")
            perpDistance = MIN_MAGNITUDE if perpDistance > 0 else -MIN_MAGNITUDE

        self.perpDistance = perpDistance
        self.recomputePositionRef()

    def onStopDrag(self):
        self.segment.getPrevious().constraints.hideTheta()
        self.segment.getNext().constraints.hideTheta()
