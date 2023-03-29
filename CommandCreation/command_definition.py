from dataclasses import dataclass
from Widgets.widget import Widget
from Commands.command_type import CommandType

"""
Immutable struct used to represent all the data for initializing a command
Namely, the widgets and the text template
Passed into CommandBuilder to actually build into a CommandState object
"""

class CommandDefinition:
    type: CommandType
    name: str
    widgets: list[Widget]
    templateText: str