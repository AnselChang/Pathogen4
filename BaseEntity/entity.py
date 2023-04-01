from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from BaseEntity.EntityListeners.click_listener import ClickListener
from BaseEntity.EntityListeners.drag_listener import DragListener
from BaseEntity.EntityListeners.select_listener import SelectListener
from BaseEntity.EntityListeners.tick_listener import TickListener
from BaseEntity.EntityListeners.hover_listener import HoverListener

import pygame

"""
Any graphical or interactable object should subclass Entity. By adding entities to
EntityManager, it auto-handles all mouse interaction and drawing capabilities through Interactor.
Optionally pass in drag, select, etc. listeners to recieve mouse interaction callbacks
for your entity.
DrawOrder, with enum defined in draw_order.py, specifies the layering of the drawn objects.
Feel free to add to DrawOrder enum if you want to order a new entity type.
"""

class Entity(ABC):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, drag: DragListener = None, select: SelectListener = None, click: ClickListener = None, tick: TickListener = None, hover: HoverListener = None, drawOrder: int = 0) -> None:
        self.drawOrder = drawOrder
        self.drag = drag
        self.select = select
        self.click = click
        self.tick = tick
        self.hover = hover
        self._children: list[Entity] = []
        self._parent: Entity = None
        
    # setting child will make sure that when parent is removed from manager, children will be too
    # do not call this manually; handled by EntityManager
    def _setParent(self, parent: 'Entity'):
        self._parent = parent
        parent._children.append(self)

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

    def toString(self) -> str:
        "Generic entity"

    def __str__(self):
        return f"Entity: {self.toString()}"
