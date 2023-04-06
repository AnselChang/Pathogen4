from common.image_manager import ImageID, ImageManager
from common.dimensions import Dimensions
from utility.math_functions import clamp
from utility.pygame_functions import scaleSurface
import pygame
import weakref


"""This class is used for storing the field transformations (zooming and panning) relative to the screen, as well as
the image of the field itself.
It bounds the pan and zoom so that the field never leaves the screen, and does so automatically whenever you
change the panning or zooming values through automatic getters and setters.

It is expected only to have a single instance of this class to represent the screen transformation state, and this
object would be used in cases like for PointRef objects to figure out their field and screen reference frame conversions
"""
class FieldTransform:

    def __init__(self, images: ImageManager, dimensions: Dimensions, fieldZoom: float = 1, xyFieldPanInPixels: tuple = (0,0)):

        self.pointsAndVectors: list = weakref.WeakSet()

        self._images = images
        self._dimensions = dimensions
        self.zoom = fieldZoom
        self._panX, self._panY = xyFieldPanInPixels

        self.rawSize = self._images.get(ImageID.FIELD).get_width()

        self.resizeScreen()

    def recalculatePointsAndVectors(self):
        pass

    def resizeScreen(self):

        self.zoom = self._dimensions.LARGER_FIELD_SIDE / self.rawSize
        self.updateScaledSurface()
        self._boundFieldPan()
        self.recalculatePointsAndVectors()

    # Whenever the zoom is changed, this function should be called to scale the raw surface into the scaled one
    def updateScaledSurface(self):
        rawImage = self._images.get(ImageID.FIELD)
        self.size = self.rawSize * self.zoom
        self.scaledFieldSurface = scaleSurface(rawImage, self.zoom)

    # Restrict the panning range for the field as to keep the field in sight of the screen
    def _boundFieldPan(self):

        MARGIN = 0

        minPanX = self._dimensions.FIELD_WIDTH - self.size
        minPanY = self._dimensions.SCREEN_HEIGHT - self.size
        self._panX = clamp(self._panX, minPanX - MARGIN, MARGIN)
        self._panY = clamp(self._panY, minPanY - MARGIN, MARGIN)

    # mouse is a PointRef
    def changeZoom(self, mouse, deltaZoom: float):
        oldX, oldY = mouse.screenRef

        #self.zoom = clamp(self.zoom + deltaZoom, 0.5, 5) # limits to how much you can zoom in or out
        self.zoom = self.zoom + deltaZoom

        MAX_ZOOM = 5 # can only do [MAX_ZOOM]x zoom from when the image is scaled to fit screen
        self.zoom = min(self.zoom, MAX_ZOOM * self._dimensions.LARGER_FIELD_SIDE / self._dimensions.FIELD_SIZE_IN_PIXELS)

        # can't zoom more than the width of the screen
        if self._dimensions.LARGER_FIELD_SIDE > self.rawSize * self.zoom:
            self.zoom = self._dimensions.LARGER_FIELD_SIDE / self.rawSize

        newX, newY = mouse.screenRef

        # compensate pan for zooming to maintain zoom center at mouse pointer
        self._panX += oldX - newX
        self._panY += oldY - newY

        self.updateScaledSurface()
        self._boundFieldPan()
        self.recalculatePointsAndVectors()

    def getPan(self) -> tuple:
        return self._panX, self._panY
    
    def startPan(self):
        self.startX, self.startY = self.getPan()

    def updatePan(self, offsetX, offsetY): # offset is a vectorRef

        self._panX = self.startX + offsetX
        self._panY = self.startY + offsetY

        self._boundFieldPan()
        self.recalculatePointsAndVectors()

    # Return the zoom multiplied by a scalar. The most common use case is for determining the size of objects, so that
    # objects grow when zooming in, but at a slower rate than the zoom (when 0 < scalar < 1)
    def getPartialZoom(self, scalar):
        return (self.zoom - 1) * scalar + 1
    
    # Draw the scaled field with the stored pan
    def draw(self, screen: pygame.Surface):
        screen.blit(self.scaledFieldSurface, self.getPan())

    def __str__(self):
        return "FieldTransform object\nzoom: {}\npan: ({},{})".format(self._zoom, self._panX, self._panY)

# Testing code
if __name__ == "__main__":
    f = FieldTransform()
    print(f)
    f.zoom = 4
    f.pan = -10000, 1000
    print(f)