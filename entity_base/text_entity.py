from entity_base.entity import Entity

from common.font_manager import DynamicFont, FontID
from utility.pygame_functions import drawText
from common.draw_order import DrawOrder
import pygame, enum

"""
Draw text at the center of the parent rect, regardless of parent width and height
"""

class TextAlign(enum.Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3

class TextEntity(Entity):
    
    # if align center, then center of text will be aligned with center of parent
    # if not align center, then left of text will be aligned with left of parent
    def __init__(self, parent, fontID: FontID, fontSize: int, staticText: str = None, textFunction = None, align: TextAlign = TextAlign.CENTER, drawOrder = DrawOrder.FRONT):

        # for now, always draw text in the front. can easily make flexible if needed
        super().__init__(parent, drawOrder = drawOrder)

        self.align = align

        self.staticText = staticText
        self.textFunction = textFunction

        self.font: DynamicFont = self.fonts.getDynamicFont(fontID, fontSize)
        self.font.subscribe(onNotify = self.recomputePosition)

        self.recomputePosition()

    
    def getText(self):
        if self.textFunction is not None:
            return self.textFunction()
        elif self.staticText is not None:
            return self.staticText
        return "[no text specified]"
    
    def isTouching(self, mouse: tuple) -> float:
        return False

    # Draw text at the center. opacity set to parent opacity
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        if self.align == TextAlign.CENTER:
            x = self.CENTER_X
            alignX = 0.5
        elif self.align == TextAlign.LEFT:
            x = self.LEFT_X
            alignX = 0
        else:
            x = self.RIGHT_X
            alignX = 1
        drawText(screen, self.font.get(), self.getText(), (0,0,0), x, self.CENTER_Y, opacity = self.getOpacity(), alignX = alignX)
