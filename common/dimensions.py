from data_structures.observer import Observable
import pygame, math

"""
Holds the mutable dimensions information about the window. updates as window resizes
"""

class Dimensions(Observable):

    def __init__(self):

        self.RESIZED_THIS_FRAME = False

        self.RATIO = 0.55

        self.FIELD_SIZE_IN_INCHES = 144
        self.FIELD_MARGIN_IN_PIXELS = 95 # the margin from image (0,0) to (0,0) of the field in pixels

        display_info = pygame.display.Info()

        # I work off my smaller-res mac computer, so I need to keep track of this to not screw with larger resolutions
        self.ANSEL_START_WIDTH = 800
        self.ANSEL_START_HEIGHT = 600

        self.DEFAULT_SCREEN_WIDTH = display_info.current_w
        self.DEFAULT_SCREEN_HEIGHT = display_info.current_h

    def setFieldSizePixels(self, pixels: int):
        self.FIELD_SIZE_IN_PIXELS = pixels
        self.FIELD_SIZE_IN_PIXELS_NO_MARGIN = self.FIELD_SIZE_IN_PIXELS - 2 * self.FIELD_MARGIN_IN_PIXELS

    # Resize screen to (screenWidth, screenHeight) and return a new instance of the screen with updated dimensions
    def resizeScreen(self, screenWidth: int, screenHeight: int) -> pygame.Surface:
        screenWidth = max(screenWidth, int(screenHeight * self.RATIO)*2)
        screenHeight = max(screenHeight, 500)
        

        self.SCREEN_WIDTH = screenWidth
        self.SCREEN_HEIGHT = screenHeight
        self.PANEL_WIDTH = int(screenHeight * self.RATIO)
        self.FIELD_WIDTH = screenWidth - self.PANEL_WIDTH
        self.FIELD_DIAGONAL = math.sqrt(self.FIELD_WIDTH ** 2 + self.SCREEN_HEIGHT ** 2)

        #ratioSquared = (self.SCREEN_WIDTH * self.SCREEN_HEIGHT) / (self.DEFAULT_SCREEN_HEIGHT * self.DEFAULT_SCREEN_WIDTH)
        #self.RESOLUTION_RATIO = math.sqrt(ratioSquared)

        self.X_RATIO = self.SCREEN_WIDTH / self.ANSEL_START_WIDTH
        self.Y_RATIO = self.SCREEN_HEIGHT / self.ANSEL_START_HEIGHT

        self.RESOLUTION_RATIO = min(self.X_RATIO, self.Y_RATIO)


        self.LARGER_FIELD_SIDE = max(self.SCREEN_HEIGHT, self.FIELD_WIDTH)
        self.SMALLER_FIELD_SIDE = min(self.SCREEN_HEIGHT, self.FIELD_WIDTH)

        screen = pygame.display.set_mode((screenWidth,screenHeight), pygame.RESIZABLE)

        self.RESIZED_THIS_FRAME = True

        self.notify()

        return screen
