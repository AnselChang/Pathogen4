from __future__ import annotations
from typing import TYPE_CHECKING

from entities.root_container.panel_container.element.overall.task_commands_container import TaskCommandsContainer
if TYPE_CHECKING:
    from entities.root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
    from adapter.path_adapter import PathAdapter
    
from command_creation.command_definition import CommandDefinition, CommandType
from entities.root_container.panel_container.element.overall.abstract_elements_container import AbstractElementsContainer
from entities.root_container.panel_container.element.overall.code_element_container import CodeElementContainer
from entities.root_container.panel_container.element.overall.row_elements_container import RowElementsContainer

def createElementsContainer(parentCommand: CommandBlockEntity,
                            commandDefinition: CommandDefinition,
                            pathAdapter: PathAdapter
                            ) -> AbstractElementsContainer:

    if commandDefinition.isTask:
        return TaskCommandsContainer(parentCommand, commandDefinition, pathAdapter)
    elif commandDefinition.isCode:
        return CodeElementContainer(parentCommand, commandDefinition, pathAdapter)
    else:
        return RowElementsContainer(parentCommand, commandDefinition, pathAdapter)