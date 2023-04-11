from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
    from root_container.panel_container.command_block.function.function_name_entity import FunctionNameEntity



from common.draw_order import DrawOrder
from common.image_manager import ImageID
from entity_base.container_entity import Container
from entity_base.image.image_entity import ImageEntity
from entity_base.image.image_state import ImageState
"""
The icon that appears on the left side of the function name
"""

class FunctionSelectorIcon(Container):

    def __init__(self, functionName: FunctionNameEntity, parentCommand: CommandBlockEntity):

        super().__init__(parent = functionName)
        self.parentCommand = parentCommand
        self.functionName = functionName
        self.recomputePosition()

        ImageEntity(self, ImageState(0, ImageID.DROPDOWN_ICON),
                    drawOrder = DrawOrder.FUNCTION_NAME,
                    disableTouching = True
                    )

    # Show only when hovering over parent command
    def isVisible(self) -> bool:
        return super().isVisible() and self.parentCommand.mouseHoveringCommand

    def defineCenter(self) -> tuple:
        return self._ax(10), self._py(0.5)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self.defineHeight()
    def defineHeight(self) -> float:
        return self._pheight(0.8)