from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity_ui.group.variable_group.variable_container import VariableContainer


class CommandOrInserter:

    def __init__(self, parentVariableContainer: VariableContainer):
        self.container = parentVariableContainer