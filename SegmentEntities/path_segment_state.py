from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef
from BaseEntity.entity import Entity
from SegmentEntities.edge_entity import EdgeEntity
import pygame

"""
Following the State design pattern, an interface for segment shapes (straight, arc, etc.)
Also provides an interface for getting thetas at both sides, and holding references to nodes
"""

class PathSegmentState(ABC):
    def __init__(self, segment: EdgeEntity) -> None:
        self.segment = segment # type PathSegmentEntity (the parent)

    @abstractmethod
    def isTouching(self, position: PointRef) -> bool:
        pass

    @abstractmethod
    def distanceTo(self, position: PointRef) -> float:
        pass

    @abstractmethod
    def getPosition(self) -> PointRef:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pass

    @abstractmethod
    def toString(self) -> str:
        pass