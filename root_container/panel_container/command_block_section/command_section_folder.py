from __future__ import annotations
from typing import TYPE_CHECKING
from common.image_manager import ImageID
from entity_base.image.image_entity import ImageEntity

from entity_base.entity import Entity
from entity_base.image.image_state import ImageState
if TYPE_CHECKING:
    from root_container.panel_container.command_block_section.command_section_header import CommandSectionHeader


from entity_base.container_entity import Container
import pygame

"""
Section header contains a textbox to edit section name, as well
as UI buttons like expand/collapse
"""

class CommandSectionFolder(Container):

    def __init__(self, parent: CommandSectionHeader):

        super().__init__(parent = parent)

        self.image = ImageEntity(parent = self,
            states = ImageState(0, ImageID.FOLDER),
            disableTouching = True
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