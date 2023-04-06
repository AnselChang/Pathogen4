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

class PathSegmentState(ABC):
    def __init__(self, segment: Entity | LinkedListNode) -> None:
        self.segment = segment # type PathSegmentEntity (the parent)

    @abstractmethod
    def getAdapter(self) -> PathAdapter:
        pass

    @abstractmethod
    def updateAdapter(self) -> None:
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

    @abstractmethod
    def toString(self) -> str:
        pass