from __future__ import annotations
from typing import TYPE_CHECKING
from data_structures.observer import Observable

from typing import TypeVar, Generic

"""
A variable that stores a value. When the value is modified,
it sends an notification to subscribers.
"""

T = TypeVar('T')
class Variable(Observable, Generic[T]):

    def __init__(self, startValue: T = None):
        
        self._prevValue = startValue
        self._currentValue = startValue

        super().__init__()

    # get the current value of the variable
    def get(self) -> T:
        return self._currentValue
    
    # set a new value for the variable, and notify subscribers if there was a change
    def set(self, value: T):

        changed = value != self._currentValue

        self._prevValue = self._currentValue
        self._currentValue = value

        if changed:
            self.notify()