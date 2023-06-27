from enum import Enum
from common.image_manager import ImageID, ImageManager
from common.dimensions import Dimensions
from entity_base.entity import Entity
from utility.coordinate_transform import CoordinateTransformBuilder
from utility.math_functions import clamp
from utility.pygame_functions import scaleSurface
from data_structures.observer import Observable
import pygame
import weakref

class Ref(Enum):
    IMAGE_PIXELS = 0
    FIELD_INCHES = 1

"""This class is used for storing the field transformations (zooming and panning) relative to the screen, as well as
the image of the field itself.
It bounds the pan and zoom so that the field never leaves the screen, and does so automatically whenever you
change the panning or zooming values through automatic getters and setters.

It is expected only to have a single instance of this class to represent the screen transformation state, and this
object would be used in cases like for PointRef objects to figure out their field and screen reference frame conversions
"""
class FieldEntity(Entity, Observable):

    def __init__(self, parent: Entity):

        super().__init__(parent)

        # At zoom = 1, the image is completely fit to the parent rect,
        # NOT the original resolution of the image.
        # Scaling zoom scales this already-scaled value.
        # zoom is applied from top-left corner of parent rect, and then pan.
        self._zoom = 1 # displayed image dimensions = _zoom * original dimensions
        self._panX, self._panY = (0, 0)

        self.rawSurface = self.images.get(ImageID.FIELD)
        self.RAW_SURFACE_PIXELS = self.rawSurface.get_width()

        self.TOP_LEFT_POS_PIXELS = (65, 58)
        self.BOTTOM_RIGHT_POS_PIXELS = (4947, 4938)
        self.FIELD_SIZE_INCHES = 144

        builder = CoordinateTransformBuilder[Ref](Ref.IMAGE_PIXELS, Ref.FIELD_INCHES)
        builder.defineFirstPoint(self.TOP_LEFT_POS_PIXELS, (0, 0))
        fsi = [self.FIELD_SIZE_INCHES, self.FIELD_SIZE_INCHES]
        builder.defineSecondPoint(self.BOTTOM_RIGHT_POS_PIXELS, fsi)
        self.transform = builder.build()

        self.oldRect = None
    
    def defineLeftX(self) -> float:
        return self._px(0) + self._awidth(self._panX)
    
    def defineTopY(self) -> float:
        return self._py(0) + self._aheight(self._panY)
    
    def defineWidth(self) -> float:
        return self._pwidth(1) * self._zoom
    
    def defineHeight(self) -> float:
        return self._pheight(1) * self._zoom
    
    def defineAfter(self) -> None:
        
        # use cached surface
        if self.RECT == self.oldRect:
            return
        
        self.oldRect = self.RECT
        self.scaledSurface = pygame.transform.smoothscale(self.rawSurface, (self.WIDTH, self.HEIGHT))
        

    def mouseToInches(self, mousePos: tuple) -> tuple:
        px = self._inverse_px(mousePos[0])
        py = self._inverse_py(mousePos[1])

        pixelX = self.RAW_SURFACE_PIXELS * px
        pixelY = self.RAW_SURFACE_PIXELS * py

        return self.transform.convertFrom(Ref.IMAGE_PIXELS, (pixelX, pixelY))

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):
        screen.blit(self.scaledSurface, (self.LEFT_X, self.TOP_Y))