from __future__ import annotations
from typing import TYPE_CHECKING
from common.font_manager import FontID
from data_structures.observer import Observer
from entity_base.container_entity import Container
from entity_base.listeners.hover_listener import HoverLambda
from entity_ui.dropdown.dropdown_container import DropdownContainer
from utility.pygame_functions import shade
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from entity_base.entity import Entity
from entity_base.text_entity import TextEntity, TextAlign
from common.draw_order import DrawOrder
import pygame

"""
Draws the function name, and contains the dropdown to select the funciton
"""

class FunctionNameEntity(Entity, Observer):

    def __init__(self, parentHeader, parentCommand: CommandBlockEntity):
        
        self.parentCommand = parentCommand
        super().__init__(parent = parentHeader,
                         hover = HoverLambda(self))
        
        self.dx = 19 # delta for text from left edge
        self.textEntity = None

        self.CORNER_RADIUS = 5
        
        names = self._getDefinitionFunctionNames()
        self.dropdown = DropdownContainer(self, names,
                          FontID.FONT_NORMAL, 18,
                          (0,0,0), (0,0,0), (0,0,0), (0,0,0),
                          dynamicWidth = True, dynamicBorderOpacity = True, centered = False,
                          iconScale = 0.6, textLeftOffset = 16, cornerRadius = 7, verticalTextPadding = 0)
        self.updateColor()

        # Whenever the name changes, notify the commmand block entity to update the command
        self.dropdown.subscribe(self, onNotify = self.parentCommand.onFunctionChange)

    def updateColor(self):

        color = self.parentCommand.getColor()
        colorSelectedHovered = shade(color, 0.975)
        colorSelected = shade(color, 1)
        colorHovered = shade(color, 1.1)
        colorOff = shade(color, 1.3)
        self.dropdown.setColor(colorSelectedHovered, colorSelected, colorHovered, colorOff)


    def getFunctionName(self):
        return self.dropdown.getSelectedOptionText()

    def _getDefinitionFunctionNames(self) -> list[str]:
        return self.parentCommand.database.getDefinitionNames(self.parentCommand.type)

    def defineLeftX(self) -> tuple:
        return self._px(0) + self._pheight(1)
    
    def defineCenterY(self) -> float:
        return self._py(0.5)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:

        if self.textEntity is None:
            return 0

        RIGHT_MARGIN = 5
        return self._awidth(self.dx + RIGHT_MARGIN) + self.textEntity.getTextWidth() # yes, this is height not width. square icon
    
    def defineHeight(self) -> float:
        return self._pheight(0.8)
