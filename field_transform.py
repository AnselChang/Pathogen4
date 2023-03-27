from dimensions import Dimensions
from math_functions import clamp

"""This class is used for storing the field transformations (zooming and panning) relative to the screen, as well as
the image of the field itself.
It bounds the pan and zoom so that the field never leaves the screen, and does so automatically whenever you
change the panning or zooming values through automatic getters and setters.

It is expected only to have a single instance of this class to represent the screen transformation state, and this
object would be used in cases like for PointRef objects to figure out their field and screen reference frame conversions

To use, simply assign new values to pan and zoom as they have been overloaded:
    f = FieldTransform
    f.pan = (15, 25) -> for (panX, panY)
    f.zoom = 3.5 -> gets clamped back to 3
"""
class FieldTransform:

    def __init__(self, dimensions: Dimensions, fieldZoom: float = 1, xyFieldPanInPixels: tuple = (0,0)):
        self._dimensions = dimensions
        self._zoom = fieldZoom
        self._panX, self._panY = xyFieldPanInPixels

    # Restrict the panning range for the field as to keep the field in sight of the screen
    def _boundFieldPan(self):
        minPanX = (1-self._zoom) * self._dimensions.fieldWidth
        minPanY = (1-self._zoom) * self._dimensions.screenHeight
        self._panX = clamp(self._panX, minPanX, 0)
        self._panY = clamp(self._panY, minPanY, 0)

    # A setter function for self.zoom, which bounds zoom and pan after zoom is updated to keep the field in sight of hte screen
    def _getZoom(self):
        return self._zoom

    def _setZoom(self, fieldZoom: float):
        self._zoom = clamp(fieldZoom, 1, 3) # limits to how much you can zoom in or out
        self._boundFieldPan()

    # self.zoom property that is gettable and settable
    zoom = property(_getZoom, _setZoom)

    def _getPan(self):
        return self._panX, self._panY

    # After updating the field pan, make sure it is in bounds
    def _setPan(self, xyFieldPanInPixels: tuple):
        self._panX, self._panY = xyFieldPanInPixels
        self._boundFieldPan()

    # self.pan property that is gettable and settable
    pan = property(_getPan, _setPan)

    # Return the zoom multiplied by a scalar. The most common use case is for determining the size of objects, so that
    # objects grow when zooming in, but at a slower rate than the zoom (when 0 < scalar < 1)
    def getPartialZoom(self, scalar):
        return (self.zoom - 1) * scalar + 1

    def __str__(self):
        return "FieldTransform object\nzoom: {}\npan: ({},{})".format(self._zoom, self._panX, self._panY)

# Testing code
if __name__ == "__main__":
    f = FieldTransform()
    print(f)
    f.zoom = 4
    f.pan = -10000, 1000
    print(f)