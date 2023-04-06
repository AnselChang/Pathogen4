from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Commands.command_block_entity import CommandBlockEntity

from Commands.custom_command_block_entity import CustomCommandBlockEntity
from BaseEntity.container_entity import ContainerEntity
from Commands.icon_entity import CommandBlockIcon
from Commands.trash_button_entity import TrashEntity
from Adapters.path_adapter import PathAdapter
from draw_order import DrawOrder

class CommandBlockHeader(ContainerEntity):

    def __init__(self, parentCommand: CommandBlockEntity | CustomCommandBlockEntity, pathAdapter: PathAdapter):
        super().__init__(parentCommand, drawOrder = DrawOrder.WIDGET)

        self.parentCommand = parentCommand

        CommandBlockIcon(self, pathAdapter)

        # Only create trash can for custom command blocks
        if isinstance(self.parentCommand, CustomCommandBlockEntity):
            TrashEntity(parentCommand, onDelete = parentCommand.delete)

    def defineTopLeft(self) -> tuple:
        return self._px(0), self._py(0)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self._pwidth(1)
    def defineHeight(self) -> float:
        return self.parentCommand.COLLAPSED_HEIGHT
    