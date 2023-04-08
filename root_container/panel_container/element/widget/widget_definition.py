
from root_container.panel_container.element.widget.widget_entity import WidgetContainer
from root_container.panel_container.element.row.element_definition import ElementDefinition
from abc import abstractmethod

"""
A CommandDefinition holds a list of DefinedWidgets.
A defined widget which has a widget type, as well as information relevant to a CommandDefinition
Namely: holds information for variable name and position relative to command
Does not hold the widget value itself (set and get that from widgetEntity)
"""

class WidgetDefinition(ElementDefinition):

    def __init__(self, variableName: str):
        super().__init__(variableName)