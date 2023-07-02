from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.path_models.path_model import PathModel


from enum import Enum
from common.image_manager import ImageID, ImageManager
from common.dimensions import Dimensions
from entity_base.entity import Entity
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.drag_listener import DragLambda
from entity_base.listeners.mousewheel_listener import MousewheelLambda
from utility.coordinate_transform import CoordinateTransformBuilder
from utility.math_functions import clamp, isInsideBox
from utility.pygame_functions import scaleSurface
from data_structures.observer import Observable
import pygame
import weakref

class Ref(Enum):
    IMAGE_PIXELS = 0
    FIELD_INCHES = 1

"""
Handles logic for the interactive field.
This includes:
- Drawing the background
- Panning and zooming
- Coordinate conversions between image pixels and field inches
     - children inside field can access these methods
"""

class FieldEntity(Entity, Observable):

    def __init__(self, parent: Entity):

        super().__init__(parent,
            mousewheel = MousewheelLambda(self, FonMousewheel = self.onMousewheel),
            drag = DragLambda(self,
                FonStartDrag = self.onStartDrag,
                FonDrag = self.onDrag,
                FonStopDrag = self.onStopDrag
            ),
            click = ClickLambda(self, FonRightClick = self.onRightClick)
        )

        # At zoom = 1, the image is completely fit to the parent rect,
        # NOT the original resolution of the image.
        # Scaling zoom scales this already-scaled value.
        # zoom is applied from top-left corner of parent rect, and then pan.
        self._zoom = 1

        # pan units are in percent
        self._panX, self._panY = (0, 0)

        self.rawSurface = self.images.get(ImageID.FIELD)
        self.RAW_SURFACE_PIXELS = self.rawSurface.get_width()

        # define where (0,0) and (144, 144) are relative to raw image pixels
        # measure these values by identifying the corners of the field in the image
        # on something like Preview on Mac
        self.TOP_LEFT_POS_PIXELS = (65, 58)
        self.BOTTOM_RIGHT_POS_PIXELS = (4947, 4938)

        # 144 inches on the field
        self.FIELD_SIZE_INCHES = 144

        builder = CoordinateTransformBuilder[Ref](Ref.IMAGE_PIXELS, Ref.FIELD_INCHES)
        builder.defineFirstPoint(self.TOP_LEFT_POS_PIXELS, (0, 0))
        fsi = [self.FIELD_SIZE_INCHES, self.FIELD_SIZE_INCHES]
        builder.defineSecondPoint(self.BOTTOM_RIGHT_POS_PIXELS, fsi)
        self.transform = builder.build()

        # cache old rect to see if there was any change, in which case
        # scaled image needs to be recomputed
        self._oldRect = None
        self._oldZoom = None
        self._oldPan = None

    def initPathModel(self, path: PathModel):
        self.model = path

    def onMousewheel(self, offset: int) -> bool:
        P_ZOOM = 0.05
        MIN_ZOOM = 1
        MAX_ZOOM = 3.5 # maximum zoom from fit-to-container size

        oldZoom = self._zoom
        self._zoom += offset * P_ZOOM
        self._zoom = clamp(self._zoom, MIN_ZOOM, MAX_ZOOM)
        zoomDelta = self._zoom - oldZoom

        # Calculate how much to pan to zoom on mouse axis
        mx, my = self.mousewheel.mouse
        px = self._inverse_px(mx)
        py = self._inverse_py(my)

        # apply panning
        px -= self._panX
        py -= self._panY
        px /= self._zoom
        py /= self._zoom

        self._panX -= zoomDelta * px
        self._panY -= zoomDelta * py

        self._boundPan()
        self.recomputeEntity()

        return True # always consume event
    
    def onStartDrag(self, mouse: tuple):
        self.startPan = (self._panX, self._panY)

    def _boundPan(self):
        # panning must always be between (-zoom, 0)
        self._panX = clamp(self._panX, 1-self._zoom, 0)
        self._panY = clamp(self._panY, 1-self._zoom, 0)

    # pan and recompute
    def onDrag(self, mouse: tuple):
        ox, oy = self.drag.totalOffsetX, self.drag.totalOffsetY

        self._panX = self.startPan[0] + self._inverse_pwidth(ox)
        self._panY = self.startPan[1] + self._inverse_pheight(oy)

        self._boundPan()
        self.recomputeEntity()

    def onStopDrag(self):
        pass

    # recompute scaled surface if change in scale
    def defineAfter(self) -> None:
        
        # use cached surface if no change
        if self.RECT == self._oldRect:
            if self._zoom == self._oldZoom:
                if (self._panX, self._panY) == self._oldPan:
                    return
        
        self._oldRect = self.RECT
        self._oldZoom = self._zoom
        self._oldPan = (self._panX, self._panY)

        size = self.WIDTH * self._zoom
        scaledSurface = pygame.transform.smoothscale(self.rawSurface, (size, size))
        self.fieldSurface = pygame.Surface((self.WIDTH, self.HEIGHT))

        offsetX = self._pwidth(self._panX)
        offsetY = self._pheight(self._panY)

        self.fieldSurface.blit(scaledSurface, (offsetX, offsetY))
        
    # convert from absolute coordinates to position on field in inches (0-144)
    def mouseToInches(self, mousePos: tuple) -> tuple:
        # get px (0-1) and py (0-1) for percent position on field
        px = self._inverse_px(mousePos[0])
        py = self._inverse_py(mousePos[1])

        # apply panning
        px -= self._panX
        py -= self._panY

        # convert to raw image pixels
        pixelX = self.RAW_SURFACE_PIXELS * px / self._zoom
        pixelY = self.RAW_SURFACE_PIXELS * py / self._zoom

        # convert to inches
        return self.transform.convertFrom(Ref.IMAGE_PIXELS, (pixelX, pixelY))
    
    # convert only through scaling for vectors, no offsets
    def mouseToInchesScaleOnly(self, vector: tuple) -> tuple:
        pwidth = self._inverse_pwidth(vector[0])
        pheight = self._inverse_pheight(vector[1])

        # convert to raw image pixels
        pixelWidth = self.RAW_SURFACE_PIXELS * pwidth / self._zoom
        pixelHeight = self.RAW_SURFACE_PIXELS * pheight / self._zoom

        # convert to inches
        return self.transform.scaleFrom(Ref.IMAGE_PIXELS, (pixelWidth, pixelHeight))

    # convert from inches (0-144) to absolute coordinates
    def inchesToMouse(self, inches: tuple) -> tuple:

        # convert to raw image pixels
        pixelX, pixelY = self.transform.convertFrom(Ref.FIELD_INCHES, inches)

        # convert to px (0-1) and py (0-1) for percent position on field
        px = pixelX * self._zoom / self.RAW_SURFACE_PIXELS
        py = pixelY * self._zoom / self.RAW_SURFACE_PIXELS

        # unapply panning
        px += self._panX
        py += self._panY

        # convert to absolute coordinates
        return (self._px(px), self._py(py))
    
    # convert only through scaling for vectors, no offsets
    def inchesToMouseScaleOnly(self, vector: tuple) -> tuple:
        pixelWidth, pixelHeight = self.transform.scaleFrom(Ref.FIELD_INCHES, vector)

        # convert to px (0-1) and py (0-1) for percent position on field
        pwidth = pixelWidth * self._zoom / self.RAW_SURFACE_PIXELS
        pheight = pixelHeight * self._zoom / self.RAW_SURFACE_PIXELS

        return (self._pwidth(pwidth), self._pheight(pheight))
    
    def inBoundsInches(self, inches: tuple) -> bool:
        return isInsideBox(*inches, 0, 0, 144, 144)
    
    def inBoundsPixels(self, pixels: tuple) -> bool:
        return self.inBoundsInches(self.mouseToInches(pixels))
    
    # Add a new node at location
    def onRightClick(self, mousePos: tuple):
        fieldPos = self.mouseToInches(mousePos)
        self.model.addNode(fieldPos)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):
        screen.blit(self.fieldSurface, (self.LEFT_X, self.TOP_Y))
        pass