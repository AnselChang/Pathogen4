from entity_base.container_entity import Container
from entity_base.entity import Entity
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity


"""
Holds a CommandBlockEntity.
Rect is identical to CommandBlockEntity, EXCEPT when the user is dragging a custom
block to move it around. In that case, the y position is the mouse position.
"""

class CommandBlockContainer(Container):

    def __init__(self, parent: Entity):

        super().__init__(parent)

        self.commandBlock: CommandBlockEntity = None

    def initCommandBlock(self, command: CommandBlockEntity):
            self.commandBlock = command