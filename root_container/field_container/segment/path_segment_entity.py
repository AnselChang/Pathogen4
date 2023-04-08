from __future__ import annotations
from typing import TYPE_CHECKING

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
    def __init__(self, parent: Entity) -> None:
        
        super().__init__(parent = parent,
                         select = SelectLambda(self, "segment", type = SelectorType.SOLO),
                         drag = DragLambda(self,
                                           FonStartDrag = self.onStartDrag,
                                           FcanDrag = self.canDrag,
                                           FonDrag = self.onDrag,
                                           FonStopDrag = self.onStopDrag
                                           ),
                         drawOrder = DrawOrder.SEGMENT)
        
        LinkedListNode.__init__(self)

        self.state: PathSegmentState = StraightSegmentState(self)
        self.direction: SegmentDirection = SegmentDirection.FORWARD

        self.thickness = 3
        self.hitboxThickness = 5
        self.colorForward = [122, 210, 118]
        self.colorForwardH = shade(self.colorForward, 0.9)
        self.colorForwardA = shade(self.colorForward, 0.4)
        self.colorReversed = [191, 118, 118]
        self.colorReversedH = shade(self.colorReversed, 0.9)
        self.colorReversedA = shade(self.colorReversed, 0.4)

        self.updateAdapter()
        self.recomputePosition()

    def onStartDrag(self, mouse: tuple):
        self.mouseStartDrag = PointRef(Ref.SCREEN, mouse)
        self.nodeStartPosition = []
        for node in [self.getPrevious(), self.getNext()]:
            self.nodeStartPosition.append(node.position)
            node.constraints.show()

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
            node.constraints.reset(node.position)

        delta = VectorRef(Ref.FIELD, (0,0))
        for node in [self.getPrevious(), self.getNext()]:
            node.constrainPosition()
            if node.constraints.snappable():
                delta = node.constraints.get() - node.position
                break # can only snap one node at a time

        for node in [self.getPrevious(), self.getNext()]:
            node.position += delta
            node.onNodeMove()

    def onStopDrag(self):
        for node in [self.getPrevious(), self.getNext()]:
            node.constraints.hide()

    # a segment is temporary if the nodes on either ends are temporary
    def isTemporary(self) -> bool:
        if self.getPrevious() is not None and self.getPrevious().isTemporary():
            return True
        if self.getNext() is not None and self.getNext().isTemporary():
            return True
        return False


    def changeSegmentShape(self, newStateClass: type[PathSegmentState]):
        self.state = newStateClass(self)
        self.section.changeSegmentShape(self.getAdapter())

    def onNodeMove(self, node: Entity):
        self.updateAdapter()
        self.recomputePosition()
        if node is self.getPrevious():
            self.getNext().onAngleChange()
        else:
            self.getPrevious().onAngleChange()

    def getAdapter(self) -> PathAdapter:
        return self.state.getAdapter()
    
    def updateAdapter(self) -> None:
        self.state.updateAdapter()


    def toggleDirection(self):
        if self.direction == SegmentDirection.FORWARD:
            self.direction = SegmentDirection.REVERSE
        else:
            self.direction = SegmentDirection.FORWARD
        self.updateAdapter()

    def getDirection(self):
        return self.direction

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
        return self.state.getStartTheta()

    def getEndTheta(self) -> float:
        return self.state.getEndTheta()
    
    def isTouching(self, position: PointRef) -> bool:
        return self.state.isTouching(position)

    def defineCenter(self) -> tuple:
        return self.state.getCenter()

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        return self.state.draw(screen, isActive, isHovered)
    
    def toString(self) -> str:
        "Segment with shape: " + self.state.toString()