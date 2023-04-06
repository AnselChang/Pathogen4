from command_creation.command_definition import CommandDefinition

from root_container.panel_container.widget.widget_definition import WidgetDefinition
from root_container.panel_container.widget.readout_definition import ReadoutDefinition

from command_creation.command_type import CommandType

from enum import Enum

"""
Instantiates a CommandDefinition
"""

class CommandDefinitionBuilder:

    def __init__(self, type: CommandType):

        self.type = type
        self.name = "untitledFunction()"
        self.fullHeight = 0.15
        self.widgets: list[WidgetDefinition] = []
        self.readouts: list[ReadoutDefinition] = []
        self.templateText = "// [default text]"

    def setName(self, name: str):
        self.name = name

    def setHeight(self, height: int):
        self.fullHeight = height

    def setTemplateText(self, templateText: str):
        self.templateText = templateText

    def addWidget(self, widget: WidgetDefinition):
        self.widgets.append(widget)

    def addReadout(self, attribute: Enum, px: float, py: float):
        self.readouts.append(ReadoutDefinition(attribute, px, py))

    def build(self) -> CommandDefinition:
        return CommandDefinition(
            type = self.type,
            name = self.name,
            fullHeight = self.fullHeight,
            widgets = self.widgets,
            readouts = self.readouts,
            templateText = self.templateText
        )