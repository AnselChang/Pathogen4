from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.field_container.node.path_node_entity import PathNodeEntity

from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref

from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.select_listener import SelectLambda
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
                         select = SelectLambda(self, "segment"),
                         click = ClickLambda(self,FOnDoubleClick = self.onDoubleClick),
                         drawOrder = DrawOrder.SEGMENT)
        
        LinkedListNode.__init__(self)

        self.state: PathSegmentState = StraightSegmentState(self)
        self.isReversed = False

        self.thickness = 3
        self.hitboxThickness = 5
        self.colorForward = [122, 191, 118]
        self.colorForwardH = shade(self.colorForward, 0.9)
        self.colorForwardA = shade(self.colorForward, 0.4)
        self.colorReversed = [191, 118, 118]
        self.colorReversedH = shade(self.colorReversed, 0.9)
        self.colorReversedA = shade(self.colorReversed, 0.4)

        self.updateAdapter()
        self.recomputePosition()


    def changeSegmentShape(self, newStateClass: type[PathSegmentState]):
        self.state = newStateClass(self)
        self.section.changeSegmentShape(self.getAdapter())

    def onNodeMove(self, node: Entity):
        self.updateAdapter()
        if node is self.getPrevious():
            self.getNext().onAngleChange()
        else:
            self.getPrevious().onAngleChange()

    def getAdapter(self) -> PathAdapter:
        return self.state.getAdapter()
    
    def updateAdapter(self) -> None:
        self.state.updateAdapter()

    def onDoubleClick(self):
        entities = [self, self.getPrevious(), self.getNext()]
        self.interactor.setSelectedEntities(entities)

    def reverseSegmentDirection(self):
        self.isReversed = not self.isReversed

    def getColor(self, isActive: bool = False, isHovered: bool = False):

        if self.isReversed:
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