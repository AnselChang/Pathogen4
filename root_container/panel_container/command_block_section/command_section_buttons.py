from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from common.font_manager import FontID
from common.image_manager import ImageID

from entity_base.entity import Entity
from entity_base.image.image_entity import ImageEntity
from entity_base.image.image_state import ImageState
from entity_ui.group.dynamic_group_container import DynamicGroupContainer
from entity_ui.group.linear_container import LinearContainer
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
from entity_ui.text.text_editor_entity import TextEditorEntity
if TYPE_CHECKING:
    from root_container.panel_container.command_block_section.command_section_header import CommandSectionHeader
    from root_container.panel_container.command_block_section.section_entity import SectionEntity


from entity_base.container_entity import Container
import pygame

"""
Holds a VGC for the UI buttons on the section header
IE toggle visibility, expand/collapse, etc
"""

class CommandSectionButtons(Container):

    def __init__(self, parent: CommandSectionHeader, section: SectionEntity):

        super().__init__(parent = parent)

        self.section = section

        self.group = DynamicGroupContainer(parent = self,
            isHorizontal = True,
            entitySizePixels = 12
        )
        self.id = 0
        self.percent = 1.2

        VisibilityButton(self.newLC(), section)
        VisibilityButton(self.newLC(), section)
        VisibilityButton(self.newLC(), section)

    # creates a new linear container for a section ui button
    def newLC(self) -> LinearContainer:
        lc = LinearContainer(self.group, self.id, self.percent)
        self.group.add(lc)
        return lc

    # right edge aligned to right edge of section header plus margin
    def defineRightX(self) -> float:
        return self._px(1) - self._awidth(2)
    
    # centered vertically to header
    def defineCenterY(self) -> float:
        return self._py(0.5)
    
    def defineWidth(self) -> float:
        return self.group.defineWidth()

class VisibilityID(Enum):
    VISIBLE = 0
    INVISIBLE = 1
class VisibilityButton(Container):

    def __init__(self, parent, section: SectionEntity):
        super().__init__(parent = parent)

        self.section = section

        states = [
            ImageState(VisibilityID.VISIBLE, ImageID.VISIBLE, "Path section is shown"),
            ImageState(VisibilityID.INVISIBLE, ImageID.INVISIBLE, "Path section is hidden")
        ]
        self.image = ImageEntity(parent = self,
            states = states,
            onClick = lambda mouse: self.togglePathVisibility(),
            getStateID = lambda: self.getStateID()
            )
        
    def togglePathVisibility(self):
        visibility = self.section.getPathVisibility()
        self.section.setPathVisibility(not visibility)

    def getStateID(self) -> ImageID:
        if self.section.getPathVisibility():
            return VisibilityID.VISIBLE
        else:
            return VisibilityID.INVISIBLE