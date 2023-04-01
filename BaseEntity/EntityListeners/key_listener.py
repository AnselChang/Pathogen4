from abc import ABC, abstractmethod

# onTick() is called every tick

class KeyListener(ABC):

    def __init__(self, entity):
        self.entity = entity

    @abstractmethod
    def onKeyDown(self, key):
        pass

    @abstractmethod
    def onKeyUp(self, key):
        pass


class KeyLambda(KeyListener):

    def __init__(self, entity, FonKeyDown = lambda key: None, FonKeyUp = lambda key: None):
        super().__init__(entity)

        self.FonKeyDown = FonKeyDown
        self.FonKeyUp = FonKeyUp

    def onKeyDown(self, key):
        self.FonKeyDown(key)

    def onKeyUp(self, key):
        self.FonKeyUp(key)