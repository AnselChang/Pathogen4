from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, VectorRef

from BaseEntity.EntityFunctions.click_function import Click
from BaseEntity.EntityFunctions.drag_function import Drag
from BaseEntity.EntityFunctions.select_function import Select

import pygame

class Entity(ABC):
    def __init__(self, drag: Drag = None, select: Select = None, click: Click = None) -> None:
        self.drag = drag
        self.select = select
        self.click = click
        
    @abstractmethod
    def isVisible(self) -> bool:
        pass

    @abstractmethod
    def isTouching(self, position: PointRef) -> bool:
        pass

    @abstractmethod
    def getPosition(self) -> PointRef:
        self

    @abstractmethod
    def draw(self, screen: pygame.Surface, isActive: bool) -> bool:
        pass

    @abstractmethod
    def toString(self) -> str:
        pass

    def __str__(self):
        return f"Entity: {self.toString()}"
