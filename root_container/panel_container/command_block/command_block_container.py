from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity_ui.group.variable_group.variable_container import VariableContainer
    from root_container.panel_container.command_block.command_inserter import CommandInserter


from entity_base.container_entity import Container
from entity_base.entity import Entity
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity


"""
Holds a CommandBlockEntity.
Rect is identical to CommandBlockEntity, EXCEPT when the user is dragging a custom
block to move it around. In that case, the y position is the mouse position.
"""

class CommandBlockContainer(Container):

    def __init__(self, parent: VariableContainer[CommandBlockContainer | CommandInserter]):

        super().__init__(parent)
        self.variableContainer = parent
        self.commandBlock: CommandBlockEntity = None

    def initCommandBlock(self, command: CommandBlockEntity):
        self.commandBlock = command

    def defineHeight(self) -> float:
         return self.commandBlock.defineHeight()
    
    # if command is being dragged, always show in front of other commands
    def drawOrderTiebreaker(self) -> float:
        if self.commandBlock.drag.isDragging:
            return self.dimensions.SCREEN_HEIGHT
        else:
            return None