from data_structures.observer import Observer
from entity_base.entity import Entity

from common.font_manager import DynamicFont, FontID
from entity_base.listeners.click_listener import ClickLambda
from utility.pygame_functions import drawText, getText
from common.draw_order import DrawOrder
import pygame, enum

"""
Draw text at the center of the parent rect, regardless of parent width and height
"""

class TextAlign(enum.Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3

class TextEntity(Entity, Observer):
    
    # if align center, then center of text will be aligned with center of parent
    # if not align center, then left of text will be aligned with left of parent
    def __init__(self, parent, fontID: FontID, fontSize: int, staticText: str = None,
                 textFunction = None, align: TextAlign = TextAlign.CENTER,
                 drawOrder = DrawOrder.FRONT, onClick = lambda mouse: None,
                 dx = 0, dy = 0
                 ):

        # for now, always draw text in the front. can easily make flexible if needed
        super().__init__(parent,
                         click = ClickLambda(self, FonLeftClick = onClick),
                         drawOrder = drawOrder)

        self.align = align
        self.dx, self.dy = dx, dy

        self.staticText = staticText
        self.textFunction = textFunction

        self.font: DynamicFont = self.fonts.getDynamicFont(fontID, fontSize)
        self.font.subscribe(self, onNotify = self.recomputePosition)


    def defineAfter(self):
        self.surface = getText(self.font.get(), self.getText(), (0,0,0), 1)

    def getTextWidth(self):
        return self.surface.get_width()
    
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

        x += self._awidth(self.dx)
        y = self.CENTER_Y + self._aheight(self.dy)

        drawText(screen, self.font.get(), self.getText(), (0,0,0), x, y, opacity = self.getOpacity(), alignX = alignX)
