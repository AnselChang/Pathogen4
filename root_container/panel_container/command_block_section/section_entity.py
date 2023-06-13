from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.entity import Entity
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.hover_listener import HoverLambda
from entity_base.listeners.tick_listener import TickLambda
from entity_ui.group.variable_group.variable_container import VariableContainer
from models.command_models.model_based_entity import ModelBasedEntity
from root_container.panel_container.command_block_section.command_section_body import CommandSectionBody
from root_container.panel_container.command_block_section.command_section_header import CommandSectionHeader
from utility.motion_profile import MotionProfile
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

class SectionEntity(Entity, ModelBasedEntity):

    def __init__(self, parent: Entity):

        self.HEADER_HEIGHT = 30
        super().__init__(parent = parent,
            click = ClickLambda(self, FonLeftClick=lambda mouse: self.toggleExpansion()),
            tick = TickLambda(self, FonTickStart=lambda: self.onTick()),
        )

        self.pathVisible = True
        self.commandsVisible = True

        # controls height animation
        self.animatedExpansion = MotionProfile(1, speed = 0.4)
        
        self.body = CommandSectionBody(parent = self)
        self.header = CommandSectionHeader(parent = self)

    def getChildVGC(self) -> VariableGroupContainer:
        return self.body.vgc

     # Update animation every tick
    def onTick(self):

        # If section just finished collapsing, hide commands
        isFullyCollapsed = self.isFullyCollapsed()
        if self.commandsVisible and isFullyCollapsed:
            self.body.setInvisible()
            self.commandsVisible = False
            self.recomputeEntity()
        elif not self.commandsVisible and not isFullyCollapsed:
            self.body.setVisible()
            self.commandsVisible = True
            self.recomputeEntity()

        # handle expansion animation
        if not self.animatedExpansion.isDone():
            self.animatedExpansion.tick()
            self.recomputeEntity()

    def getCommandOpacity(self) -> float:
        return self.animatedExpansion.get()

    def setPathVisibility(self, isPathVisible: bool):
        self.pathVisible = isPathVisible

    def getPathVisibility(self) -> bool:
        return self.pathVisible
    
    def isFullyCollapsed(self):
        return self.animatedExpansion.isDone() and self.animatedExpansion.getEndValue() == 0
    
    def setExpansion(self, isExpanded: bool):
        self.animatedExpansion.setEndValue(1 if isExpanded else 0)

    def getExpansion(self) -> float:
        return self.commandsVisible
    
    def isExpanded(self) -> bool:
        return not self.isFullyCollapsed()
    
    def toggleExpansion(self):
        if self.animatedExpansion.getEndValue() == 0:
            self.setExpansion(True)
        else:
            self.setExpansion(False)

    # This container is dynamically fit to VariableGroupContainer
    def defineHeight(self) -> float:
        py = self._aheight(10) # a little padding below header
        return self.header.defineHeight() + (self.body.defineHeight()-py) * self.animatedExpansion.get() + py

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pygame.draw.rect(screen, (120, 120, 120), self.RECT, 0, border_radius = 5)