from abc import ABC, abstractmethod
from common.reference_frame import VectorRef, PointRef

"""
MUST be have selectListener to have DragListener.
But, can set to SOLO and deSelectOnMouseUp to true to have a drag listener that is not selectable.
"""

class DragListener(ABC):

    def __init__(self, entity):
        self.entity = entity
    
    @abstractmethod
    def onStartDrag(self, mouse: tuple):
        pass

    @abstractmethod
    def canDrag(self, mouse: tuple) -> bool:
        pass

    @abstractmethod
    def onDrag(self, mouse: tuple):
        pass

    @abstractmethod
    def onStopDrag(self):
        pass

class DragLambda(DragListener):

    def __init__(self, entity, FonStartDrag = lambda mouse: None, FonDrag = lambda mouse: True, FcanDrag = lambda mouse: True, FonStopDrag = lambda: None):
        super().__init__(entity)
        
        self.FonStartDrag = FonStartDrag
        self.FonDrag = FonDrag
        self.FcanDrag = FcanDrag
        self.FonStopDrag = FonStopDrag

    def onStartDrag(self, mouse: tuple):
        self.FonStartDrag(mouse)

    def canDrag(self, mouse: tuple) -> bool:
        return self.FcanDrag(mouse)

    def onDrag(self, mouse: tuple):
        self.FonDrag(mouse)

    def onStopDrag(self):
        self.FonStopDrag()