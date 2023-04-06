from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Commands.command_block_entity import CommandBlockEntity

from BaseEntity.container_entity import ContainerEntity
from Commands.command_block_icon import CommandBlockIcon
from Adapters.path_adapter import PathAdapter
from draw_order import DrawOrder

class CommandBlockHeader(ContainerEntity):

    def __init__(self, parentCommand: CommandBlockEntity, pathAdapter: PathAdapter):
        super().__init__(parentCommand, drawOrder = DrawOrder.WIDGET)

        self.parentCommand = parentCommand
        CommandBlockIcon(self, pathAdapter)

    def defineTopLeft(self) -> tuple:
        return self._px(0), self._py(0)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self._pwidth(1)
    def defineHeight(self) -> float:
        return self.parentCommand.COLLAPSED_HEIGHT
    