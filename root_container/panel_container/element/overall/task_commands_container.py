from __future__ import annotations
from typing import TYPE_CHECKING
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from root_container.panel_container.element.overall.abstract_elements_container import AbstractElementsContainer

from adapter.path_adapter import PathAdapter
from command_creation.command_definition import CommandDefinition
from entity_base.entity import Entity
from entity_base.container_entity import Container
from entity_ui.group.dynamic_group_container import DynamicGroupContainer
from entity_ui.group.linear_container import LinearContainer
"""
Contains zero or more command block entities
"""

class TaskCommandsContainer(AbstractElementsContainer):
    
    def __init__(self, parentCommand: CommandBlockEntity, commandDefinition: CommandDefinition, pathAdapter: PathAdapter):

        super().__init__(parentCommand, commandDefinition, pathAdapter)

        self.vgc = VariableGroupContainer(self, False, name = "task",
            innerMargin = 1,
            outerMargin = 0)

    # This container is dynamically fit to VariableGroupContainer
    def defineHeight(self) -> float:
        return self.vgc.defineHeight()
    
    # Element and label define their own x positions along width of command block
    def defineWidth(self) -> float:
        return self._pwidth(0.95)
    
    def getGeneratedText(self) -> str:
        return "[TODO]"