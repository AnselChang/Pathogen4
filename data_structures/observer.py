from typing import Callable
from enum import Enum, auto

# observer design pattern
class NotifyType(Enum):
    DEFAULT = auto()
    TURN_ENABLE_TOGGLED = auto()

class _Observer:

    def __init__(self, id = NotifyType.DEFAULT, onNotify: Callable = lambda : None):
        self.id = id
        self.onNotify = onNotify

class Observable:

    def subscribe(self, id = NotifyType.DEFAULT, onNotify: Callable = lambda : None):
        if "observers" not in self.__dict__:
            self.observers: list[Observable] = []
        self.observers.append(_Observer(id, onNotify))
        return True

    def notify(self, id = NotifyType.DEFAULT):
        if "observers" in self.__dict__:
            for observer in self.observers:
                if id == observer.id:
                    observer.onNotify()