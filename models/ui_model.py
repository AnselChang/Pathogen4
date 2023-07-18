from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

from data_structures.variable import Variable

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

        self.testVar = Variable("1234")

        self.testAllOptions = Variable(["A", "AB", "ABC", "ABCD"])
        self.testActiveOption = Variable("AB")
        self.testBool = Variable(True)

    # reference to ui needed to send update callbacks
    def initRootContainer(self, root: RootContainer):
        self.root = root

    def showCommandEditor(self):
        self.commandEditorActive = CommandEditorStatus.SHOWN


    def hideCommandEditor(self):
        self.commandEditorActive = CommandEditorStatus.HIDDEN


    def getCommandEditorStatus(self) -> CommandEditorStatus:
        return self.commandEditorActive