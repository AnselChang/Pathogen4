from entity_base.entity import Entity

from data_structures.observer import Observable, Observer
from entity_base.listeners.hover_listener import HoverLambda

from entity_ui.text.text_handler import TextHandler
from entity_ui.text.text_border import TextBorder

from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.key_listener import KeyLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType

from common.font_manager import DynamicFont, FontID
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

# propagates change whenever resized from text (isDynamic)
# sends notification whenever change in text
class TextEditorEntity(Entity, Observer, Observable):

    def __init__(self, parent: Entity,
                 fontID: FontID,
                 fontSize: int,
                 isDynamic: bool = False,
                 isNumOnly: bool = False,
                 isCentered: bool = True,
                 isFixedWidth: bool = False,
                 defaultText: str = "",
                 hideTextbox: bool = False,
                 borderThicknessRead: int = 2,
                 borderThicknessWrite: int = 2,
                 readColor = (196, 219, 250),
                 readColorH = (176, 200, 250),
                 writeColor = (239, 226, 174),
                 writeColorH = (239, 226, 174),
                 maxTextLength: int | None = None,
                 ):
        
        super().__init__(parent, 
            key = KeyLambda(self,
                FonKeyDown = self.onKeyDown,
                FonKeyUp = self.onKeyUp
            ),
            select = SelectLambda(self, "text editor", type = SelectorType.SOLO, greedy = True,
                FonSelect = self.onSelect,
                FonDeselect = self.onDeselect
            ),
            hover = HoverLambda(self))
        self.font = self.fonts.getDynamicFont(fontID, fontSize)
        
        self.dynamic = isDynamic # whether to grow vertically
        self.numOnly = isNumOnly # whether to only allow numbers
        self.centered = isCentered # whether to center text
        self.fixedWidth = isFixedWidth # whether to grow horizontally
        self.hideTextbox = hideTextbox # whether to hide the textbox when not hovered/selected
        self.maxTextLength = maxTextLength # maximum length of text

        self.border = TextBorder()
        self.borderThickness: dict[TextEditorMode, int] = {
            TextEditorMode.READ : borderThicknessRead,
            TextEditorMode.WRITE : borderThicknessWrite
        }

        self.rows = 1

        self.textHandler = TextHandler(self, defaultText = defaultText)
        self.cursorBlink = CursorBlink(35, 33)

        self.mode: TextEditorMode = TextEditorMode.READ

        self.backgroundColor: dict[TextEditorMode, tuple] = {
            TextEditorMode.WRITE : {
                True: writeColorH,
                False: writeColor
            },
            TextEditorMode.READ : {
                True: readColorH,
                False: readColor
            }
        }



    def onFontUpdate(self):
        self.textHandler.update()
        self.recomputeEntity()

    def setRows(self, rows):
        self.rows = rows
        self.recomputeEntity()

    def addRow(self):
        self.setRows(self.rows + 1)

    def removeRow(self):
        self.setRows(self.rows - 1)

    def defineCenterY(self) -> tuple:
        return self._py(0.5)
    
    def defineCenterX(self) -> tuple:
        if self.centered:
            return self._px(0.5)
        return None
        
    def defineLeftX(self) -> tuple:
        if not self.centered:
            return self._px(0)
        return None

    def defineWidth(self) -> float:
        if self.fixedWidth:
            return self._pwidth(1)
        else:
            return self.textHandler.getSurfaceWidth() + self._awidth(self.border.OUTER_X_MARGIN * 2)
    
    def defineHeight(self) -> float:
        return self.getHeightForNumRows(self.rows)
    
    def getHeightForNumRows(self, rows: int):
        charHeight = self.font.getCharHeight()
        height = rows * (charHeight + self.border.INNER_Y_MARGIN)
        height += self._aheight(2 * self.border.OUTER_Y_MARGIN - self.border.INNER_Y_MARGIN)
        return height
    
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

        leftX, topY, width, height = self.RECT
        surf = pygame.Surface((width, height))
        
        # draw background
        if not self.hideTextbox or self.mode == TextEditorMode.WRITE or isHovered:    
            pygame.draw.rect(surf, self.backgroundColor[self.mode][isHovered], [0,0,width,height], border_radius = self.border.BORDER_RADIUS)
            
            bt = self.borderThickness[self.mode]
            if bt > 0:
                pygame.draw.rect(surf, (0,0,0), [0,0,width,height], width = bt, border_radius = self.border.BORDER_RADIUS)
        
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
            y = outerYMargin + cy * (charHeight + innerYMargin)
            pygame.draw.rect(surf, (0,0,0), (x, y, 1, charHeight))

        screen.blit(surf, (leftX, topY))

    def onKeyDown(self, key):

        # only useful when in write mode
        if self.mode == TextEditorMode.READ:
            return
        
        print(key)
        
        oldHeight = self.defineHeight()
        oldText = self.getText()

        self.textHandler.onKeyDown(key)
        # notify observers on text change
        if self.getText() != oldText:
            self.notify()

        self.recomputeEntity()

    def onKeyUp(self, key):
        pass

    def onSelect(self, interactor):
        self.setMode(TextEditorMode.WRITE)

    def onDeselect(self, interactor):
        self.setMode(TextEditorMode.READ)

    def setMode(self, mode: TextEditorMode):
        self.mode = mode
        self.recomputeEntity()