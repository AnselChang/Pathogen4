from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from BaseEntity.EntityListeners.click_listener import ClickListener
from BaseEntity.EntityListeners.drag_listener import DragListener
from BaseEntity.EntityListeners.select_listener import SelectListener
from BaseEntity.EntityListeners.tick_listener import TickListener
from BaseEntity.EntityListeners.hover_listener import HoverListener
from BaseEntity.EntityListeners.key_listener import KeyListener

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
    def __init__(self, drag: DragListener = None,
                 select: SelectListener = None,
                 click: ClickListener = None,
                 tick: TickListener = None,
                 hover: HoverListener = None,
                 key: KeyListener = None,
                 drawOrder: int = 0) -> None:
        
        self.drawOrder = drawOrder
        self.drag = drag
        self.select = select
        self.click = click
        self.tick = tick
        self.hover = hover
        self.key = key
        self._children: list[Entity] = []
        self._parent: Entity = None
        
    # setting child will make sure that when parent is removed from manager, children will be too
    # do not call this manually; handled by EntityManager
    def _setParent(self, parent: 'Entity'):
        self._parent = parent
        parent._children.append(self)

    def distanceTo(self, position: tuple) -> float:
        return (position - self.getPosition()).magnitude(Ref.SCREEN)
        
    @abstractmethod
    def isVisible(self) -> bool:
        pass

    @abstractmethod
    def isTouching(self, position: PointRef) -> bool:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pass

    
    # THESE METHODS ARE IMPLEMENTED BY SUBCLASS TO SPECIFY RELATIVE POSITION

    # impl EITHER getCenterX OR getLeftX
    def getCenterX(self) -> float:
        return self.getLeftX() + self.getWidth() / 2
    def getLeftX(self) -> float:
        return self.getCenterX() - self.getWidth() / 2

    # impl EITHER getCenterY OR getTopY
    def getCenterY(self) -> float:
        return self.getTopY() + self.getHeight() / 2
    def getTopY(self) -> float:
        return self.getCenterY() + self.getHeight() / 2

    # must impl both of these
    @abstractmethod
    def getWidth(self) -> float:
        pass
    @abstractmethod
    def getHeight(self) -> float:
        pass

    # THESE ARE UTILITY METHODS THAT CAN BE USED TO SPECIFY RELATIVE POSITIONS ABOVE

    # get relative x as a percent of parent horizontal span
    def _px(self, px):
        if self._parent is None:
            raise Exception("No parent")
        return self._parent.getLeftX() + self._parent.getWidth() / 2
    
    # get relative x as a percent of parent horizontal span
    def _py(self, py):
        if self._parent is None:
            raise Exception("No parent")
        return self._parent.getTopY() + self._parent.getHeight() / 2
    
    # get relative width as a percent of parent horizontal span
    def _pwidth(self, pwidth):
        if self._parent is None:
            raise Exception("No parent")
        return self._parent.getWidth() * pwidth
    
    # get relative height as a percent of parent vertical span
    def _pheight(self, pheight):
        if self._parent is None:
            raise Exception("No parent")
        return self._parent.getHeight() * pheight
    
    # Get width given a margin (on both sides) from parent horizontal span
    def _mwidth(self, margin):
        return self._parent.getWidth() - margin * 2

    
