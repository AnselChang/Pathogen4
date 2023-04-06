from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from SegmentEntities.path_segment_state import PathSegmentState
from BaseEntity.entity import Entity

from linked_list import LinkedListNode

from Adapters.path_adapter import PathAdapter
from Adapters.straight_adapter import StraightAdapter, StraightAttributeID

from image_manager import ImageID

from pygame_functions import drawLine
from math_functions import pointTouchingLine

import pygame

# Abstract class for a non-functional edge
# only purpose is to connect two points. 

class StraightSegmentState(PathSegmentState):
    def __init__(self, segment: Entity) -> None:
        super().__init__(segment)
        self.adapter = StraightAdapter()

    def getAdapter(self) -> PathAdapter:
        return self.adapter

    def updateAdapter(self) -> None:
        posA = self.segment.getPrevious().getPosition()
        posB = self.segment.getNext().getPosition()

        self.adapter.set(StraightAttributeID.X1, posA.fieldRef[0], f"{posA.fieldRef[0]:.1f})")
        self.adapter.set(StraightAttributeID.Y1, posA.fieldRef[1], f"{posA.fieldRef[1]:.1f})")
        self.adapter.set(StraightAttributeID.X2, posB.fieldRef[0], f"{posB.fieldRef[0]:.1f})")
        self.adapter.set(StraightAttributeID.Y2, posB.fieldRef[1], f"{posB.fieldRef[1]:.1f})")

        distance = (posB - posA).magnitude(Ref.FIELD)
        self.adapter.set(StraightAttributeID.DISTANCE, distance, f"{distance:.1f}\"")

        self.adapter.setIcon(ImageID.STRAIGHT_REVERSE if self.segment.isReversed else ImageID.STRAIGHT_FORWARD)

    def getStartTheta(self) -> float:
        theta = (self.segment.getNext().getPosition() - self.segment.getPrevious().getPosition()).theta()
        return theta

    def getEndTheta(self) -> float:
        return self.getStartTheta()

    def isTouching(self, position: PointRef) -> bool:
        mx, my = position.screenRef
        x1, y1 = self.segment.getPrevious().getPosition().screenRef
        x2, y2 = self.segment.getNext().getPosition().screenRef
        return pointTouchingLine(mx, my, x1, y1, x2, y2, self.segment.hitboxThickness)


    def getCenter(self) -> tuple:
        fpos = self.segment.getPrevious().getPosition()
        spos = self.segment.getNext().getPosition()

        return (fpos + (spos - fpos) / 2).screenRef


    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        x1, y1 = self.segment.getPrevious().getPosition().screenRef
        x2, y2 = self.segment.getNext().getPosition().screenRef

        drawLine(screen, self.segment.getColor(isActive, isHovered), x1, y1, x2, y2, self.segment.thickness, None)

    def toString(self) -> str:
        return "straight"