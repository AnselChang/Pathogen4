from Widgets.widget_type import WidgetType

"""
A CommandDefinition holds a list of DefinedWidgets.
A defined widget which has a widget type, as well as information relevant to a CommandDefinition
Namely: holds information for variable name and position relative to command
Does not hold the widget value itself (set and get that from widgetEntity)
"""

class DefinedWidget:

    def __init__(self, widgetType: WidgetType, name: str, px: int, py: int):
        self.widgetType = widgetType
        self._name = name

        # px and py are numbers (0-1) representing 0 (top/left) and 1 (top/right) for relative position
        self._px, self._py = px, py
        
    def setName(self, name: str) -> str:
        self._name = name

    def getName(self) -> str:
        return self._name
    
    def getPositionRatio(self) -> tuple:
        return self._px, self._py