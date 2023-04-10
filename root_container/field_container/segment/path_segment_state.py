from __future__ import annotations
from typing import TYPE_CHECKING
from data_structures.observer import Observable

from root_container.field_container.segment.segment_type import SegmentType
if TYPE_CHECKING:
    from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
    from root_container.field_container.node.path_node_entity import PathNodeEntity

from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef
from entity_base.entity import Entity
from data_structures.linked_list import LinkedListNode
from adapter.path_adapter import PathAdapter
import pygame

"""
Following the State design pattern, an interface for segment shapes (straight, arc, etc.)
Also provides an interface for getting thetas at both sides, and holding references to nodes
"""

class PathSegmentState(ABC, Observable):
    def __init__(self, type: SegmentType, segment: PathSegmentEntity | LinkedListNode) -> None:
        self.type = type
        self.segment = segment # type PathSegmentEntity (the parent)

    @abstractmethod
    def getAdapter(self) -> PathAdapter:
        pass

    @abstractmethod
    def updateAdapter(self) -> None:
        pass

    def onStateChange(self):
        pass

    @abstractmethod
    def getStartTheta(self) -> float:
        pass

    @abstractmethod
    def getEndTheta(self) -> float:
        pass


    @abstractmethod
    def isTouching(self, position: PointRef) -> bool:
        pass

    @abstractmethod
    def getCenter(self) -> tuple:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pass

    # callback when a node attached to this segment has stopped dragging
    def onNodeStopDrag(self):
        pass