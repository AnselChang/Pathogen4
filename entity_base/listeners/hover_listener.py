from abc import ABC, abstractmethod

class HoverListener(ABC):

    def __init__(self, entity, hoverMouseMoveCallbackEnabled):
        self.entity = entity
        self.isHovering = False

        self.hoverMouseMoveCallbackEnabled = hoverMouseMoveCallbackEnabled

    def onHoverOn(self, mouse: tuple):
        self.isHovering = True

    def onHoverOff(self):
        self.isHovering = False

    # callback for mouse moving while hovering on entity
    def onHoverMouseMove(self, mouse: tuple):
        pass

class HoverLambda(HoverListener):

    def __init__(self, entity,
                 FonHoverOn = lambda mouse: None,
                 FonHoverOff = lambda: None,
                 FonHoverMouseMove = None
                 ):
        super().__init__(entity, FonHoverMouseMove is not None)

        self.FonHoverOn = FonHoverOn
        self.FonHoverOff = FonHoverOff

        if FonHoverMouseMove is None:
            self.FonHoverMouseMove = lambda: None
        else:
            self.FonHoverMouseMove = FonHoverMouseMove

    def onHoverOn(self, mouse: tuple):
        super().onHoverOn(mouse)
        self.FonHoverOn(mouse)

    def onHoverOff(self):
        super().onHoverOff()
        self.FonHoverOff()

    def onHoverMouseMove(self, mouse: tuple):
        super().onHoverMouseMove(mouse)
        self.FonHoverMouseMove(mouse)