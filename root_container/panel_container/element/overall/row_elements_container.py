from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

import random
from root_container.panel_container.element.overall.abstract_elements_container import AbstractElementsContainer

from adapter.path_adapter import PathAdapter
from command_creation.command_definition import CommandDefinition
from entity_base.entity import Entity
from entity_base.container_entity import Container
from entity_ui.group.dynamic_group_container import DynamicGroupContainer
from entity_ui.group.linear_container import LinearContainer
"""
Defines the boundaries of the child RowGroupContainer in relation to the command block
This container is dynamically sized, and will resize itself to fit the number of rows
Each row has a left column (label), and right column (widget or readout)
"""

class RowElementsContainer(AbstractElementsContainer):
    
    def __init__(self, parentCommand: CommandBlockEntity, commandDefinition: CommandDefinition, pathAdapter: PathAdapter):

        super().__init__(parentCommand, commandDefinition, pathAdapter)

        self.group = None

        # Create the container that will store the rows
        self.group = DynamicGroupContainer(self, False, entitySizePixels = 22)

        # Create the rows
        ROW_SPACING = 1
        for i, elementDefinition in enumerate(commandDefinition.elements):
            row = LinearContainer(self.group, i, ROW_SPACING)

            # For each row, add label and widget/readout
            # No need to store references after created for now. But could if neededs
            label = elementDefinition.makeLabel(row)
            element = elementDefinition.makeElement(row, parentCommand, pathAdapter)

    # This container is dynamically fit to DynamicGroupContainer
    def defineHeight(self) -> float:
        if self.group is None:
            return 0
        return self.group.defineHeight()
    
    # Element and label define their own x positions along width of command block
    def defineWidth(self) -> float:
        return self._pwidth(1)
    
    def getGeneratedText(self) -> str:
        return "[TODO]"