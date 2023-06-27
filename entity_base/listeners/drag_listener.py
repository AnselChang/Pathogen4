from abc import ABC, abstractmethod

"""
MUST be have selectListener to have DragListener.
But, can set to SOLO and deSelectOnMouseUp to true to have a drag listener that is not selectable.
"""

class DragListener(ABC):

    # if selectEntityNotThis is not None, when this object is dragged,
    # it won't be selected, but selectEntityNotThis will be selected
    def __init__(self, entity, selectEntityNotThis):
        self.entity = entity
        self.selectEntityNotThis = selectEntityNotThis
        self.isDragging = False
    
    def onStartDrag(self, mouse: tuple):
        self.isDragging = True
        self.prevX, self.prevY = mouse
        self.startX, self.startY = mouse
        self.offsetX = 0
        self.offsetY = 0
        self.totalOffsetX = 0
        self.totalOffsetY = 0

    @abstractmethod
    def canDrag(self, mouse: tuple) -> bool:
        pass

    def onDrag(self, mouse: tuple):
        self.offsetX = mouse[0] - self.prevX
        self.offsetY = mouse[1] - self.prevY
        self.prevX, self.prevY = mouse

        self.totalOffsetX = mouse[0] - self.startX
        self.totalOffsetY = mouse[1] - self.startY

    def onStopDrag(self):
        self.isDragging = False
        self.offsetX = 0
        self.offsetY = 0

class DragLambda(DragListener):

    def __init__(self, entity, selectEntityNotThis = None, FonStartDrag = lambda mouse: None, FonDrag = lambda mouse: True, FcanDrag = lambda mouse: True, FonStopDrag = lambda: None):
        super().__init__(entity, selectEntityNotThis)
        self.FonStartDrag = FonStartDrag
        self.FonDrag = FonDrag
        self.FcanDrag = FcanDrag
        self.FonStopDrag = FonStopDrag

    def onStartDrag(self, mouse: tuple):
        super().onStartDrag(mouse)
        self.FonStartDrag(mouse)

    def canDrag(self, mouse: tuple) -> bool:
        return self.FcanDrag(mouse)

    def onDrag(self, mouse: tuple):
        super().onDrag(mouse)
        self.FonDrag(mouse)

    def onStopDrag(self):
        super().onStopDrag()
        self.FonStopDrag()