from __future__ import annotations
from typing import TYPE_CHECKING, Callable

from common.draw_order import DrawOrder
from entity_base.listeners.mousewheel_listener import MousewheelListener

if TYPE_CHECKING:
    from entity_handler.entity_manager import EntityManager
    from entity_handler.interactor import Interactor
    from common.font_manager import FontManager
    from common.image_manager import ImageManager
    from common.dimensions import Dimensions
    from root_container.field_container.field_entity import FieldEntity


from abc import ABC, abstractmethod
from enum import Enum

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
Any graphical or interactable object should subclass Entity. The constructor of Entity automatically
adds itself to EntityManager, which auto-handles all mouse interaction and drawing capabilities.
Optionally pass in drag, select, etc. listeners to recieve mouse interaction callbacks
for your entity.
"""
_entities: EntityManager = None
_interactor: Interactor = None
_images: ImageManager = None
_fonts: FontManager = None
_dimensions: Dimensions = None
ROOT_CONTAINER = None
def initEntityClass(entityManager: EntityManager, interactor: Interactor, images: ImageManager, fonts: FontManager, dimensions: Dimensions):
    global _entities, _interactor, _images, _fonts, _dimensions, _transform
    _entities = entityManager
    _interactor = interactor
    _images = images
    _fonts = fonts
    _dimensions = dimensions

def setRootContainer(rootContainer):
    global ROOT_CONTAINER
    ROOT_CONTAINER = rootContainer

class Entity(ABC, Observable):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, parent: 'Entity' | None,
                 drag: DragListener = None,
                 select: SelectListener = None,
                 click: ClickListener = None,
                 tick: TickListener = None,
                 hover: HoverListener = None,
                 key: KeyListener = None,
                 mousewheel: MousewheelListener = None,
                 drawOrder: DrawOrder = DrawOrder.BACK,
                 initiallyVisible: bool = True,
                 recomputeWhenInvisible: bool = False,
                 thisUpdatesParent: bool = False,
                 verbose: bool = True,
                 drawOrderRecursive: bool = True,

                 ) -> None:
                
        self.drawOrder = drawOrder
        self.drawOrderRecursive = drawOrderRecursive # if not recursive, draws in front of everything
        self.drag = drag
        self.select = select
        self.click = click
        self.tick = tick
        self.hover = hover
        self.key = key
        self.mousewheel = mousewheel
        self._LOCAL_VISIBLE = initiallyVisible
        self.recomputeWhenInvisible = recomputeWhenInvisible

        # if true, means that recomputing self must first recompute parent
        self.thisUpdatesParent = thisUpdatesParent or (parent is not None and parent.thisUpdatesParent)

        # for debugging with tree()
        self.verbose = verbose

        self.entities = _entities
        self.interactor = _interactor
        self.images = _images
        self.fonts = _fonts
        self.dimensions = _dimensions

        self._children: list[Entity] = []
        self._parent: Entity = parent

        self._widthCached = False
        self._heightCached = False

        if self._parent is not None and self not in self._parent._children:
            self._parent._children.append(self)
            self._parent.onAddChild(self)

        self.entities._addEntity(self)

    def removeChild(self, child: Entity):
        if child in self._children:
            child._parent = None
            self._children.remove(child)
            self.entities.removeEntity(child)
            

    def changeParent(self, newParent: Entity):
        if self._parent is not None and self in self._parent._children:
            self._parent._children.remove(self)

        if self not in newParent._children:
            newParent._children.append(self)

        self._parent = newParent

    # optional callback to override for when child just set this as parent
    def onAddChild(self, child: Entity):
        return

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

        return self.dimensions.SCREEN_WIDTH if self._parent is None else self._pwidth(1)
    
    def defineHeight(self) -> float:

        return self.dimensions.SCREEN_HEIGHT if self._parent is None else self._pheight(1)


    # override this to define anything else before the position is recomputed
    def defineBefore(self) -> None:
        return

    # override this to define anything else after the position is recomputed
    def defineAfter(self) -> None:
        return
        
    # DO NOT OVERRIDE. Call setVisible() and setInvisible() instead.
    # Through this function, a parent entity that is invisible
    # will make all its children invisible as well, and prevent redundant computation
    def isVisible(self) -> bool:

        if self._parent is None:
            return True

        return self._LOCAL_VISIBLE and self._parent.isVisible()
    
    def setVisible(self, recompute: bool = True):

        # if already visible, don't do anything
        if self._LOCAL_VISIBLE:
            return

        self._LOCAL_VISIBLE = True

        if recompute:
            if not self._parent.isVisible():
                # need to make sure parent rect is updated first if parent not visible
                self._parent.recomputeEntity()
            else:
                self.recomputeEntity()

    def setInvisible(self):

        # if already invisible, don't do anything
        if not self._LOCAL_VISIBLE:
            return

        self._LOCAL_VISIBLE = False

    
    def isSelfOrChildrenHovering(self):
        if self.hover is not None and self.hover.isHovering:
            return True
        for child in self._children:
            if child.isSelfOrChildrenHovering():
                return True
        return False
    
    # override
    def getOpacity(self) -> float:
        if self._parent is not None:
            return self._parent.getOpacity()
        return 1 

    # override. By default, is set to mouse inside the entity rect
    def isTouching(self, mouse: tuple) -> float:
        #print(self, self._LOCAL_VISIBLE, self.isVisible(), self._parent)
        self._isTouching = isInsideBox2(*mouse, *self.RECT)
        return self._isTouching
    
    # override
    # with entities of equal DrawOrder, the largest number is drawn in the front 
    def drawOrderTiebreaker(self) -> float:
        return None

    # override
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pass

    # draw rect specified by x, y, width, height. For testing only probably
    def drawRect(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0,0,0), [self.LEFT_X, self.TOP_Y, self.WIDTH, self.HEIGHT], 1)


    def recomputeWidth(self):
        self.WIDTH = self.defineWidth()

    def recomputeHeight(self):
        self.HEIGHT = self.defineHeight()

    def recomputePosition(self):
        self.CENTER_X, self.CENTER_Y = self.defineCenter()
        self.LEFT_X, self.TOP_Y = self.defineTopLeft()
        self.RIGHT_X = self.defineRightX()
        self.BOTTOM_Y = self.defineBottomY()

        # able to define two points instead of width/height
        if self.LEFT_X is not None and self.RIGHT_X is not None:
            self.WIDTH = self.RIGHT_X - self.LEFT_X
        if self.TOP_Y is not None and self.BOTTOM_Y is not None:
            self.HEIGHT = self.BOTTOM_Y - self.TOP_Y

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
            self.LEFT_X = 0 if self._parent is None else self._px(0)
            self.CENTER_X = self.dimensions.SCREEN_WIDTH/2 if self._parent is None else self._px(0.5)
            self.RIGHT_X = self.dimensions.SCREEN_WIDTH if self._parent is None else self._px(1)
        
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
            self.TOP_Y = 0 if self._parent is None else self._py(0)
            self.CENTER_Y = self.dimensions.SCREEN_HEIGHT/2 if self._parent is None else self._py(0.5)
            self.BOTTOM_Y = self.dimensions.SCREEN_HEIGHT if self._parent is None else self._py(1)

        self.WIDTH = int(round(self.WIDTH))
        self.HEIGHT = int(round(self.HEIGHT))
        self.LEFT_X = int(round(self.LEFT_X))
        self.CENTER_X = int(round(self.CENTER_X))
        self.RIGHT_X = int(round(self.RIGHT_X))
        self.TOP_Y = int(round(self.TOP_Y))
        self.CENTER_Y = int(round(self.CENTER_Y))
        self.BOTTOM_Y = int(round(self.BOTTOM_Y))


        self.RECT = [self.LEFT_X, self.TOP_Y, self.WIDTH, self.HEIGHT]

    # Going up the tree, find first ancestor entity with (thisUpdatesParent == False)
    def findAncestorEntityIndependentFromParent(self) -> 'Entity':
        if self._parent is not None and self.thisUpdatesParent:
            return self._parent.findAncestorEntityIndependentFromParent()
        else:
            return self

    # Must call recomputePosition every time the entity changes its position or dimensions
    def recomputeEntity(self, isRoot: bool = True):

        # for initially calling this function, update ancestors first if ancestor dimensions dependent on self
        if isRoot:
            self.entities.redrawScreenThisTick()
            firstEntityToCompute = self.findAncestorEntityIndependentFromParent()
            #print("first", firstEntityToCompute)
            firstEntityToCompute.recomputeEntity(False)
            return

        # only recompute when visible. Otherwise, the position is not defined
        # When the entity is made visible, it will recompute its position
        if not self.isVisible() and not self.recomputeWhenInvisible:
            return
                
        self.defineBefore()
        self.recomputeWidth()
        self.recomputeHeight()
        self.recomputePosition()

        self.defineAfter()


        # Now that this entity position is recomputed, make sure children recompute too
        for child in self._children:
            child.recomputeEntity(False)

    # THESE ARE UTILITY METHODS THAT CAN BE USED TO SPECIFY RELATIVE POSITIONS ABOVE

    def scalePixels(self, pixels: float):
        return pixels * self.dimensions.RESOLUTION_RATIO

    # get relative x as a percent of parent horizontal span
    def _px(self, px):
        return self._parent.LEFT_X + px * self._parent.WIDTH
    
    # from absolute x, get relative x as a percent of parent horizontal span
    def _inverse_px(self, x):
        if self._parent.WIDTH == 0:
            return 0
        return (x - self._parent.LEFT_X) / self._parent.WIDTH
    
    # get relative y as a percent of parent horizontal span
    def _py(self, py):
        return self._parent.TOP_Y + py * self._parent.HEIGHT
    
    # from absolute y, get relative y as a percent of parent horizontal span
    def _inverse_py(self, y):
        if self._parent.HEIGHT == 0:
            return 0
        return (y - self._parent.TOP_Y) / self._parent.HEIGHT
    
    # get relative x in "pixels". One "pixel" is accurate for default resolution
    def _ax(self, pixels):
        return self._parent.LEFT_X + pixels * self.dimensions.X_RATIO
    
    # get relative y in "pixels". One "pixel" is accurate for default resolution
    def _ay(self, pixels):
        return self._parent.TOP_Y + pixels * self.dimensions.Y_RATIO
    
    # get relative width as a percent of parent horizontal span
    def _pwidth(self, pwidth):
        try:
            return self._parent.WIDTH * pwidth
        except:
            raise Exception("Entity not defined", self, self._parent)
    
    # from absolute width, get relative width as a percent of parent horizontal span
    def _inverse_pwidth(self, width):
        if self._parent.WIDTH == 0:
            return 0
        return width / self._parent.WIDTH

    # get relative height as a percent of parent vertical span
    def _pheight(self, pheight):
        return self._parent.HEIGHT * pheight
    
    # from absolute height, get relative height as a percent of parent vertical span
    def _inverse_pheight(self, height):
        if self._parent.HEIGHT == 0:
            return 0
        return height / self._parent.HEIGHT
    
    # Get width given a margin (on both sides) from parent horizontal span
    def _mwidth(self, margin):
        return self._parent.WIDTH - self.dimensions.X_RATIO * margin * 2

    # Get height given a margin (on both sides) from parent vertical span
    def _mheight(self, margin):
        return self._parent.HEIGHT - self.dimensions.Y_RATIO * margin * 2
    
    # Get "absolute" width in "pixels". One "pixel" is accurate for default resolution
    def _awidth(self, pixels):
        return pixels * self.dimensions.X_RATIO
    
    def _inverse_awidth(self, absolutePixels):
        return absolutePixels / self.dimensions.X_RATIO

    # Get "absolute" height in "pixels". One "pixel" is accurate for default resolution
    def _aheight(self, pixels):
        return pixels * self.dimensions.Y_RATIO
    
    def _inverse_aheight(self, absolutePixels):
        return absolutePixels / self.dimensions.Y_RATIO
    
    # Overloading these methods allows us to use the "in" operator
    # to check if this entity contains some child (recursively)
    def __contains__(self, key: 'Entity'):

        if self is key:
            return True

        for child in self._children:
            if key in child:
                return True
            
        return False
    

    def __repr__(self):
        p = ""
        if self._parent is not None:
            p = " " + str(self._parent.__class__.__name__)
        return f"{self.__class__.__name__} (D) " + str(id(self)) + " " + p

    def logMoreInfo(self) -> str:
        return str(self._parent)
    
    # print tree using indentation to indicate hierarchy
    # very useful debugging feature for visualizing parent-child entity relationships
    def tree(self, targetEntity: 'Entity' = None, indent: int = 0, verbose: bool = False):
        targetStr = "(!) " if self is targetEntity else ""
        print("  " * indent + targetStr + str(self))

        if not self.verbose and not verbose:
            return

        for child in self._children:
            child.tree(targetEntity, indent + 1, verbose)