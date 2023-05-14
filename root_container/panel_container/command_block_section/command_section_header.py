from __future__ import annotations
from typing import TYPE_CHECKING
from root_container.panel_container.command_block_section.command_section_buttons import CommandSectionButtons
from root_container.panel_container.command_block_section.command_section_folder import CommandSectionFolder

from root_container.panel_container.command_block_section.command_section_name import CommandSectionName
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_sequence_handler import CommandSequenceHandler
    from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer
    from root_container.panel_container.command_block_section.command_section import CommandSection

from entity_base.container_entity import Container
import pygame

"""
Section header contains a textbox to edit section name, as well
as UI buttons like expand/collapse
"""

class CommandSectionHeader(Container):

    def __init__(self, parent: CommandSection):

        super().__init__(parent = parent)
        self.section = parent

        self.folder = CommandSectionFolder(parent = self, section = parent)
        self.sectionName = CommandSectionName(parent = self)
        self.buttons = CommandSectionButtons(parent = self, section = parent)
    
    # This container is dynamically fit to VariableGroupContainer
    def defineHeight(self) -> float:
        return self._aheight(self.section.HEADER_HEIGHT)
    
    def defineTopY(self) -> float:
        return self._py(0) + self._aheight(5)