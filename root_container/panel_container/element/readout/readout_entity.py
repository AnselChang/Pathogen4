from __future__ import annotations
from typing import TYPE_CHECKING
from data_structures.observer import Observer
from entity_base.listeners.hover_listener import HoverLambda

from root_container.panel_container.element.row.element_entity import ElementContainer
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

class ReadoutEntity(ElementContainer, Observer):
    def __init__(self, parent, parentCommand: CommandBlockEntity, pathAdapter: PathAdapter, readoutDefinition: ReadoutDefinition):

        self.border = TextBorder()

        self.font: DynamicFont = parentCommand.fonts.getDynamicFont(readoutDefinition.LABEL_FONT, readoutDefinition.LABEL_SIZE)
        self.font.subscribe(self, onNotify = self.recomputeEntity)

        self.definition = readoutDefinition
        self.pathAdapter = pathAdapter
        self.pathAdapter.subscribe(self, onNotify = self.recomputeEntity)

        super().__init__(parent, parentCommand)
        
    def updateText(self) -> str:
        self.textString = str(self.pathAdapter.getString(self.definition.getAttribute()))
        textSurface = getText(self.font.get(), self.textString, (0,0,0), 1)
        self.textWidth = textSurface.get_width()
        self.textHeight = textSurface.get_height()

    def defineBefore(self):
        self.updateText()

    
    def defineWidth(self) -> float:
        return self.textWidth + self._awidth(self.border.OUTER_X_MARGIN*2)
    
    def defineHeight(self) -> float:
        return self.textHeight + self._aheight(self.border.OUTER_Y_MARGIN*2)
    
    def isTouching(self, mouse: tuple) -> bool:
        return Entity.isTouching(self, mouse)
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        color = (60,60,60) if isHovered else (0,0,0)

        drawText(screen, self.font.get(), self.textString, color, self.CENTER_X, self.CENTER_Y, opacity = self.getOpacity())

        alpha = int(round(self.getOpacity() * 255))
        drawTransparentRect(screen, *self.RECT, color, alpha = alpha, radius = self.border.BORDER_RADIUS, width = 2)