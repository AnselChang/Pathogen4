from CommandCreation.command_definition import CommandDefinition

from Widgets.defined_widget import DefinedWidget
from Widgets.widget_type import WidgetType
from Widgets.defined_readout import DefinedReadout

from CommandCreation.command_type import CommandType

from enum import Enum

"""
Used to store and update the temporary state while the command is being designed by the user.
Handles stuff like adding each individual widget at a time, renaming, etc.
When the user is finished, instantiates an immutable CommandDefinition
"""

class CommandDefinitionBuilder:

    def __init__(self, type: CommandType):

        self.type = type
        self.name = "untitledFunction()"
        self.widgets: list[DefinedWidget] = []
        self.readouts: list[DefinedReadout] = []
        self.templateText = "// [default text]"

    def setName(self, name: str):
        self.name = name

    def setTemplateText(self, templateText: str):
        self.templateText = templateText

    def addWidget(self, widget: DefinedWidget):
        self.widgets.append(widget)

    def addReadout(self, attribute: Enum, px: float, py: float):
        self.readouts.append(DefinedReadout(attribute, px, py))

    def build(self) -> CommandDefinition:
        return CommandDefinition(
            type = self.type,
            name = self.name,
            widgets = self.widgets,
            readouts = self.readouts,
            templateText = self.templateText
        )