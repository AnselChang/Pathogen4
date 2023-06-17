from __future__ import annotations
from typing import TYPE_CHECKING, Any

from root_container.panel_container.element.widget.widget_definition import WidgetDefinition
if TYPE_CHECKING:
    from models.command_models.command_model import CommandModel

"""
Stores the hashmap of parameter values for a specific command block.
"""


class ParameterState:

    def __init__(self, model: CommandModel):
        self.model = model
        self.database = model.database
        self.hashmap: dict[str, Any] = {}

    def getValue(self, id):

        # if parameter is not in hashmap, assign to default value
        if id not in self.hashmap:
            widgetDefinition: WidgetDefinition = self.model.getDefinition().getElementDefinitionByID(id)
            self.hashmap[id] = widgetDefinition.defaultValue

        return self.hashmap[id]
    
    def setValue(self, id: str, value: Any):
        self.hashmap[id] = value

    # when the command definition updates, modify hashmap to fit new parameters
    def onCommandDefinitionUpdate(self):
        pass