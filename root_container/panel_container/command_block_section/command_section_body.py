from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.entity import Entity
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_sequence_handler import CommandSequenceHandler
    from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer
    from root_container.panel_container.command_block_section.section_entity import SectionEntity

from entity_base.container_entity import Container
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
import pygame

"""
Contains the command blocks of the section. below the section header
"""

class CommandSectionBody(Container):

    def __init__(self, parent: SectionEntity):

        super().__init__(parent = parent)
        self.section = parent

        self.vgc = VariableGroupContainer(parent = self,
                         isHorizontal = False,
                         innerMargin = 0,
                         outerMargin = 5,
                         name = "section")
        

    
    # This container is dynamically fit to VariableGroupContainer
    def defineHeight(self) -> float:
        return self.vgc.defineHeight()
    
    def defineTopY(self) -> float:
        return self._ay(self.section.HEADER_HEIGHT)
    
    def getOpacity(self) -> float:
        return self.section.getCommandOpacity()