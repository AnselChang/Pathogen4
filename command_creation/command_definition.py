from root_container.panel_container.element.row.element_definition import ElementDefinition
from root_container.panel_container.element.readout.readout_definition import ReadoutDefinition
from command_creation.command_type import CommandType
from command_creation.id_generation import generate_random_id

"""
Struct used to represent the structure of a user-created command
Namely, the widgets and the text template
CommandBlocks will refer to one of these structs at a time, and users can change which
    definition object to use associated with the selected CommandBlock
This object holds DefinedWidget and DefinedReadout which store relative location, but must refer to
    the command it belongs to in order to get absolute position
"""

COMMAND_ID_LENGTH = 10

class CommandDefinition:

    def __init__(self, type: CommandType, name: str, color: tuple, elements: list[ElementDefinition] = [],
                 templateText: str = "// [default text]", isCode: bool = False, nonblockingEnabled: bool = False,
                 isTask: bool = False, allowedInTask: bool = True, id: str = None):
        
        if id is None:
            self.id = generate_random_id(COMMAND_ID_LENGTH)
        else:
            self.id = id

        self.type = type
        self.name = name
        self.color = color
        self.elements = elements
        self.templateText = templateText # text template
        self.isCode = isCode
        self.isTask = isTask
        self.nonblockingEnabled = nonblockingEnabled
        self.allowedInTask = allowedInTask