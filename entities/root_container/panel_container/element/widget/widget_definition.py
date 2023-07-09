
from entities.root_container.panel_container.element.widget.widget_entity import WidgetContainer
from entities.root_container.panel_container.element.row.element_definition import ElementDefinition, ElementType
from abc import abstractmethod

class WidgetDefinition(ElementDefinition):

    def __init__(self, elementType: ElementType, variableName: str, defaultValue):
        super().__init__(elementType, variableName)
        self.defaultValue = defaultValue