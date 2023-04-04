from Observers.observer import Observer, Observable
from dimensions import Dimensions
from math_functions import clamp
import pygame
from enum import Enum, auto

class FontID(Enum):
    FONT_NORMAL = auto()
    FONT_CODE = auto()

_fontPaths: dict[FontID, str] = {
    FontID.FONT_NORMAL : 'CascadiaCode.ttf',
    FontID.FONT_CODE : 'CascadiaMono.ttf'
}

# A font class which changes size based on the window resolution
# subscribes to dimensions, which notifies on window rescale
class DynamicFont(Observable):
    def __init__(self, dimensions: Dimensions, fontSizes: dict[int, pygame.font.Font], widths: dict[int, float], heights: dict[int, float], smallest: int, largest: int, baseFontSize: float):
        self._dimensions = dimensions
        self._fontSizes = fontSizes
        self._widths = widths
        self._heights = heights
        self._smallest = smallest
        self._largest = largest
        self._baseFontSize = baseFontSize

        # Subscribe to window changes
        self._dimensions.subscribe(Observer(onNotify = self.update)) 

        # Calculate initial font size
        self.update()

    # Get the font for the given window resolution ratio
    def get(self) -> pygame.font.Font:
        return self._currentFont
    
    def getCharWidth(self) -> float:
        return self._widths[self.size]
    
    def getCharHeight(self) -> float:
        return self._heights[self.size]

    # update font size based from dimensions resolution
    def update(self):
        self.size = int(round(self._baseFontSize * self._dimensions.RESOLUTION_RATIO))
        self._currentFont = self._getFontFromSize(self.size)
        self.notify()
    
    def _getFontFromSize(self, fontSize: int) -> pygame.font.Font:
        fontSize = clamp(fontSize, self._smallest, self._largest)
        return self._fontSizes[fontSize]

class FontManager:

    def __init__(self, dimensions: Dimensions):
        pygame.font.init()

        self.dimensions = dimensions

        self.SMALLEST_SUPPORTED_FONT = 1
        self.LARGEST_SUPPORTED_FONT = 50

        self.allFontSizes: dict[FontID, dict[int, pygame.font.Font]] = {}
        for fontID in FontID:
            self.allFontSizes[fontID] = self._generateFontSizes(fontID, self.SMALLEST_SUPPORTED_FONT, self.LARGEST_SUPPORTED_FONT)
    
        self.allFontWidths: dict[FontID, dict[int, float]] = {}
        self.allFontHeights: dict[FontID, dict[int, float]] = {}
        for fontID in FontID:
            self.allFontWidths[fontID], self.allFontHeights[fontID] = self._getFontDimensions(fontID)
            

    def _getFontDimensions(self, fontID):
        widths: dict[int, float] = {}
        heights: dict[int, float] = {}

        fontSizes = self.allFontSizes[fontID]
        for fontSize in fontSizes:
            font = self.allFontSizes[fontID][fontSize]
            charSurface = font.render("T", True, (0,0,0))

            widths[fontSize] = charSurface.get_width()
            heights[fontSize] = charSurface.get_height()
        return widths, heights


    def _generateFontSizes(self, font: FontID, smallest: int, biggest: int) -> dict[int, pygame.font.Font]:

        fontPath = _fontPaths[font]

        fonts: dict[int, pygame.font.Font] = {}
        for i in range(smallest, biggest+1):
            fonts[i] = pygame.font.Font(fontPath, i)

        return fonts
    
    def getDynamicFont(self, fontID: FontID, baseFontSize: float) -> DynamicFont:
        return DynamicFont(
            self.dimensions,
            self.allFontSizes[fontID],
            self.allFontWidths[fontID],
            self.allFontHeights[fontID],
            self.SMALLEST_SUPPORTED_FONT,
            self.LARGEST_SUPPORTED_FONT,
            baseFontSize
        )