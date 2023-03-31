from Widgets.defined_widget import DefinedWidget
from Widgets.readout_state import ReadoutState
from CommandCreation.command_type import CommandType

from Adapters.path_adapter import PathAdapter
from Adapters.widget_adapter import WidgetAdapter

import re

"""
Struct used to represent the structure of a user-created command
Namely, the widgets and the text template
CommandBlocks will refer to one of these structs at a time, and users can change which
    definition object to use associated with the selected CommandBlock
This object holds WidgetState and ReadoutState which store relative location, but must refer to
    the command it belongs to in order to get absolute position
"""

class CommandDefinition:

    def __init__(self, type: CommandType, name: str, widgets: list[DefinedWidget], readouts: list[ReadoutState], templateText: str):

        self.type = type
        self.name = name
        self.widgets = widgets
        self.readouts = readouts
        self.templateText = templateText # text template