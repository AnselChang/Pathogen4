from typing import Callable
from enum import Enum, auto

# observer design pattern
class NotifyType(Enum):
    DEFAULT = auto()
    TURN_ENABLE_TOGGLED = auto()

# Classes that want to observe observables must implement Observers
# This is in charge of correctly handling unsubscriptions when the object is deleted
# otherwise, the observable will still try to notify the observer, and prevent
# object from being garbage collected
class Observer:

    def onSubscribe(self, observable: 'Observable'):

        if "observablesIAmSubscribedTo" not in self.__dict__:
            self.observablesIAmSubscribedTo: list['Observable'] = []

        self.observablesIAmSubscribedTo.append(observable)


    def unsubscribeAll(self):

        if "observablesIAmSubscribedTo" not in self.__dict__:
            return
        
        
        for observable in self.observablesIAmSubscribedTo:
            observable.unsubscribe(self)

class _ObserverState:

    def __init__(self, observer: Observer, id = NotifyType.DEFAULT, onNotify: Callable = lambda : None):
        self.observer = observer
        self.id = id
        self.onNotify = onNotify

class Observable:

    # object should pass its own reference to subscribe() as a first argument
    def subscribe(self, yourself: Observer, id = NotifyType.DEFAULT, onNotify: Callable = lambda : None):

        if not isinstance(yourself, Observer):
            raise Exception("you must pass a reference to yourself as the first argument")

        if not isinstance(id, NotifyType):
            raise Exception("id must be of type NotifyType")
        
        if not isinstance(onNotify, Callable):
            raise Exception("onNotify must be of type Callable")
        
        yourself.onSubscribe(self)
        
        if "observers" not in self.__dict__:
            self.observers: list[_ObserverState] = []
        self.observers.append(_ObserverState(yourself, id, onNotify))
        return True
    
    def unsubscribe(self, observer: Observer):
        if "observers" not in self.__dict__:
            return
        
        i = 0
        while i < len(self.observers):
            if self.observers[i].observer is observer:
                del self.observers[i]
            else:
                i += 1

    def notify(self, id = NotifyType.DEFAULT):
        if "observers" in self.__dict__:
            for observer in self.observers:
                if id == observer.id:
                    observer.onNotify()