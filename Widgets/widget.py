from abc import ABC, abstractmethod
from Observers.observer import Observable


"""
Each widget has following properties:
- dx, dy
- variableName
- variableValue

Slider
- min, max, step

Radio
- numOptions
- subtext for each option

Checkbox
- [none specific]

SmallTextbox

"""

class Widget(Observable):
    
    @abstractmethod
    def getVariableName(self) -> str:
        pass

    @abstractmethod
    def getVariableValue(self) -> float:
        pass