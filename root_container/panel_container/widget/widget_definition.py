
from Widgets.widget_entity import WidgetEntity
from abc import abstractmethod

"""
A CommandDefinition holds a list of DefinedWidgets.
A defined widget which has a widget type, as well as information relevant to a CommandDefinition
Namely: holds information for variable name and position relative to command
Does not hold the widget value itself (set and get that from widgetEntity)
"""

class WidgetDefinition:

    def __init__(self, name: str, px: float, py: float):
        self._name = name

        # px and py are numbers (0-1) representing 0 (top/left) and 1 (top/right) for relative position
        self.px, self.py = px, py
        
        self.DEFAULT_WIDGET_HEIGHT = 0.05

    @abstractmethod
    def make(self, parentCommand) -> WidgetEntity:
        return