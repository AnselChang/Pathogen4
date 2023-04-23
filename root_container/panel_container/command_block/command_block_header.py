from __future__ import annotations
from typing import TYPE_CHECKING

from root_container.panel_container.command_block.highlight_path_entity import HighlightPathEntity
from root_container.panel_container.command_block.wait_entity import WaitEntity
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
    from root_container.panel_container.command_block.custom_command_block_entity import CustomCommandBlockEntity

from entity_base.container_entity import Container
from root_container.panel_container.command_block.icon_entity import CommandBlockIcon
from root_container.panel_container.command_block.trash_button_entity import TrashEntity
from root_container.panel_container.command_block.function_name_entity import FunctionNameEntity
from adapter.path_adapter import PathAdapter
from common.draw_order import DrawOrder

class CommandBlockHeader(Container):

    def __init__(self, parentCommand: CommandBlockEntity | CustomCommandBlockEntity, pathAdapter: PathAdapter, isCustom: bool):
        super().__init__(parentCommand, drawOrder = DrawOrder.WIDGET)

        self.parentCommand = parentCommand

        
        self.commandIcon = CommandBlockIcon(self, pathAdapter)
        self.functionName = FunctionNameEntity(self, parentCommand)

        # Only create trash can for custom command blocks
        if isCustom:
            self.trashEntity = TrashEntity(self, onDelete = parentCommand.onDelete)
            self.highlightEntity = None
            self.waitEntity = WaitEntity(self)
        else:
            self.trashEntity = None
            self.highlightEntity = HighlightPathEntity(self, onHighlight = parentCommand.onHighlightPath)
            self.waitEntity = None
        
        self.onFunctionChange()

    # It doesn't make sense for wait() functions to be non-blocking
    def onFunctionChange(self):

        if self.waitEntity is not None:
            functionName = self.functionName.getFunctionName()
            if functionName == "wait()":
                self.waitEntity.setInvisible()
            else:
                self.waitEntity.setVisible()


    def defineTopLeft(self) -> tuple:
        return self._px(0), self._py(0)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self._pwidth(1)
    def defineHeight(self) -> float:
        return self._aheight(self.parentCommand.COLLAPSED_HEIGHT)
    