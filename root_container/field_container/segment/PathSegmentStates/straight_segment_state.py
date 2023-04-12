from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.image.image_state import ImageState
from root_container.field_container.segment.segment_direction import SegmentDirection
from root_container.field_container.segment.segment_type import PathSegmentType
from utility.format_functions import formatInches
if TYPE_CHECKING:
    from root_container.field_container.segment.path_segment_entity import PathSegmentEntity

from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref

from root_container.field_container.segment.path_segment_state import PathSegmentState
from entity_base.entity import Entity

from data_structures.linked_list import LinkedListNode

from adapter.path_adapter import PathAdapter
from adapter.straight_adapter import StraightAdapter, StraightAttributeID

from common.image_manager import ImageID

from utility.pygame_functions import drawLine
from utility.math_functions import pointTouchingLine
from enum import Enum, auto

import pygame

class StraightSegmentState(PathSegmentState):
    def __init__(self, segment: PathSegmentEntity) -> None:
        super().__init__(PathSegmentType.STRAIGHT, segment)
        self.adapter = StraightAdapter([
            ImageState(SegmentDirection.FORWARD, ImageID.STRAIGHT_FORWARD),
            ImageState(SegmentDirection.REVERSE, ImageID.STRAIGHT_REVERSE),
        ])

    def getAdapter(self) -> PathAdapter:
        return self.adapter

    def updateAdapter(self) -> None:

        # not properly initialized (yet)
        if self.segment.getPrevious() is None or self.segment.getNext() is None:
            return

        posA = self.segment.getPrevious().getPositionRef()
        posB = self.segment.getNext().getPositionRef()

        self.adapter.set(StraightAttributeID.X1, posA.fieldRef[0], formatInches(posA.fieldRef[0]))
        self.adapter.set(StraightAttributeID.Y1, posA.fieldRef[1], formatInches(posA.fieldRef[1]))
        self.adapter.set(StraightAttributeID.X2, posB.fieldRef[0], formatInches(posB.fieldRef[0]))
        self.adapter.set(StraightAttributeID.Y2, posB.fieldRef[1], formatInches(posB.fieldRef[1]))

        distance = (posB - posA).magnitude(Ref.FIELD)
        if self.segment.getDirection() == SegmentDirection.REVERSE:
            distance *= -1
        self.adapter.set(StraightAttributeID.DISTANCE, distance, formatInches(distance))

        self.adapter.setIconStateID(self.segment.getDirection())

    def getStartTheta(self) -> float:
        theta = (self.segment.getNext().getPositionRef() - self.segment.getPrevious().getPositionRef()).theta()
        return theta

    def getEndTheta(self) -> float:
        return self.getStartTheta()

    def isTouching(self, position: tuple) -> bool:
        x1, y1 = self.segment.getPrevious().getPositionRef().screenRef
        x2, y2 = self.segment.getNext().getPositionRef().screenRef
        return pointTouchingLine(*position, x1, y1, x2, y2, self.segment.getThickness(True))


    def getCenter(self) -> tuple:

        if self.segment.getPrevious() is None or self.segment.getNext() is None:
            return (0, 0)

        fpos = self.segment.getPrevious().getPositionRef()
        spos = self.segment.getNext().getPositionRef()
        return (fpos + (spos - fpos) / 2).screenRef


    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        x1, y1 = self.segment.getPrevious().getPositionRef().screenRef
        x2, y2 = self.segment.getNext().getPositionRef().screenRef

        drawLine(screen, self.segment.getColor(isActive, isHovered), x1, y1, x2, y2, self.segment.getThickness(), None)
