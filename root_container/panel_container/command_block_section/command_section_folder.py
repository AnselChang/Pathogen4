from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from common.image_manager import ImageID
from entity_base.image.image_entity import ImageEntity

from entity_base.entity import Entity
from entity_base.image.image_state import ImageState
if TYPE_CHECKING:
    from root_container.panel_container.command_block_section.command_section_header import CommandSectionHeader
    from root_container.panel_container.command_block_section.section_entity import SectionEntity

from entity_base.container_entity import Container
import pygame

"""
Section header contains a textbox to edit section name, as well
as UI buttons like expand/collapse
"""

class SectionExpansion(Enum):
    EXPANDED = 0
    COLLAPSED = 1

class CommandSectionFolder(Container):

    def __init__(self, parent: CommandSectionHeader, section: SectionEntity):

        super().__init__(parent = parent)

        states = [
            ImageState(SectionExpansion.EXPANDED, ImageID.FOLDER_OPEN, hoveredBrightenAmount = -20),
            ImageState(SectionExpansion.COLLAPSED, ImageID.FOLDER_CLOSED, hoveredBrightenAmount = -20)
        ]

        self.image = ImageEntity(parent = self,
            states = states,
            getStateID = lambda: SectionExpansion.EXPANDED if section.isExpanded() else SectionExpansion.COLLAPSED,
            onClick = lambda mouse: section.toggleExpansion(),
        )
    
    # left margin from left edge of section header
    def defineLeftX(self) -> float:
        return self._ax(10)
    
    # centered vertically to header
    def defineCenterY(self) -> float:
        return self._py(0.5)
    
    def defineWidth(self) -> float:
        return self.defineHeight()
    
    def defineHeight(self) -> float:
        return self._pheight(0.8)