from Widgets.widget import Widget
from Widgets.readout import Readout
from CommandCreation.command_type import CommandType

"""
Immutable struct used to represent all the data for initializing a command
Namely, the widgets and the text template
Passed into CommandBuilder to actually build into a CommandState object
"""

class CommandDefinition:

    def __init__(self,
                 type: CommandType,
                 name: str,
                 widgets: list[Widget] = [],
                 readouts: list[Readout] = [],
                 templateText: str = "// [no text specified]"
                 ):
        self.type = type
        self.name = name
        self.widgets = widgets
        self.readouts = readouts
        self.templateText = templateText