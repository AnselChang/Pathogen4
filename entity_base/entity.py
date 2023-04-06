from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity_handler.entity_manager import EntityManager
    from entity_handler.interactor import Interactor
    from common.font_manager import FontManager
    from common.image_manager import ImageManager
    from common.dimensions import Dimensions

from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref

from entity_base.listeners.click_listener import ClickListener
from entity_base.listeners.drag_listener import DragListener
from entity_base.listeners.select_listener import SelectListener
from entity_base.listeners.tick_listener import TickListener
from entity_base.listeners.hover_listener import HoverListener
from entity_base.listeners.key_listener import KeyListener

from common.dimensions import Dimensions

from data_structures.observer import  Observable
from utility.math_functions import distance, isInsideBox2
import pygame





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
ROOT_ENTITY = None
def initEntityClass(entityManager: EntityManager, interactor: Interactor, images: ImageManager, fonts: FontManager, dimensions: Dimensions):
    global _entities, _interactor, _images, _fonts, _dimensions, ROOT_ENTITY
    _entities = entityManager
    _interactor = interactor
    _images = images
    _fonts = fonts
    _dimensions = dimensions

    # top-level entities like panel should set this as parent
    ROOT_ENTITY = _entities.rootEntity

class Entity(ABC, Observable):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, parent: 'Entity' | None,
                 drag: DragListener = None,
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

        self.entities = _entities
        self.interactor = _interactor
        self.images = _images
        self.fonts = _fonts
        self.dimensions = _dimensions

        self._children: list[Entity] = []
        self._parent: Entity = parent

        if self._parent is not None:
            self._parent._children.append(self)

        self.entities._addEntity(self)

        self.recomputePosition()


    def distanceTo(self, position: tuple) -> float:
        return distance(*position, self.CENTER_X, self.CENTER_Y)
    
    # MUST define x and y ONCE each through combination of below functions
    def defineCenter(self) -> tuple:
        return self.defineCenterX(), self.defineCenterY()

    def defineTopLeft(self) -> tuple:
        return self.defineLeftX(), self.defineTopY()
    
    def defineCenterX(self) -> float:
        return None
    
    def defineLeftX(self) -> float:
        return None
    
    def defineRightX(self) -> float:
        return None
    
    def defineCenterY(self) -> float:
        return None
    
    def defineTopY(self) -> float:
        return None
    
    def defineBottomY(self) -> float:
        return None

    # must impl both of these if want to contain other entity
    # by default, set to the parent width and height
    def defineWidth(self) -> float:
        return self._pwidth(1)
    def defineHeight(self) -> float:
        return self._pheight(1)
    
    # override this to define anything else after the position is recomputed
    def defineOther(self) -> None:
        return
        
    # override
    def isVisible(self) -> bool:
        return self._parent.isVisible()
    
    # override
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
        self.WIDTH = self.defineWidth()
        self.HEIGHT = self.defineHeight()
        self.CENTER_X, self.CENTER_Y = self.defineCenter()
        self.LEFT_X, self.TOP_Y = self.defineTopLeft()
        self.RIGHT_X = self.defineRightX()
        self.BOTTOM_Y = self.defineBottomY()

        if self.LEFT_X is not None:
            self.CENTER_X = self.LEFT_X + self.WIDTH / 2
            self.RIGHT_X = self.LEFT_X + self.WIDTH
        elif self.CENTER_X is not None:
            self.LEFT_X = self.CENTER_X - self.WIDTH / 2
            self.RIGHT_X = self.LEFT_X + self.WIDTH
        elif self.RIGHT_X is not None:
            self.LEFT_X = self.RIGHT_X - self.WIDTH
            self.CENTER_X = self.LEFT_X + self.WIDTH / 2
        else: # if no position defined, entity rect is set to parent entity rect
            self.LEFT_X = self._px(0)
            self.CENTER_X = self._px(0.5)
            self.RIGHT_X = self._px(1)
        
        if self.TOP_Y is not None:
            self.CENTER_Y = self.TOP_Y + self.HEIGHT / 2
            self.BOTTOM_Y = self.TOP_Y + self.HEIGHT
        elif self.CENTER_Y is not None:
            self.TOP_Y = self.CENTER_Y - self.HEIGHT / 2
            self.BOTTOM_Y = self.TOP_Y + self.HEIGHT
        elif self.BOTTOM_Y is not None:
            self.TOP_Y = self.BOTTOM_Y - self.HEIGHT
            self.CENTER_Y = self.TOP_Y + self.HEIGHT / 2
        else: # if no position defined, entity rect is set to parent entity rect
            self.TOP_Y = self._px(0)
            self.CENTER_Y = self._px(0.5)
            self.BOTTOM_Y = self._px(1)

        self.WIDTH = int(round(self.WIDTH))
        self.HEIGHT = int(round(self.HEIGHT))
        self.LEFT_X = int(round(self.LEFT_X))
        self.CENTER_X = int(round(self.CENTER_X))
        self.RIGHT_X = int(round(self.RIGHT_X))
        self.TOP_Y = int(round(self.TOP_Y))
        self.CENTER_Y = int(round(self.CENTER_Y))
        self.BOTTOM_Y = int(round(self.BOTTOM_Y))


        self.RECT = [self.LEFT_X, self.TOP_Y, self.WIDTH, self.HEIGHT]

        self.defineOther()

        # Now that this entity position is recomputed, make sure children recompute too
        for child in self._children:
            child.recomputePosition()

    # THESE ARE UTILITY METHODS THAT CAN BE USED TO SPECIFY RELATIVE POSITIONS ABOVE

    # get relative x as a percent of parent horizontal span
    def _px(self, px):
        return self._parent.LEFT_X + px * self._parent.WIDTH
    
    # get relative x as a percent of parent horizontal span
    def _py(self, py):
        return self._parent.TOP_Y + py * self._parent.HEIGHT
    
    # get relative x in "pixels". One "pixel" is accurate for default resolution
    def _ax(self, pixels):
        return self._parent.LEFT_X + pixels * self.dimensions.RESOLUTION_RATIO
    
    # get relative y in "pixels". One "pixel" is accurate for default resolution
    def _ay(self, pixels):
        return self._parent.TOP_Y + pixels * self.dimensions.RESOLUTION_RATIO
    
    # get relative width as a percent of parent horizontal span
    def _pwidth(self, pwidth):
        return self._parent.WIDTH * pwidth
    
    # get relative height as a percent of parent vertical span
    def _pheight(self, pheight):
        return self._parent.HEIGHT * pheight
    
    # Get width given a margin (on both sides) from parent horizontal span
    def _mwidth(self, margin):
        return self._parent.WIDTH - self.dimensions.RESOLUTION_RATIO * margin * 2

    # Get height given a margin (on both sides) from parent vertical span
    def _mheight(self, margin):
        return self._parent.HEIGHT - self.dimensions.RESOLUTION_RATIO * margin * 2
    
    # Get "absolute" width in "pixels". One "pixel" is accurate for default resolution
    def _awidth(self, pixels):
        return pixels * self.dimensions.RESOLUTION_RATIO

    # Get "absolute" height in "pixels". One "pixel" is accurate for default resolution
    def _aheight(self, pixels):
        return pixels * self.dimensions.RESOLUTION_RATIO