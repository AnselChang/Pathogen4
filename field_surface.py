from field_transform import FieldTransform
from reference_frame import PointRef
from dimensions import Dimensions
import pygame

"""A class that stores the scaled surface of the vex field, and contains a draw() method to draw it onto the screen.
It implements Draggable, meaning that the mouse can drag the field to pan the screen. This is coupled with FieldTransform,
in that panning the screen will change panning values in FieldTransform and therefore pan every other object on the field.
"""

class FieldSurface:

    def __init__(self, dimensions: Dimensions, fieldTransform: FieldTransform):
        self.dimensions = dimensions
        self.transform = fieldTransform
        self.rawFieldSurface: pygame.Surface = pygame.image.load("Images/squarefield.png")
        self.updateScaledSurface()


    # Whenever the zoom is changed, this function should be called to scale the raw surface into the scaled one
    def updateScaledSurface(self):

        sizePixels = self.dimensions.FIELD_SIZE_IN_PIXELS

        self.scaledFieldSurface: pygame.Surface = pygame.transform.smoothscale(
            self.rawFieldSurface, [sizePixels * self.transform.zoom, sizePixels * self.transform.zoom])

    # Draw the scaled field with the stored pan
    def draw(self, screen: pygame.Surface):
        screen.blit(self.scaledFieldSurface, self.transform.getPan())

    def __str__(self):
        return "FieldSurface with transform: {}".format(self.transform)