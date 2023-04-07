from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from entity_base.container_entity import Container
from root_container.panel_container.command_block.icon_entity import CommandBlockIcon
from root_container.panel_container.command_block.trash_button_entity import TrashEntity
from root_container.panel_container.command_block.function_name_entity import FunctionNameEntity
from adapter.path_adapter import PathAdapter
from common.draw_order import DrawOrder

class CommandBlockHeader(Container):

    def __init__(self, parentCommand: CommandBlockEntity, pathAdapter: PathAdapter, hasTrashCan: bool):
        super().__init__(parentCommand, drawOrder = DrawOrder.WIDGET)

        self.parentCommand = parentCommand

        # recompute position BEFORE creating child entity
        self.recomputePosition()
        
        CommandBlockIcon(self, pathAdapter)
        FunctionNameEntity(self, parentCommand)

        # Only create trash can for custom command blocks
        if hasTrashCan:
            self.trashEntity = TrashEntity(self, onDelete = parentCommand.delete)
        else:
            self.trashEntity = None

    def defineTopLeft(self) -> tuple:
        return self._px(0), self._py(0)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self._pwidth(1)
    def defineHeight(self) -> float:
        return self._aheight(self.parentCommand.COLLAPSED_HEIGHT)
    