from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from BaseEntity.EntityListeners.click_listener import Click
from BaseEntity.EntityListeners.drag_listener import Drag
from BaseEntity.EntityListeners.select_listener import Select
from BaseEntity.EntityListeners.tick_listener import Tick
from BaseEntity.EntityListeners.hover_listener import Hover

import pygame

class Entity(ABC):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, drag: Drag = None, select: Select = None, click: Click = None, tick: Tick = None, hover: Hover = None, drawOrder: int = 0) -> None:
        self.drawOrder = drawOrder
        self.drag = drag
        self.select = select
        self.click = click
        self.tick = tick
        self.hover = hover
        self.children: list[Entity] = []
    
    def addChild(self, child: 'Entity'):
        self.children.append(child)

    def distanceTo(self, position: PointRef) -> float:
        return (position - self.getPosition()).magnitude(Ref.SCREEN)
        
    @abstractmethod
    def isVisible(self) -> bool:
        pass

    @abstractmethod
    def isTouching(self, position: PointRef) -> bool:
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

    def __str__(self):
        return f"Entity: {self.toString()}"
