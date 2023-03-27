from field_transform import FieldTransform
from reference_frame import PointRef
import pygame

"""A class that stores the scaled surface of the vex field, and contains a draw() method to draw it onto the screen.
It implements Draggable, meaning that the mouse can drag the field to pan the screen. This is coupled with FieldTransform,
in that panning the screen will change panning values in FieldTransform and therefore pan every other object on the field.
"""

class FieldSurface():

    def __init__(self, fieldTransform: FieldTransform):
        self.transform = fieldTransform
        self.rawFieldSurface: pygame.Surface = pygame.image.load("Images/squarefield.png")
        self.updateScaledSurface()

        self.startDragX, self.startDragY = None, None # For calculating mouse dragging delta to determine panning amount
        self.startPanX, self.startPanY = None, None

        super().__init__()

    # Whenever the zoom is changed, this function should be called to scale the raw surface into the scaled one
    def updateScaledSurface(self):
        self.scaledFieldSurface: pygame.Surface = pygame.transform.smoothscale(
            self.rawFieldSurface, [Utility.SCREEN_SIZE * self.transform.zoom, Utility.SCREEN_SIZE * self.transform.zoom])


    def checkIfHovering(self, userInput: UserInput) -> bool:
        return True

    
    # Called when the field was just pressed at the start of the drag.
    # Get the current mouse and pan position so that new pan based on changes in mouse position can be calculated
    def startDragging(self, userInput: UserInput):
        self.startDragX, self.startDragY = userInput.mousePosition.screenRef
        self.startPanX, self.startPanY = self.transform.pan

    # Called every frame that the object is being dragged.
    # Compute pan based on mouse position delta
    def beDraggedByMouse(self, userInput: UserInput):

        # Calculate delta in mouse position
        deltaX = userInput.mousePosition.screenRef[0] - self.startDragX
        deltaY = userInput.mousePosition.screenRef[1] - self.startDragY

        self.transform.pan = self.startPanX + deltaX, self.startPanY + deltaY

    # Called when the dragged object was just released
    def stopDragging(self):
        pass

    # Draw the scaled field with the stored pan
    def draw(self, screen: pygame.Surface):
        screen.blit(self.scaledFieldSurface, self.transform.pan)

    def __str__(self):
        return "FieldSurface with transform: {}".format(self.transform)