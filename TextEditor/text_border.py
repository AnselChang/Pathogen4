"""
Handles drawing the border around text
Defines the standardized constants for margins
"""

class TextBorder:

    def __init__(self):
        self.BORDER_RADIUS = 3
        self.OUTER_X_MARGIN = 6
        self.OUTER_Y_MARGIN = 4
        self.INNER_Y_MARGIN = 0

    def getBorderWidth(self, textWidth):
        return textWidth + self.OUTER_X_MARGIN * 2
    
    def getBorderHeight(self, textHeight):
        return textHeight + self.OUTER_Y_MARGIN * 2
    
    def getTextWidth(self, borderWidth):
        return borderWidth - self.OUTER_X_MARGIN * 2
    
    def getRect(self, centerX, centerY, textWidth, textHeight):
        width = self.getBorderWidth(textWidth)
        height = self.getBorderHeight(textHeight)
        x = int(round(centerX - width / 2))
        y = int(round(centerY - height / 2))
        return x, y, width, height