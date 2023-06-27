from common.image_manager import ImageID, ImageManager
from common.dimensions import Dimensions
from entity_base.entity import Entity
from utility.math_functions import clamp
from utility.pygame_functions import scaleSurface
from data_structures.observer import Observable
import pygame
import weakref


"""This class is used for storing the field transformations (zooming and panning) relative to the screen, as well as
the image of the field itself.
It bounds the pan and zoom so that the field never leaves the screen, and does so automatically whenever you
change the panning or zooming values through automatic getters and setters.

It is expected only to have a single instance of this class to represent the screen transformation state, and this
object would be used in cases like for PointRef objects to figure out their field and screen reference frame conversions
"""
class FieldTransform(Entity, Observable):

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

        self.FIELD_SIZE_INCHES = 144
        self.MARGIN_PIXELS = 12 # raw pixels from top left to (0", 0") for field ref
        self.ACTIVE_FIELD_PIXELS = self.RAW_SURFACE_PIXELS - 2 * self.MARGIN_PIXELS

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
        scaled = pygame.transform.smoothscale(self.rawSurface, (self.WIDTH, self.HEIGHT))
        self.scaledSurface = pygame.Surface((self._pwidth(1), self._pheight(1)))
        self.scaledSurface.blit(scaled, (self._awidth(self._panX), self._aheight(self._panY)))
    
    def _fieldToScreenX(self, x: float) -> float:
        x = self._px(0) # left edge of container
        x += self._awidth(self._panX) # add pan
        x += self._zoom * self.MARGIN_PIXELS # add margin
        x += self._zoom * (self.ACTIVE_FIELD_PIXELS / self.FIELD_SIZE_INCHES) * x # add x
        return x
    
    def _fieldToScreenY(self, y: float) -> float:
        y = self._py(0) # top edge of container
        y += self._aheight(self._panY) # add pan
        y += self._zoom * self.MARGIN_PIXELS # add margin
        y += self._zoom * (self.ACTIVE_FIELD_PIXELS / self.FIELD_SIZE_INCHES) * y # add y
        return y
    
    # Draw the scaled field with the stored pan
    def draw(self, screen: pygame.Surface):
        screen.blit(self.scaledSurface, (self.LEFT_X, self.TOP_Y))

    def __str__(self):
        return "FieldTransform object\nzoom: {}\npan: ({},{})".format(self._zoom, self._panX, self._panY)

# Testing code
if __name__ == "__main__":
    f = FieldTransform()
    print(f)
    f._zoom = 4
    f.pan = -10000, 1000
    print(f)