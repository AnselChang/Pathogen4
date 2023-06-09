from typing import Callable
from entity_base.tick_entity import TickEntity


"""
Stores a "variable", rather a callback to a function that returns a value.
Calls the function every tick, and runs a callback on function change.
"""

class NotifyingVariable(TickEntity):

    def __init__(self, getValue: Callable, onChange: Callable = lambda value: None):

        self.getValue = getValue
        self.onChange = onChange

        super().__init__(onTickStart = self.onTick)

        self.previousValue = self.getValue()

    # check if there's a change, and if so, run the callback
    def onTick(self):
        newValue = self.getValue()
        if newValue != self.previousValue:
            self.onChange(newValue)
        self.previousValue = newValue

    def isVisible(self) -> bool:
        return False
    
    def isTouching(self, mouse: tuple) -> float:
        return False