from adapter.path_adapter import PathAdapter
from command_creation.command_definition import CommandDefinition
from entity_base.entity import Entity
from entity_base.container_entity import Container
from entity_ui.group.dynamic_group_container import DynamicGroupContainer
from entity_ui.group.linear_container import LinearContainer
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
"""
Defines the boundaries of the child RowGroupContainer in relation to the command block
This container is dynamically sized, and will resize itself to fit the number of rows
Each row has a left column (label), and right column (widget or readout)
"""

class AllElementsContainer(Container):
    
    def __init__(self, parentCommand: CommandBlockEntity, commandDefinition: CommandDefinition, pathAdapter: PathAdapter):

        super().__init__(parentCommand)
        self.parentCommand = parentCommand
        self.commandDefinition = commandDefinition

        self.recomputePosition()

        # Create the container that will store the rows
        self.group = DynamicGroupContainer(self, False, entitySizePixels = 30)

        # Create the rows
        ROW_SPACING = 0.95
        for i, elementDefinition in enumerate(commandDefinition.elements):
            row = LinearContainer(self.group, i, ROW_SPACING)

            # For each row, add label and widget/readout
            label = elementDefinition.makeLabel(row)
            element = elementDefinition.makeElement(row, parentCommand, pathAdapter)
        

    def defineCenterX(self) -> float:
        return self._px(0.5)
    
    def defineTopY(self) -> float:
        bottomHeaderY = self._py(0) + self._aheight(self.parentCommand.COLLAPSED_HEIGHT)
        return bottomHeaderY + self._aheight(10) # 10px of padding between header and rows

    # This container is dynamically fit to DynamicGroupContainer
    def defineHeight(self) -> float:
        return self.group.defineHeight()
    
    # Element and label define their own x positions along width of command block
    def defineWidth(self) -> float:
        return self._pwidth(1)