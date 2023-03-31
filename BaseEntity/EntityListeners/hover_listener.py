from abc import ABC, abstractmethod

class Hover(ABC):

    def __init__(self, entity):
        self.entity = entity
        self.isHovering = False

    def onHoverOn(self):
        self.isHovering = True

    def onHoverOff(self):
        self.isHovering = False

class HoverLambda(Hover):

    def __init__(self, entity, FonHoverOn = lambda: None, FonHoverOff = lambda: None):
        super().__init__(entity)

        self.FonHoverOn = FonHoverOn
        self.FonHoverOff = FonHoverOff

    def onHoverOn(self):
        super().onHoverOn()
        self.FonHoverOn()

    def onHoverOff(self):
        super().onHoverOff()
        self.FonHoverOff()