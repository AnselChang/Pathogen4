from __future__ import annotations
from typing import TYPE_CHECKING
from common.font_manager import FontID
from data_structures.observer import Observer

from entity_base.entity import Entity
from entity_ui.text.text_editor_entity import TextEditorEntity
if TYPE_CHECKING:
    from entities.root_container.panel_container.command_block_section.command_section_header import CommandSectionHeader


from entity_base.container_entity import Container
import pygame

"""
Section header contains a textbox to edit section name, as well
as UI buttons like expand/collapse
"""

class CommandSectionName(Container, Observer):

    def __init__(self, parent: CommandSectionHeader):

        super().__init__(parent = parent)

        self.header = parent

        self.text = TextEditorEntity(parent = self,
            fontID = FontID.FONT_NORMAL,
            fontSize = 16,
            isDynamic = False,
            isNumOnly = False,
            isCentered = False,
            isFixedWidth = False,
            defaultText = parent.section.model.getName(),
            hideTextbox = False,
            borderThicknessRead = 0,
            borderThicknessWrite = 2,
            readColor = (110, 110, 110),
            readColorH = (103, 103, 103),
            maxTextLength = 17
        )

        self.text.subscribe(self, onNotify = self.onTextEntityUpdate)

    def onTextEntityUpdate(self):
        self.header.section.model.setName(self.text.getText())
    
    # left margin from left edge of section header
    def defineLeftX(self) -> float:
        return self._pheight(0.8) + self._ax(17)
    
    # centered vertically to header
    def defineCenterY(self) -> float:
        return self._py(0.5)