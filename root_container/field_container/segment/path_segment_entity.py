from __future__ import annotations
from typing import TYPE_CHECKING
from entity_base.listeners.tick_listener import TickLambda
from root_container.field_container.node.arc_curve_node import ArcCurveNode
from root_container.field_container.node.bezier_lines import BezierLines
from root_container.field_container.node.bezier_theta_node import BezierThetaNode

from root_container.field_container.segment.segment_type import SegmentType
if TYPE_CHECKING:
    from root_container.path import Path

from entity_base.listeners.drag_listener import DragLambda
from root_container.field_container.segment.segment_direction import SegmentDirection
from utility.math_functions import isInsideBox
if TYPE_CHECKING:
    from root_container.field_container.node.path_node_entity import PathNodeEntity

from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref, VectorRef

from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType
from entity_base.entity import Entity

from root_container.field_container.segment.path_segment_state import PathSegmentState
from root_container.field_container.segment.PathSegmentStates.bezier_segment_state import BezierSegmentState
from root_container.field_container.segment.PathSegmentStates.arc_segment_state import ArcSegmentState
from root_container.field_container.segment.PathSegmentStates.straight_segment_state import StraightSegmentState

from adapter.path_adapter import PathAdapter, AdapterInterface

from data_structures.linked_list import LinkedListNode

from common.draw_order import DrawOrder
from utility.pygame_functions import shade
import pygame

"""
Acts as a "context" class in the state design pattern. Owns PathSegmentState objects
that define behavior for straight/arc/bezier shapes. Easy to switch between states
We also define the constants that apply across all segment types here, like color and thickness
"""

