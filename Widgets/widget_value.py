"""
A struct to store the value of the widget for a specific CommandBlockEntity
"""

class WidgetValue:

    def __init__(self, value: int = 0):
        self._value = value

    def getValue(self) -> float:
        return self._value
    
    def setValue(self, value: float) -> float:
        self._value = value