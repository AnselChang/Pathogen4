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

    @abstractmethod
    def canDrag(self, mouse: tuple) -> bool:
        pass

    @abstractmethod
    def onDrag(self, mouse: tuple):
        pass

    def onStopDrag(self):
        self.isDragging = False

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
        self.FonDrag(mouse)

    def onStopDrag(self):
        super().onStopDrag()
        self.FonStopDrag()