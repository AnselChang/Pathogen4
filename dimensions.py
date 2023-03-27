import pygame

class Dimensions:

    def __init__(self):

        self.RATIO = 0.7

    # Resize screen to (screenWidth, screenHeight) and return a new instance of the screen with updated dimensions
    def resizeScreen(self, screenWidth: int, screenHeight: int) -> pygame.Surface:

        self.SCREEN_HEIGHT = screenHeight
        self.FIELD_WIDTH = int(screenWidth * self.RATIO)
        self.PANEL_WIDTH = screenWidth - self.FIELD_WIDTH

        larger = max(self.SCREEN_HEIGHT, self.FIELD_WIDTH)

        self.PIXELS_TO_FIELD_CORNER = 19 * (larger / 800) 
        self.FIELD_SIZE_IN_PIXELS = 766 * (larger / 800)
        self.FIELD_SIZE_IN_INCHES = 144

        return pygame.display.set_mode((screenWidth,screenHeight), pygame.RESIZABLE)
