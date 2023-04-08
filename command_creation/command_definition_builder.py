from command_creation.command_definition import CommandDefinition

from root_container.panel_container.element.widget.widget_definition import WidgetDefinition
from root_container.panel_container.element.readout.readout_definition import ReadoutDefinition
from root_container.panel_container.element.row.element_definition import ElementDefinition

from command_creation.command_type import CommandType

from enum import Enum

"""
Instantiates a CommandDefinition
"""

class CommandDefinitionBuilder:

    def __init__(self, type: CommandType):

        self.type = type
        self.name = "untitledFunction()"
        self.elements: list[ElementDefinition] = []
        self.templateText = "// [default text]"

    def setName(self, name: str):
        self.name = name

    def setTemplateText(self, templateText: str):
        self.templateText = templateText

    def addWidget(self, widget: WidgetDefinition):
        self.elements.append(widget)

    def addReadout(self, variableName: str, attribute: Enum):
        self.elements.append(ReadoutDefinition(attribute, variableName))

    def build(self) -> CommandDefinition:
        return CommandDefinition(
            type = self.type,
            name = self.name,
            elements = self.elements,
            templateText = self.templateText
        )