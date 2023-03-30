from abc import ABC, abstractmethod

# onTick() is called every tick

class Tick(ABC):

    def __init__(self, entity):
        self.entity = entity

    @abstractmethod
    def onTick(self):
        pass


class TickLambda(Tick):

    def __init__(self, entity, FonTick = lambda: None):
        super().__init__(entity)

        self.FonTick = FonTick

    def onTick(self):
        self.FonTick()