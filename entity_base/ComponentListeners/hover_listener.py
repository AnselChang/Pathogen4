from abc import ABC, abstractmethod
from reference_frame import PointRef

class HoverListener(ABC):

    def __init__(self, entity):
        self.entity = entity
        self.isHovering = False

    def onHoverOn(self):
        self.isHovering = True

    def onHoverOff(self):
        self.isHovering = False

    def whileHovering(self, mouse: PointRef):
        pass

class HoverLambda(HoverListener):

    def __init__(self, entity, FonHoverOn = lambda: None, FonHoverOff = lambda: None, FWhileHovering = lambda mouse: None):
        super().__init__(entity)

        self.FonHoverOn = FonHoverOn
        self.FonHoverOff = FonHoverOff
        self.FWhileHovering = FWhileHovering

    def onHoverOn(self):
        super().onHoverOn()
        self.FonHoverOn()

    def onHoverOff(self):
        super().onHoverOff()
        self.FonHoverOff()

    def whileHovering(self, mouse: PointRef):
        super().whileHovering(mouse)
        self.FWhileHovering(mouse)