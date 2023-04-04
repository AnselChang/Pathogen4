from typing import Callable

# observer design pattern

class Observer:

    def __init__(self, id = None, onNotify: Callable = lambda : None):
        self.id = id
        self.onNotify = onNotify

class Observable:

    def subscribe(self, id = None, onNotify: Callable = lambda : None):
        if "observers" not in self.__dict__:
            self.observers: list[Observable] = []
        self.observers.append(Observer(id, onNotify))
        return True

    def notify(self, id = None):
        if "observers" in self.__dict__:
            for observer in self.observers:
                if id == observer.id:
                    observer.onNotify()