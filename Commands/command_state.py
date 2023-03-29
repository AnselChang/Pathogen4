from abc import ABC, abstractmethod
from CommandCreation.command_definition import CommandDefinition
from Widgets.widget import Widget
from Widgets.readout import Readout
from Adapters.adapter import Adapter
from Observers.observer import Observer
import re

"""
A ready-made command 
Text template has text like $distance$, in which case command will search for distance attribute
in both adapter and widgets

Can be initialized with CommandBuilder
"""
class CommandState(ABC):

    def __init__(self, definition: CommandDefinition, adapter: Adapter):

        observer = Observer(onNotify = self.recalculateText)

        self.adapter: Adapter = adapter
        self.widgets: list[Widget] = definition.widgets
        self.readouts: list[Readout] = definition.readouts

        self.adapter.addObserver(observer)
        for widget in self.widgets:
            widget.addObserver(observer)
        
        self.type = definition.type
        self.name = definition.name
        self.templateText = definition.templateText # text template

    # Try to find variable name in self.adapter and self.widgets and replace with value
    def replaceWithValue(self, token: str) -> str:
        if token.startswith("$") and token.endswith("$"):
            variableName = token[1:-1]

            value = self.adapter.get(variableName)
            if value is not None:
                return value
            
            for widget in self.widgets:
                if variableName == widget.getVariableName():
                    return widget.getVariableValue()
                
        # No variable found. return string as-is
        return token

    # recalculate final text from template, adapter, and widgets
    def recalculateText(self):

        result = ""

        # Split each $variable$ into tokens
        tokens = re.split(r'(\$[^\$]+\$)', self.templateText)

        # replace each $variable$ with value
        for token in tokens:
            result += self.replaceWithValue(token)

        # save computed result in finalText
        self.finalText = result

    def getCode(self) -> str:
        return self.finalText




