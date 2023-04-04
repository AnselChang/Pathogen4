from dimensions import Dimensions

"""
Handles drawing the border around text
Defines the standardized constants for margins
"""

class TextBorder:

    def __init__(self, dimensions: Dimensions):

        self.dimensions = dimensions

        self.BORDER_RADIUS = 3
        self._OUTER_X_MARGIN = 6
        self._OUTER_Y_MARGIN = 4
        self._INNER_Y_MARGIN = 0

    def getOuterXMargin(self):
        return int(round(self._OUTER_X_MARGIN * self.dimensions.RESOLUTION_RATIO))
    
    def getOuterYMargin(self):
        return int(round(self._OUTER_Y_MARGIN * self.dimensions.RESOLUTION_RATIO))
    
    def getInnerYMargin(self):
        return int(round(self._INNER_Y_MARGIN * self.dimensions.RESOLUTION_RATIO))

    def getBorderWidth(self, textWidth):
        return textWidth + self.getOuterXMargin() * 2
    
    def getBorderHeight(self, textHeight):
        return textHeight + self.getOuterXMargin() * 2
    
    def getTextWidth(self, borderWidth):
        return borderWidth - self.getOuterXMargin() * 2
    
    def getRect(self, centerX, centerY, textWidth, textHeight):
        width = self.getBorderWidth(textWidth)
        height = self.getBorderHeight(textHeight)
        x = int(round(centerX - width / 2))
        y = int(round(centerY - height / 2))
        return x, y, width, height