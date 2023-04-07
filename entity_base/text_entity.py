from entity_base.entity import Entity

from common.font_manager import DynamicFont, FontID
from utility.pygame_functions import drawText
from common.draw_order import DrawOrder
import pygame

"""
Draw text at the center of the parent rect, regardless of parent width and height
"""

class TextEntity(Entity):
    
    # if align center, then center of text will be aligned with center of parent
    # if not align center, then left of text will be aligned with left of parent
    def __init__(self, parent, fontID: FontID, fontSize: int, staticText: str = None, textFunction = None, isAlignCenter = True):

        # for now, always draw text in the front. can easily make flexible if needed
        super().__init__(parent, drawOrder = DrawOrder.FRONT)

        self.isAlignCenter = isAlignCenter

        self.staticText = staticText
        self.textFunction = textFunction

        self.font: DynamicFont = self.fonts.getDynamicFont(fontID, fontSize)
        self.font.subscribe(onNotify = self.recomputePosition)

        self.recomputePosition()

    def defineCenter(self) -> tuple:
        return self._px(0.5), self._py(0.5)
    
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
        if self.isAlignCenter:
            x = self.CENTER_X
            alignX = 0.5
        else:
            x = self.LEFT_X
            alignX = 0
        drawText(screen, self.font.get(), self.getText(), (0,0,0), x, self.CENTER_Y, opacity = self.getOpacity(), alignX = alignX)
