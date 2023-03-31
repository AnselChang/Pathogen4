from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from BaseEntity.EntityListeners.click_listener import ClickLambda
from BaseEntity.EntityListeners.select_listener import SelectLambda
from BaseEntity.entity import Entity

from SegmentEntities.path_segment_state import PathSegmentState
from SegmentEntities.PathSegmentStates.straight_segment_state import StraightSegmentState

from Adapters.path_adapter import PathAdapter, AdapterInterface

from linked_list import LinkedListNode

from draw_order import DrawOrder
from pygame_functions import shade
import pygame

"""
Acts as a "context" class in the state design pattern. Owns PathSegmentState objects
that define behavior for straight/arc/bezier shapes. Easy to switch between states
We also define the constants that apply across all segment types here, like color and thickness
"""

class PathSegmentEntity(Entity, AdapterInterface, LinkedListNode[Entity]):
    def __init__(self, interactor) -> None:
        
        super().__init__(select = SelectLambda(self, "segment", FonSelect = lambda: print("select"), FonDeselect=lambda:print("deselect")),
                         click = ClickLambda(self,FOnDoubleClick = self.onDoubleClick),
                         drawOrder = DrawOrder.SEGMENT)
        
        LinkedListNode.__init__(self)

        self.interactor = interactor
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
        
    def isVisible(self) -> bool:
        return True
    
    def getStartTheta(self) -> float:
        return self.state.getStartTheta()

    def getEndTheta(self) -> float:
        return self.state.getEndTheta()
    
    def isTouching(self, position: PointRef) -> bool:
        return self.state.isTouching(position)

    def distanceTo(self, position: PointRef) -> float:
        return self.state.distanceTo(position)

    def getPosition(self) -> PointRef:
        return self.state.getPosition()

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        return self.state.draw(screen, isActive, isHovered)
    
    def toString(self) -> str:
        "Segment with shape: " + self.state.toString()