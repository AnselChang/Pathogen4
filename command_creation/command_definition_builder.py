from command_creation.command_definition import CommandDefinition

from root_container.panel_container.element.widget.widget_definition import WidgetDefinition
from root_container.panel_container.element.readout.readout_definition import ReadoutDefinition
from root_container.panel_container.element.row.element_definition import ElementDefinition

from command_creation.command_type import CommandType

from enum import Enum

"""
Instantiates a CommandDefinition
Passing in "None" indicates it is a code command
"""

class CommandDefinitionBuilder:

    def __init__(self, type: CommandType | None):

        self.type = type
        self.elements: list[ElementDefinition] = []

        if type is None:
            self.type = CommandType.CUSTOM
            self._isCode = True
            self.name = "code"
            self.templateText = "// [default text]"
        else:
            self._isCode = False
            self.name = "untitledFunction"
            self.templateText = "// [Code template unspecified]"

        

    def setName(self, name: str):

        if self._isCode:
            raise Exception("Cannot set variable name for code commands")

        self.name = name

    def setTemplateText(self, templateText: str):

        if self._isCode:
            raise Exception("Cannot set template text to code commands")

        self.templateText = templateText

    def addWidget(self, widget: WidgetDefinition):
        if self._isCode:
            raise Exception("Cannot add widgets to code commands")
        
        self.elements.append(widget)

    def addReadout(self, variableName: str, attribute: Enum):
        if self._isCode:
            raise Exception("Cannot add widgets to code commands")
        
        if not self._isCode:
            self.elements.append(ReadoutDefinition(attribute, variableName))

    def build(self) -> CommandDefinition:
        return CommandDefinition(
            type = self.type,
            name = self.name,
            elements = self.elements,
            templateText = self.templateText,
            isCode = self._isCode
        )