from entity_base.entity import Entity

from data_structures.observer import Observable

from entity_ui.text.text_handler import TextHandler
from entity_ui.text.text_border import TextBorder

from common.font_manager import DynamicFont
from utility.math_functions import isInsideBox2
from common.draw_order import DrawOrder

from enum import Enum, auto
import pygame

"""
Functionality for a text editor. Not an entity
"""

class TextEditorMode(Enum):
    READ = auto()
    WRITE = auto()

class CursorBlink:
    def __init__(self, numOn: int, numOff: int):
        self.i = 0
        self.numOn = numOn
        self.numOff = numOff

    def get(self) -> bool:
        self.i += 1
        self.i %= self.numOn + self.numOff

        return self.i < self.numOn

# notifies observers whenever resized from text (isDynamic)
class TextEditorEntity(Entity, Observable):

    def __init__(self, font: DynamicFont, px: float, py: float, getOpacity = lambda: 1, isDynamic: bool = False, isNumOnly: bool = False, defaultText: str = ""):
        
        super().__init__(drawOrder = DrawOrder.WIDGET)

        self.font = font
        self.px, self.py = px, py
        
        self.getOpacity = getOpacity

        self.dynamic = isDynamic
        self.numOnly = isNumOnly

        self.border = TextBorder()

        self.rows = 1
        self.font.subscribe(Observable(onNotify = self.onFontUpdate))
        self.dimensions.subscribe(onNotify = self.recomputePosition)

        self.textHandler = TextHandler(self, defaultText = defaultText)
        self.cursorBlink = CursorBlink(35, 33)

        self.mode: TextEditorMode = TextEditorMode.READ

        self.backgroundColor: dict[TextEditorMode, tuple] = {
            TextEditorMode.READ : (239, 226, 174),
            TextEditorMode.WRITE : (174, 198, 239)
        }

        self.recomputePosition()

    def recomputePosition(self):
        super().recomputePosition()
        self.notify()

    def onFontUpdate(self):
        self.textHandler.update()
        self.recomputePosition()

    def setRows(self, rows):
        self.rows = rows
        self.recomputePosition()

    def addRow(self):
        self.setRows(self.rows + 1)

    def removeRow(self):
        self.setRows(self.rows - 1)

    def defineCenter(self) -> tuple:
        return self._px(self.px), self._py(self.py)

    def defineWidth(self) -> float:
        return self._awidth(self.textHandler.getSurfaceWidth() + self.border.OUTER_X_MARGIN * 2)
    
    def defineHeight(self) -> float:
        return self.getHeightForNumRows(self.rows)
    
    def getHeightForNumRows(self, rows: int):
        charHeight = self.font.getCharHeight()
        height = rows * (charHeight + self.border.INNER_Y_MARGIN)
        height += 2 * self.border.OUTER_Y_MARGIN - self.border.INNER_Y_MARGIN
        return self._aheight(height)
    
    # Get height offset from current height to one row height
    def getHeightOffset(self) -> float:
        return self.getHeightForNumRows(self.rows) - self.getHeightForNumRows(1)

    def getText(self) -> str:
        return self.textHandler.getText()

    def isTouching(self, position: tuple) -> bool:
        return isInsideBox2(*position, *self.RECT)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        outerXMargin = self._awidth(self.border.OUTER_X_MARGIN)
        outerYMargin = self._aheight(self.border.OUTER_Y_MARGIN)
        innerYMargin = self._aheight(self.border.INNER_Y_MARGIN)

        # draw background
        leftX, topY, width, height = self.RECT

        surf = pygame.Surface((width, height))
        
        pygame.draw.rect(surf, self.backgroundColor[self.mode], [0,0,width,height], border_radius = self.border.BORDER_RADIUS)
        pygame.draw.rect(surf, (0,0,0), [0,0,width,height], width = 2, border_radius = self.border.BORDER_RADIUS)
        surf.set_alpha(self.getOpacity() * 255)

        # draw text
        x = outerXMargin
        y = outerYMargin
        for surface in self.textHandler.getSurfaces():
            surf.blit(surface, (x,y))
            y += self.font.getCharHeight() + innerYMargin

        # draw blinkingcursor
        if self.mode == TextEditorMode.WRITE and self.cursorBlink.get():
            cx, cy = self.textHandler.getCursor()
            charWidth, charHeight = self.font.getCharWidth(), self.font.getCharHeight()
            x = outerXMargin + cx * charWidth
            y = outerYMargin + cy * (charHeight + outerYMargin)
            pygame.draw.rect(surf, (0,0,0), (x, y, 1, charHeight))

        screen.blit(surf, (leftX, topY))

    def onKeyDown(self, key):

        # only useful when in write mode
        if self.mode == TextEditorMode.READ:
            return
        
        self.textHandler.onKeyDown(key)

    def onKeyUp(self, key):
        pass

    def onSelect(self, interactor):
        self.setMode(TextEditorMode.WRITE)

    def onDeselect(self, interactor):
        self.setMode(TextEditorMode.READ)

    def setMode(self, mode: TextEditorMode):
        self.mode = mode