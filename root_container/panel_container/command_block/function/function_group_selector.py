from __future__ import annotations
from typing import TYPE_CHECKING
from common.font_manager import DynamicFont, FontID

from entity_base.entity import Entity
from entity_ui.group.linear_container import LinearContainer
from root_container.panel_container.command_block.function.function_option_entity import FunctionOptionEntity
from utility.pygame_functions import shade
from entity_ui.group.dynamic_group_container import DynamicGroupContainer

"""
A ListBox UI component that displays a static list of options for user selection.
There is no animation, and the currently-selected option has a icon to the left
to indicate it.
This uses a DynamicGroupContainer to display the options.
Kinda redundant code to store active option, but easier than dealing with
multiple inheritance.

This is a TEMPORARY entity. It returns the selected option, and should be deleted after.
"""

class FunctionGroupSelector(DynamicGroupContainer):

    def getOptionHeight(self) -> float:
        self.font.get()
        return self.font.getCharHeight() * self.TEXT_PADDING_RATIO
    
    def onOptionClick(self, option: str):
        print("option", option)
    
    def __init__(self, parent: Entity, selectedOption: str, options: str, font: DynamicFont, color: tuple, awidth: float):
        
        self.CORNER_RADIUS = 5
        self.TEXT_PADDING_RATIO = 1.1
        self.TEXT_LEFT_OFFSET = 15

        self.awidth = awidth
        self.font = font
        
        super().__init__(parent, isHorizontal = False, entitySizePixels = self.getOptionHeight())

        for i, optionStr in enumerate(options):
            
            thisColor = shade(color, 0.6) if (optionStr == selectedOption) else color

            optionContainer = LinearContainer(self, optionStr, 1)
            FunctionOptionEntity(optionContainer, optionStr, self.font, thisColor,
                isFirst = (i == 0),
                isLast = (i == len(options) - 1),
                onClick = lambda text: self.onOptionClick(text),
                leftTextOffset = self.TEXT_LEFT_OFFSET,
                cornerRadius = self.CORNER_RADIUS
            )
        
    def defineWidth(self) -> float:
        return self._awidth(self.awidth)
        