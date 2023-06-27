from enum import Enum
from common.image_manager import ImageID, ImageManager
from common.dimensions import Dimensions
from entity_base.entity import Entity
from entity_base.listeners.mousewheel_listener import MousewheelLambda
from utility.coordinate_transform import CoordinateTransformBuilder
from utility.math_functions import clamp
from utility.pygame_functions import scaleSurface
from data_structures.observer import Observable
import pygame
import weakref

class Ref(Enum):
    IMAGE_PIXELS = 0
    FIELD_INCHES = 1

"""
Draws the background field image and handles logic for panning and zooming
"""
class FieldEntity(Entity, Observable):

    def __init__(self, parent: Entity):

        super().__init__(parent,
            mousewheel = MousewheelLambda(self, FonMousewheel = self.onMousewheel)
        )

        # At zoom = 1, the image is completely fit to the parent rect,
        # NOT the original resolution of the image.
        # Scaling zoom scales this already-scaled value.
        # zoom is applied from top-left corner of parent rect, and then pan.
        self._zoom = 1
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

    def onMousewheel(self, offset: int) -> bool:
        P_ZOOM = 0.01
        MIN_ZOOM = 1
        MAX_ZOOM = 3

        self._zoom += offset * P_ZOOM
        self._zoom = clamp(self._zoom, MIN_ZOOM, MAX_ZOOM)
        self.recomputeEntity()
        print(self._zoom)
        return True

    # recompute scaled surface if change in scale
    def defineAfter(self) -> None:
        
        # use cached surface
        if self.RECT == self._oldRect:
            if self._zoom == self._oldZoom:
                return
        
        self._oldRect = self.RECT
        self._oldZoom = self._zoom

        size = self.WIDTH * self._zoom
        scaledSurface = pygame.transform.smoothscale(self.rawSurface, (size, size))
        self.fieldSurface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.fieldSurface.blit(scaledSurface, (0,0))
        
    # convert from absolute coordinates to position on field in inches (0-144)
    def mouseToInches(self, mousePos: tuple) -> tuple:
        # get px (0-1) and py (0-1) for percent position on field
        px = self._inverse_px(mousePos[0])
        py = self._inverse_py(mousePos[1])

        # convert to raw image pixels
        pixelX = self.RAW_SURFACE_PIXELS * px / self._zoom
        pixelY = self.RAW_SURFACE_PIXELS * py / self._zoom

        # convert to inches
        return self.transform.convertFrom(Ref.IMAGE_PIXELS, (pixelX, pixelY))

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):
        screen.blit(self.fieldSurface, (self.LEFT_X, self.TOP_Y))