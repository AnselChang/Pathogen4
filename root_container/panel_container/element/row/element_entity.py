from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from entity_base.container_entity import Container
from entity_base.entity import Entity
from entity_base.text_entity import TextEntity

"""
Either a widget or readout. Inside a RowEntity, the label is always on the right column
"""

class ElementContainer(Container):

    def __init__(self, parent, parentCommand: CommandBlockEntity):
        self.parentCommand = parentCommand
        super().__init__(parent)

    def defineCenter(self) -> tuple:
        return self._px(0.8), self._py(0.5)

    # widgets and readouts should not use ElementEntity width
    # because they are dynamic
    def defineWidth(self) -> float:
        return self._pwidth(0)
    
    def defineHeight(self) -> float:
        return self._pheight(1)