from Observers.observer import Observable
import pygame

"""
Holds the mutable dimensions information about the window. updates as window resizes
"""

class Dimensions(Observable):

    def __init__(self):

        self.RATIO = 0.7

        self.FIELD_SIZE_IN_INCHES = 147.8377757

    def setFieldSizePixels(self, pixels: int, margin: int):
        self.FIELD_SIZE_IN_PIXELS = pixels
        self.PIXELS_TO_FIELD_CORNER = margin
        self.FIELD_SIZE_IN_PIXELS_NO_MARGIN = self.FIELD_SIZE_IN_PIXELS - 2 * margin

    # Resize screen to (screenWidth, screenHeight) and return a new instance of the screen with updated dimensions
    def resizeScreen(self, screenWidth: int, screenHeight: int) -> pygame.Surface:

        self.SCREEN_HEIGHT = screenHeight
        self.FIELD_WIDTH = int(screenWidth * self.RATIO)
        self.PANEL_WIDTH = screenWidth - self.FIELD_WIDTH

        larger = max(self.SCREEN_HEIGHT, self.FIELD_WIDTH)
        self.LARGER_FIELD_SIDE = larger

        screen = pygame.display.set_mode((screenWidth,screenHeight), pygame.RESIZABLE)
        self.notify()

        return screen
