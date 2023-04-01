# observer design pattern

class Observer:

    def __init__(self, onNotify = lambda : None):
        self.onNotify = onNotify

    def notify(self):
        self.onNotify()

class Observable:

    def addObserver(self, observer: Observer):
        if "observers" not in self.__dict__:
            self.observers: list[Observer] = []
        self.observers.append(observer)
        return True

    def removeObserver(self, observer: Observer):
        if "observers" in self.__dict__ and observer in self.observers:
            self.observers.remove(observer)
            return True
        return False

    def notify(self):
        if "observers" in self.__dict__:
            for observer in self.observers:
                observer.notify()