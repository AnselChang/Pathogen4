from BaseEntity.entity import Entity
from Adapters.path_adapter import PathAdapter

from TextEditor.text_border import TextBorder
from reference_frame import PointRef, Ref
from draw_order import DrawOrder
from pygame_functions import drawText, drawTransparentRect
from font_manager import DynamicFont, FontID
import pygame

"""
Belongs to a specific CommandBlockEntity.
Owns a DefinedReadout which stores information about the widget's context for all commands of that type
"""

class ReadoutEntity(Entity):
    def __init__(self, parentCommand: Entity, pathAdapter: PathAdapter, definedReadout):

        super().__init__(drawOrder = DrawOrder.READOUT)

        self.border = TextBorder(parentCommand.dimensions)

        self.font: DynamicFont = parentCommand.fontManager.getDynamicFont(FontID.FONT_NORMAL, 15)

        self.parentCommand = parentCommand
        self.definedReadout = definedReadout
        self.pathAdapter = pathAdapter

    def getText(self) -> str:
        return str(self.pathAdapter.getString(self.definedReadout.getAttribute()))
    
    def isVisible(self) -> bool:
        return self.parentCommand.isVisible()

    # not interactable
    def isTouching(self, position: PointRef) -> bool:
        return False
    
    def getPosition(self) -> PointRef:
        px, py = self.definedReadout.getPositionRatio()
        x,y = self.parentCommand.getAddonPosition(px, py)
        return PointRef(Ref.SCREEN, (x, y))
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        if self.parentCommand.isFullyCollapsed():
            return

        # opacity: 1 = solid, 0 = invisible
        opacity = self.parentCommand.getAddonsOpacity()

        cx, cy = self.getPosition().screenRef
        textWidth, textHeight = drawText(screen, self.font.get(), self.getText(), (0,0,0), cx, cy, opacity = opacity)

        x, y, w, h = self.border.getRect(cx, cy, textWidth, textHeight)
        alpha = int(round(opacity*255))
        drawTransparentRect(screen, x, y, x+w, y+h, (0,0,0), alpha = alpha, radius = self.border.BORDER_RADIUS, width = 2)

    def toString(self) -> str:
        return "Readout entity"