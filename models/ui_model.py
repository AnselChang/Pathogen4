from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from root_container.root_container import RootContainer

"""
Stores state relevant to the program but not actual user information
like pgpath or pglib. Stores things like which window is open, etc.
"""

class CommandEditorStatus(Enum):
    HIDDEN = 0
    SHOWN = 1

class UIModel:

    _INSTANCE = None

    def getInstance() -> 'UIModel':
        if UIModel._INSTANCE is None:
            UIModel._INSTANCE = UIModel()

        return UIModel._INSTANCE

    def __init__(self):
        
        # whether to show command editor instead of path/commands
        self.commandEditorActive: CommandEditorStatus = CommandEditorStatus.HIDDEN

    # reference to ui needed to send update callbacks
    def initRootContainer(self, root: RootContainer):
        self.root = root

    def showCommandEditor(self):
        self.commandEditorActive = CommandEditorStatus.SHOWN

        # hide path/commands to show command editor
        self.root.FIELD_CONTAINER.setInvisible()
        self.root.PANEL_CONTAINER.setInvisible()

        self.root.COMMAND_EDITOR_CONTAINER.setVisible()

        self.root.recomputeEntity()

    def hideCommandEditor(self):
        self.commandEditorActive = CommandEditorStatus.HIDDEN

        # restore path/commands and hide command editor
        self.root.FIELD_CONTAINER.setVisible()
        self.root.PANEL_CONTAINER.setVisible()

        self.root.COMMAND_EDITOR_CONTAINER.setInvisible()

        self.root.recomputeEntity()

    def getCommandEditorStatus(self) -> CommandEditorStatus:
        return self.commandEditorActive