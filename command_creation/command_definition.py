from root_container.panel_container.element.row.element_definition import ElementDefinition
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

    def __init__(self, type: CommandType, name: str, color: tuple, elements: list[ElementDefinition] = [], templateText: str = "// [default text]", isCode: bool = False):

        self.type = type
        self.name = name
        self.color = color
        self.elements = elements
        self.templateText = templateText # text template
        self.isCode = isCode