class PathSegmentEntity(Entity, AdapterInterface, LinkedListNode['PathNodeEntity']):
    def __init__(self, parent: Entity, path: Path) -> None:
        
        super().__init__(parent = parent,
                         select = SelectLambda(self, "segment", type = SelectorType.SOLO),
                         drag = DragLambda(self,
                                           FonStartDrag = self.onStartDrag,
                                           FcanDrag = self.canDrag,
                                           FonDrag = self.onDrag,
                                           FonStopDrag = self.onStopDrag
                                           ),
                         tick = TickLambda(self, self.tick),
                         drawOrder = DrawOrder.SEGMENT)
        
        LinkedListNode.__init__(self)

        self.path = path

        self.states: dict[SegmentType, PathSegmentState] = {
            SegmentType.STRAIGHT: StraightSegmentState(self),
            SegmentType.ARC: ArcSegmentState(self),
            SegmentType.BEZIER: BezierSegmentState(self)
        }
        # on state update, recompute itself
        for stateID in self.states:
            self.states[stateID].subscribe(self.recomputePosition)

        self.currentState: SegmentType = SegmentType.STRAIGHT

        self.direction: SegmentDirection = SegmentDirection.FORWARD

        self.hitboxThickness = 5
        self.colorForward = [122, 210, 118]
        self.colorForwardH = shade(self.colorForward, 0.92)
        self.colorForwardA = shade(self.colorForward, 0.7)
        self.colorReversed = [191, 118, 118]
        self.colorReversedH = shade(self.colorReversed, 0.92)
        self.colorReversedA = shade(self.colorReversed, 0.7)

        # Since the construction of this segment is not complete, with
        # having both nodes not guaranteed, initialization of ArcCurveEntity
        # is delayed until both nodes are set at updateAdapter()
        self.arcNode: ArcCurveNode = None

        self.isFullyInitialized = False

        self.updateAdapter()
        self.recomputePosition()

        
    def tick(self):
        return
        print(self.getPrevious(), self.getNext())

    def getState(self) -> PathSegmentState:
        return self.states[self.currentState]
    
    def setState(self, newState: SegmentType) -> None:
        self.currentState = newState

        self.getState().onStateChange()
        self.updateAdapter()

        self.getPrevious().onAngleChange()
        self.getNext().onAngleChange()

    def onStartDrag(self, mouse: tuple):
        self.mouseStartDrag = PointRef(Ref.SCREEN, mouse)
        self.nodeStartPosition = []
        for node in [self.getPrevious(), self.getNext()]:
            self.nodeStartPosition.append(node.position)
            node.constraints.showPosition()

    def canDrag(self, mouseTuple: tuple) -> bool:
        mouse = PointRef(Ref.SCREEN, mouseTuple)

        self.mouseDelta = mouse - self.mouseStartDrag
        self.nodeGoalPosition = []
        for i, node in enumerate([self.getPrevious(), self.getNext()]):
            newPos = self.nodeStartPosition[i] + self.mouseDelta
            self.nodeGoalPosition.append(newPos)
            if not isInsideBox(*newPos.fieldRef, 0, 0, 144, 144):
                return False
        return True

    # When dragging, determine if either node is snappable. If so, do it
    def onDrag(self, mouseTuple: PointRef):
        for i, node in enumerate([self.getPrevious(), self.getNext()]):
            node.position = self.nodeGoalPosition[i]
            node.constraints.resetPositionConstraints(node.position)

        delta = VectorRef(Ref.FIELD, (0,0))
        for node in [self.getPrevious(), self.getNext()]:
            node.constrainPosition()
            if node.constraints.snappable():
                delta = node.constraints.getPosition() - node.position
                break # can only snap one node at a time

        for node in [self.getPrevious(), self.getNext()]:
            node.position += delta
            node.onNodeMove()

    def onStopDrag(self):
        for node in [self.getPrevious(), self.getNext()]:
            node.constraints.hidePosition()

    # callback when a node attached to this segment has stopped dragging
    # Pass callback on to segment states if they need to do something
    def onNodeStopDrag(self):
        self.getState().onNodeStopDrag()

    # a segment is temporary if the nodes on either ends are temporary
    def isTemporary(self) -> bool:
        if self.getPrevious() is not None and self.getPrevious().isTemporary():
            return True
        if self.getNext() is not None and self.getNext().isTemporary():
            return True
        return False

    def onNodeMove(self, node: Entity):
        self.updateAdapter()
        self.recomputePosition()
        self.arcNode.recomputePositionRef()
        if node is self.getPrevious():
            self.getNext().onAngleChange()
        else:
            self.getPrevious().onAngleChange()

    def getAdapter(self) -> PathAdapter:
        return self.getState().getAdapter()
    
    def updateAdapter(self) -> None:

        # initailize arc node
        if not self.isFullyInitialized and self.getNext() is not None and self.getPrevious() is not None:
            self.arcNode = ArcCurveNode(self, self.states[SegmentType.ARC])
            self.bezierTheta1 = BezierThetaNode(self, self.states[SegmentType.BEZIER], self.getPrevious, True)
            self.bezierTheta2 = BezierThetaNode(self, self.states[SegmentType.BEZIER], self.getNext, False)

            # must call this after initilizing arcNode and bezierThetas,
            # so that position recomputation happens before drawing lines
            BezierLines(self)

            self.isFullyInitialized = True

        self.getState().updateAdapter()
        self.recomputePosition()


    def toggleDirection(self):
        if self.direction == SegmentDirection.FORWARD:
            self.direction = SegmentDirection.REVERSE
        else:
            self.direction = SegmentDirection.FORWARD
        self.updateAdapter()

    def getDirection(self):
        return self.direction
    
    def getSegmentType(self) -> SegmentType:
        return self.currentState

    def getOther(self, node: PathNodeEntity):
        if self.getPrevious() is node:
            return self.getNext()
        elif self.getNext() is node:
            return self.getPrevious()
        else:
            raise ValueError("Node is not connected to this segment")

    def getColor(self, isActive: bool = False, isHovered: bool = False):

        if self.direction == SegmentDirection.REVERSE:
            if isActive:
                return self.colorReversedA
            elif isHovered:
                return self.colorReversedH
            else:
                return self.colorReversed
        else:
            if isActive:
                return self.colorForwardA
            elif isHovered:
                return self.colorForwardH
            else:
                return self.colorForward

    
    def getStartTheta(self) -> float:
        return self.getState().getStartTheta()

    def getEndTheta(self) -> float:
        return self.getState().getEndTheta()
    
    def getLinearDistance(self, ref: Ref):
        return (self.getPrevious().position - self.getNext().position).magnitude(ref)
    
    def getThetaAtNode(self, node: PathNodeEntity):
        if self.getPrevious() is node:
            return self.getStartTheta()
        elif self.getNext() is node:
            return self.getEndTheta()
        else:
            raise Exception("Node is not connected to this segment")
    
    def isTouching(self, position: PointRef) -> bool:
        return self.getState().isTouching(position)

    def defineCenter(self) -> tuple:
        return self.getState().getCenter()
    
    def getThickness(self) -> int:
        return int(3 * self.dimensions.RESOLUTION_RATIO)
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        return self.getState().draw(screen, isActive, isHovered)
    
    def isSelfOrNodesSelected(self):
        if self.select.isSelected:
            return True
        elif self.getPrevious().select.isSelected:
            return True
        elif self.getNext().select.isSelected:
            return True
        return False