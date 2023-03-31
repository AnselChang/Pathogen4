from Widgets.widget_type import WidgetType

from abc import ABC, abstractmethod
from reference_frame import PointRef
from dimensions import Dimensions

"""
A CommandDefinition holds a list of DefinedWidgets.
A defined widget which has a widget type, as well as information relevant to a CommandDefinition
Namely: holds information for variable name, position relative to command,
and any other field names...
"""

class DefinedWidget:

    def __init__(self, dimensions: Dimensions, widgetType: WidgetType, name: str, dx: int, dy: int, dict: dict[str, float] = {}):
        self.dimensions = dimensions
        self.widgetType = widgetType

        self._name = name    
        self._dx, self._dy = dx, dy # screen position offset relative to the top left corner of she command
        self._dict = dict
        
    def setName(self, name: str) -> str:
        self._name = name

    def getName(self) -> str:
        return self._name
    
    def setPositionOffset(self, offset: tuple):
        self._dx, self._dy = offset

    def getPositionOffset(self) -> tuple:
        return self._dx, self._dy

    def setAttribute(self, attribute: str, value: float):
        self._dict[attribute] = value

    def getAttribute(self, attribute: str):
        return self._dict[attribute]