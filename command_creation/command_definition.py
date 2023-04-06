from root_container.panel_container.element.widget.widget_definition import WidgetDefinition
from root_container.panel_container.element.readout.readout_definition import ReadoutDefinition
from command_creation.command_type import CommandType

import re

"""
Struct used to represent the structure of a user-created command
Namely, the widgets and the text template
CommandBlocks will refer to one of these structs at a time, and users can change which
    definition object to use associated with the selected CommandBlock
This object holds DefinedWidget and DefinedReadout which store relative location, but must refer to
    the command it belongs to in order to get absolute position
"""

class CommandDefinition:

    def __init__(self, type: CommandType, name: str, fullHeight: int, widgets: list[WidgetDefinition] = [], readouts: list[ReadoutDefinition] = [], templateText: str = "// [default text]"):

        self.type = type
        self.name = name
        self.fullHeight = fullHeight
        self.widgets = widgets
        self.readouts = readouts
        self.templateText = templateText # text template