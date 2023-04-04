from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.key_listener import KeyLambda
from BaseEntity.EntityListeners.select_listener import SelectLambda, SelectorType

from Observers.observer import Observable

from TextEditor.text_handler import TextHandler
from TextEditor.text_border import TextBorder

from reference_frame import PointRef, Ref
from pygame_functions import drawText, FONTCODE, drawTransparentRect
from math_functions import isInsideBox2
from draw_order import DrawOrder

from enum import Enum, auto
from abc import abstractmethod
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
class TextEditor(Observable):

    def setRows(self, rows):
        self.height = 2 * self.border.OUTER_Y_MARGIN + rows * (self.charHeight + self.border.INNER_Y_MARGIN) - self.border.INNER_Y_MARGIN
        self.rows = rows
        self.notify()

    def addRow(self):
        self.setRows(self.rows + 1)

    def removeRow(self):
        self.setRows(self.rows - 1)

    def __init__(self, font, xFunc: int, yFunc: int, widthFuncOrIntOrNone, rows: int, readColor: tuple, writeColor: tuple, isDynamic: bool = False, isNumOnly: bool = False, defaultText: str = ""):
        
        self.rawXFunc = xFunc

        self.noWidthRestriction = widthFuncOrIntOrNone is None

        if self.noWidthRestriction:
            self.getX = self.getDynamicX
        else:
            self.getX = xFunc

        self.getY = yFunc
        if type(widthFuncOrIntOrNone) == int:
            self.getWidth = lambda widthFuncOrInt=widthFuncOrIntOrNone: widthFuncOrInt
        elif self.noWidthRestriction:
            self.getWidth = self.getDynamicWidth
        else:
            self.getWidth = widthFuncOrIntOrNone
        self.dynamic = isDynamic
        self.numOnly = isNumOnly

        self.border = TextBorder()

        self.font = font
        test = self.font.render("T", True, (0,0,0))
        self.charWidth = test.get_width()
        self.charHeight = test.get_height()

        self.setRows(rows)
        self.originalHeight = self.height # so that original position can be maintained if height changes

        self.textHandler = TextHandler(self, defaultText = defaultText)
        self.cursorBlink = CursorBlink(35, 33)

        self.mode: TextEditorMode = TextEditorMode.READ

        self.backgroundColor: dict[TextEditorMode, tuple] = {
            TextEditorMode.READ : readColor,
            TextEditorMode.WRITE : writeColor
        }

    def getDynamicX(self) -> float:
        # bruh why does this work
        return self.rawXFunc()# - self.getDynamicWidth() / 2
        
    
    def getDynamicWidth(self) -> float:
        return self.border.getBorderWidth(self.textHandler.getSurfaceWidth())
    
    def getHeight(self) -> float:
        return self.height

    def getMaxTextWidth(self) -> float:
        return self.border.getTextWidth(self.getWidth())
    
    def getMaxTextLines(self) -> int:
        return (self.getHeight() - 2*self.border.OUTER_Y_MARGIN + self.border.INNER_Y_MARGIN) // (self.charHeight + self.border.INNER_Y_MARGIN)

    def getRect(self) -> tuple:
        return self.getX(), self.getY(), self.getWidth(), self.getHeight()
    
    def getText(self) -> str:
        return self.textHandler.getText()


    def isTouching(self, position: PointRef) -> bool:
        return isInsideBox2(*position.screenRef, self.getX(), self.getY(), self.getWidth(), self.getHeight())
    
    def getPosition(self) -> PointRef:
        x = self.getDynamicX()
        y = self.getY() + self.getHeight() / 2
        return PointRef(Ref.SCREEN, (x,y))

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool, opacity: float = 1) -> bool:
        
        # draw background
        rect = self.getRect()
        absoluteX, absoluteY, width, height = rect

        surf = pygame.Surface((width, height))
        
        pygame.draw.rect(surf, self.backgroundColor[self.mode], [0,0,width,height], border_radius = self.border.BORDER_RADIUS)
        pygame.draw.rect(surf, (0,0,0), [0,0,width,height], width = 2, border_radius = self.border.BORDER_RADIUS)
        surf.set_alpha(opacity * 255)

        # draw text
        x = self.border.OUTER_X_MARGIN
        y = self.border.OUTER_Y_MARGIN
        for surface in self.textHandler.getSurfaces():
            surf.blit(surface, (x,y))
            y += self.charHeight + self.border.INNER_Y_MARGIN

        # draw blinkingcursor
        if self.mode == TextEditorMode.WRITE and self.cursorBlink.get():
            cx, cy = self.textHandler.getCursor()
            x = self.border.OUTER_X_MARGIN + cx * self.charWidth
            y = self.border.OUTER_Y_MARGIN + cy * (self.charHeight + self.border.INNER_Y_MARGIN)
            pygame.draw.rect(surf, (0,0,0), (x, y, 1, self.charHeight))

        screen.blit(surf, (absoluteX, absoluteY))


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

    