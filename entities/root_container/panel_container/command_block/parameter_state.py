from __future__ import annotations
from typing import TYPE_CHECKING, Any

from entities.root_container.panel_container.element.widget.widget_definition import WidgetDefinition
from models.project_history_interface import ProjectHistoryInterface
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

    # find the value of a parameter by its name and return its value.
    # if parameter does not exist, return None
    def getValueByName(self, name: str) -> str | None:

        elementDefinition = self.model.getDefinition().getElementDefinitionByName(name)

        if elementDefinition is None:
            return None
        
        return self.getValueByID(elementDefinition.id)

    def getValueByID(self, id):

        # if parameter is not in hashmap, assign to default value
        if id not in self.hashmap:
            widgetDefinition: WidgetDefinition = self.model.getDefinition().getElementDefinitionByID(id)
            self.hashmap[id] = widgetDefinition.defaultValue

        return self.hashmap[id]
    
    def setValueByID(self, id: str, value: Any):
        self.hashmap[id] = value

        # add save state to undo/redo stack
        ProjectHistoryInterface.getInstance().save()


    # when the command definition updates, modify hashmap to fit new parameters
    def onCommandDefinitionUpdate(self):
        pass