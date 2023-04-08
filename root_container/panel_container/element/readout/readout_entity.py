from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.element.readout.readout_definition import ReadoutDefinition
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from entity_base.entity import Entity
from adapter.path_adapter import PathAdapter

from entity_ui.text.text_border import TextBorder

from common.reference_frame import PointRef, Ref
from common.draw_order import DrawOrder
from utility.pygame_functions import drawText, drawTransparentRect, getText
from common.font_manager import DynamicFont, FontID
import pygame

"""
Belongs to a specific CommandBlockEntity.
Owns a DefinedReadout which stores information about the widget's context for all commands of that type
"""

class ReadoutEntity(Entity):
    def __init__(self, parent, parentCommand: CommandBlockEntity, pathAdapter: PathAdapter, readoutDefinition: ReadoutDefinition):

        self.border = TextBorder()

        self.font: DynamicFont = parentCommand.fonts.getDynamicFont(FontID.FONT_NORMAL, 15)
        self.font.subscribe(onNotify = self.recomputePosition)

        self.parentCommand = parentCommand
        self.definition = readoutDefinition
        self.pathAdapter = pathAdapter
        self.pathAdapter.subscribe(onNotify = self.updateText)

        super().__init__(parent, drawOrder = DrawOrder.READOUT)
        self.updateText()
        
        self.recomputePosition()

    def updateText(self) -> str:
        self.textString = str(self.pathAdapter.getString(self.definition.getAttribute()))
        textSurface = getText(self.font.get(), self.textString, (0,0,0), 1)
        self.textWidth = textSurface.get_width()
        self.textHeight = textSurface.get_height()
        self.recomputePosition()

    # not interactable
    def isTouching(self, position: PointRef) -> bool:
        return False
    
    def defineCenter(self) -> tuple:
        return self._px(0.5), self._py(0.5)
    
    def defineWidth(self) -> float:
        return self.textWidth + self._awidth(self.border.OUTER_X_MARGIN*2)
    
    def defineHeight(self) -> float:
        return self.textHeight + self._awidth(self.border.OUTER_Y_MARGIN*2)
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        drawText(screen, self.font.get(), self.textString, (0,0,0), self.CENTER_X, self.CENTER_Y, opacity = self.getOpacity())

        alpha = int(round(self.getOpacity() * 255))
        drawTransparentRect(screen, *self.RECT, (0,0,0), alpha = alpha, radius = self.border.BORDER_RADIUS, width = 2)