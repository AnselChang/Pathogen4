from __future__ import annotations
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

"""
Stores the hashmap of parameter values for a specific command block.
"""


class ParameterState:

    def __init__(self, command: CommandBlockEntity):
        self.command = command
        self.hashmap: dict[str, Any] = {}

    def getValue(self, id: str):
        return self.hashmap[id]
    
    def setValue(self, id: str, value: Any):
        self.hashmap[id] = value

    # when the command definition updates, modify hashmap to fit new parameters
    def onCommandDefinitionUpdate(self):
        pass