from abc import ABC, abstractmethod

class Hover(ABC):

    def __init__(self, entity):
        self.entity = entity

    @abstractmethod
    def onHoverOn(self):
        pass

    @abstractmethod
    def onHoverOff(self):
        pass

class HoverLambda(Hover):

    def __init__(self, entity, FonHoverOn = lambda: None, FonHoverOff = lambda: None):
        super().__init__(entity)

        self.FonHoverOn = FonHoverOn
        self.FonHoverOff = FonHoverOff

    def onHoverOn(self):
        self.FonHoverOn()

    def onHoverOff(self):
        self.FonHoverOff()