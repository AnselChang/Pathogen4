from BaseEntity.entity import Entity
from Adapters.path_adapter import PathAdapter

from TextEditor.text_border import TextBorder

from reference_frame import PointRef, Ref
from draw_order import DrawOrder
from pygame_functions import drawText, drawTransparentRect, getText
from font_manager import DynamicFont, FontID
import pygame

"""
Belongs to a specific CommandBlockEntity.
Owns a DefinedReadout which stores information about the widget's context for all commands of that type
"""

class ReadoutEntity(Entity):
    def __init__(self, parentCommand: Entity, pathAdapter: PathAdapter, definedReadout):

        super().__init__(drawOrder = DrawOrder.READOUT)

        self.border = TextBorder()

        self.font: DynamicFont = parentCommand.fontManager.getDynamicFont(FontID.FONT_NORMAL, 15)
        self.font.subscribe(onNotify = self.recomputePosition)

        self.parentCommand = parentCommand
        self.definedReadout = definedReadout
        self.pathAdapter = pathAdapter
        self.pathAdapter.subscribe(onNotify = self.updateText)

    def updateText(self) -> str:
        self.textString = str(self.pathAdapter.getString(self.definedReadout.getAttribute()))
        textSurface = getText(self.font.get(), self.textString, (0,0,0), 1)
        self.textWidth = textSurface.get_width()
        self.textHeight = textSurface.get_height()
        self.recomputePosition()
    
    def isVisible(self) -> bool:
        return not self.parentCommand.isFullyCollapsed()

    # not interactable
    def isTouching(self, position: PointRef) -> bool:
        return False
    
    def getCenter(self) -> tuple:
        return self._px(self.definition.px), self._py(self.definition.py)
    
    def getWidth(self) -> float:
        return self._awidth(self.textWidth * self.border.OUTER_X_MARGIN*2)
    
    def getHeight(self) -> float:
        return self._awidth(self.textHeight * self.border.OUTER_Y_MARGIN*2)
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        drawText(screen, self.font.get(), self.textString, (0,0,0), self.CENTER_X, self.CENTER_Y, opacity = self.getOpacity())

        alpha = int(round(self.parentCommand.getAddonsOpacity() * 255))
        drawTransparentRect(screen, *self.RECT, (0,0,0), alpha = alpha, radius = self.border.BORDER_RADIUS, width = 2)