from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from BaseEntity.EntityListeners.click_listener import ClickListener
from BaseEntity.EntityListeners.drag_listener import DragListener
from BaseEntity.EntityListeners.select_listener import SelectListener
from BaseEntity.EntityListeners.tick_listener import TickListener
from BaseEntity.EntityListeners.hover_listener import HoverListener
from BaseEntity.EntityListeners.key_listener import KeyListener

from dimensions import Dimensions

from Observers.observer import  Observable
from math_functions import distance, isInsideBox2
import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from EntityHandler.entity_manager import EntityManager
    from EntityHandler.interactor import Interactor
    from font_manager import FontManager
    from image_manager import ImageManager
    from dimensions import Dimensions



"""
Any graphical or interactable object should subclass Entity. By adding entities to
EntityManager, it auto-handles all mouse interaction and drawing capabilities through Interactor.
Optionally pass in drag, select, etc. listeners to recieve mouse interaction callbacks
for your entity.
DrawOrder, with enum defined in draw_order.py, specifies the layering of the drawn objects.
Feel free to add to DrawOrder enum if you want to order a new entity type.
"""

_entities: EntityManager = None
_interactor: Interactor = None
_images: ImageManager = None
_fonts: FontManager = None
_dimensions: Dimensions = None
def initEntityClass(entityManager: EntityManager, interactor: Interactor, images: ImageManager, fonts: FontManager, dimensions: Dimensions):
    global _entities, _interactor, _images, _fonts, _dimensions
    _entities = entityManager
    _interactor = interactor
    _images = images
    _fonts = fonts
    _dimensions = dimensions


class Entity(ABC, Observable):

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

        self.entities = _entities
        self.interactor = _interactor
        self.images = _images
        self.fonts = _fonts
        self.dimensions = _dimensions

        self.recomputePosition()

        
    # setting child will make sure that when parent is removed from manager, children will be too
    # do not call this manually; handled by EntityManager
    def _setParent(self, parent: 'Entity'):
        self._parent = parent
        parent._children.append(self)
        self._parent.subscribe(onNotify = self.recomputePosition)

    def distanceTo(self, position: tuple) -> float:
        return distance(*position, self.CENTER_X, self.CENTER_Y)
    
    # impl EITHER getCenter OR getTopLeft
    def getCenter(self) -> tuple:
        lx, ty = self.getTopLeft()
        return lx + self.WIDTH / 2, ty + self.HEIGHT / 2

    def getTopLeft(self) -> tuple:
        cx, cy = self.getCenter()
        return cx - self.WIDTH / 2, cy - self.HEIGHT / 2

    # must impl both of these if want to contain other entity
    def getWidth(self) -> float:
        return 0
    def getHeight(self) -> float:
        return 0
        
    # override
    def isVisible(self) -> bool:
        if self._parent is not None:
            return self._parent.isVisible()
        return True
    
    def getOpacity(self) -> float:
        if self._parent is not None:
            return self._parent.getOpacity()
        return 1 

    # override for non-rect behavior
    def isTouching(self, position: tuple) -> bool:
        return isInsideBox2(*position, *self.RECT)

    # override
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pass

    # draw rect specified by x, y, width, height. For testing only probably
    def drawRect(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0,0,0), [self.LEFT_X, self.TOP_Y, self.WIDTH, self.HEIGHT])

    
    # Must call recomputePosition every time the entity changes its position or dimensions
    def recomputePosition(self):
        self.WIDTH = self.getWidth()
        self.HEIGHT = self.getHeight()
        self.CENTER_X, self.CENTER_Y = self.getCenter()
        self.LEFT_X, self.TOP_Y = self.getTopLeft()

        self.RECT = [self.LEFT_X, self.TOP_Y, self.WIDTH, self.HEIGHT]

        # Now that this entity position is recomputed, make sure children recompute too
        for child in self._children:
            child.recomputePosition()

    # THESE ARE UTILITY METHODS THAT CAN BE USED TO SPECIFY RELATIVE POSITIONS ABOVE

    # get relative x as a percent of parent horizontal span
    def _px(self, px):
        parentX = 0 if self._parent is None else self._parent.LEFT_X
        return int(round(parentX + px * self._parent.WIDTH))
    
    # get relative x as a percent of parent horizontal span
    def _py(self, py):
        parentY = 0 if self._parent is None else self._parent.TOP_Y
        return int(round(parentY + py * self._parent.HEIGHT))
    
    # get relative x in "pixels". One "pixel" is accurate for default resolution
    def _ax(self, pixels):
        parentX = 0 if self._parent is None else self._parent.LEFT_X
        return int(round(parentX + pixels * self.dimensions.RESOLUTION_RATIO))
    
    # get relative y in "pixels". One "pixel" is accurate for default resolution
    def _ay(self, pixels):
        parentY = 0 if self._parent is None else self._parent.TOP_Y
        return int(round(parentY + pixels * self.dimensions.RESOLUTION_RATIO))
    
    # get relative width as a percent of parent horizontal span
    def _pwidth(self, pwidth):
        parentWidth = self.dimensions.SCREEN_WIDTH if self._parent is None else self._parent.WIDTH
        return int(round(parentWidth * pwidth))
    
    # get relative height as a percent of parent vertical span
    def _pheight(self, pheight):
        parentHeight = self.dimensions.SCREEN_HEIGHT if self._parent is None else self._parent.HEIGHT
        return int(round(parentHeight * pheight))
    
    # Get width given a margin (on both sides) from parent horizontal span
    def _mwidth(self, margin):
        parentWidth = self.dimensions.SCREEN_WIDTH if self._parent is None else self._parent.WIDTH
        return int(round(parentWidth - self.dimensions.RESOLUTION_RATIO * margin * 2))

    # Get height given a margin (on both sides) from parent vertical span
    def _mheight(self, margin):
        parentHeight = self.dimensions.SCREEN_HEIGHT if self._parent is None else self._parent.HEIGHT
        return int(round(parentHeight - self.dimensions.RESOLUTION_RATIO * margin * 2))
    
    # Get "absolute" width in "pixels". One "pixel" is accurate for default resolution
    def _awidth(self, pixels):
        return int(round(pixels * self.dimensions.RESOLUTION_RATIO))

    # Get "absolute" height in "pixels". One "pixel" is accurate for default resolution
    def _aheight(self, pixels):
        return int(round(pixels * self.dimensions.RESOLUTION_RATIO))