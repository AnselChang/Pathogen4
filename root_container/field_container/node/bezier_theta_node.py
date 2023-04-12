from __future__ import annotations
import math
from typing import TYPE_CHECKING, Callable
from common.draw_order import DrawOrder
from common.reference_frame import PointRef, Ref, VectorRef
from entity_base.listeners.drag_listener import DragLambda

from root_container.field_container.segment.segment_type import PathSegmentType
from utility.math_functions import distanceTuples, thetaFromPoints
from utility.pygame_functions import shade
if TYPE_CHECKING:
    from root_container.field_container.node.path_node_entity import PathNodeEntity
    from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
    from root_container.field_container.segment.PathSegmentStates.bezier_segment_state import BezierSegmentState

from entity_base.abstract_circle_entity import AbstractCircleEntity

import pygame

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
    def __init__(self, segment: PathSegmentEntity, bezier: BezierSegmentState, getNode, isStartAngle):

        self.DISTANCE_TO_NODE = 40

        self.bezier = bezier
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
        if self.segment.getSegmentType() != PathSegmentType.BEZIER:
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
            if self.segment.getSegmentType() != PathSegmentType.BEZIER:
                return 0,0
            
            self.dx, self.dy = self.getInitialOffset()

        nx, ny = self.getNode().getPositionRef().fieldRef
        self.positionRef = PointRef(Ref.FIELD, (nx + self.dx, ny + self.dy))

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
        self.offsetX = self.CENTER_X - mouse[0]
        self.offsetY = self.CENTER_Y - mouse[1]

    def canDrag(self, mouse: tuple) -> bool:
        return True
    
    def setRelativeFromAbsolutePosition(self, absolutePosition: PointRef):
        self.dx, self.dy = (absolutePosition - self.getNode().getPositionRef()).fieldRef

    # find the absolute position the node is being dragged to,
    # and using that calculate what the relative position from the
    # associated node should be
    def onDrag(self, mouse: tuple):
        absoluteX = mouse[0] + self.offsetX
        absoluteY = mouse[1] + self.offsetY
        absolutePosition = PointRef(Ref.SCREEN, (absoluteX, absoluteY))

        self.setRelativeFromAbsolutePosition(absolutePosition)

        # calculate bezier curve but fast while dragging (not equidistant points)
        self.recomputePosition()
        self.constrain()
        self.bezier.recomputeBezier(True)
        self.segment.onReshape()

    # reclculate bezier curve but with equidistant points
    def onStopDrag(self):
        self.bezier.recomputeBezier(False)
        self.segment.recomputePosition()

    
    # attempt to constrain the angle to match previous/next angle
    def constrain(self):
        node = self.getNode()

        # can't constrain if no previous/next node
        if self.isStartAngle and node.getPrevious() is None:
            return
        if not self.isStartAngle and node.getNext() is None:
            return
        
        if self.isStartAngle:
            currentTheta = thetaFromPoints(node.getPositionRef().fieldRef, self.positionRef.fieldRef)
        else:
            currentTheta = thetaFromPoints(node.getPositionRef().fieldRef, self.positionRef.fieldRef)

        node.constraints.resetThetaConstraints(currentTheta, node.getPositionRef())

        # SHIFT key disables constraints
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            return
        
        # attempt to constrain to other theta
        if self.isStartAngle:
            otherTheta = node.getPrevious().getStartTheta()
        else:
            otherTheta = node.getNext().getEndTheta()
        node.constraints.addThetaConstraint(otherTheta)

        newTheta = node.constraints.getTheta()

        # if theta has changed, recalculate position.
        # maintain distance to node, but change angle to new theta
        if currentTheta != newTheta:
            magnitude = distanceTuples(self.positionRef.fieldRef, node.getPositionRef().fieldRef)
            absolutePosition = node.getPositionRef() + VectorRef(Ref.FIELD, magnitude = magnitude, heading = newTheta)

            # convert from absolute position to relative offset
            self.setRelativeFromAbsolutePosition(absolutePosition)
            self.recomputePosition()