from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.entity import Entity
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_sequence_handler import CommandSequenceHandler
    from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer


from entity_base.container_entity import Container
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
import pygame

"""
A command section holds command blocks. Its usefulness lies in being able to
expand and collapse command sections, as well as show or hide the path section
pertaining to the command section.
"""

class CommandSection(Container):

    def __init__(self, parent: Entity, handler: CommandSequenceHandler):

        super().__init__(parent = parent)
    
        self.handler = handler
        self.vgc = VariableGroupContainer(parent = self,
                         isHorizontal = False,
                         innerMargin = 0,
                         outerMargin = 5,
                         name = "section")
        
        # initialize first inserter inside command section
        inserterVariableContainer = self.handler._createInserter(self.vgc)
        self.vgc.containers.addToBeginning(inserterVariableContainer)

    # This container is dynamically fit to VariableGroupContainer
    def defineHeight(self) -> float:
        return self.vgc.defineHeight()

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pygame.draw.rect(screen, (120, 120, 120), self.RECT, 0, border_radius = 5)