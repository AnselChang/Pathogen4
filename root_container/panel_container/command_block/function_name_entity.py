from __future__ import annotations
from typing import TYPE_CHECKING
from common.font_manager import FontID
from entity_base.container_entity import Container
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from entity_base.entity import Entity
from entity_base.text_entity import TextEntity, TextAlign
from common.draw_order import DrawOrder


# trash button for custom commands
class FunctionNameEntity(Container):

    def __init__(self, parentHeader, parentCommand: CommandBlockEntity):
        
        super().__init__(parent = parentHeader)
        self.recomputePosition()

        TextEntity(self,
                   fontID = FontID.FONT_NORMAL,
                   fontSize = 19,
                   textFunction = lambda: parentCommand.getFunctionName() + "()",
                   align = TextAlign.LEFT,
                   drawOrder = DrawOrder.WIDGET
                   )


    def defineLeftX(self) -> tuple:
        return self._ax(37)
    
    def defineCenterY(self) -> float:
        return self._py(0.5)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self._pheight(0.8) # yes, this is height not width. square icon
    def defineHeight(self) -> float:
        return self._pheight(0.8)