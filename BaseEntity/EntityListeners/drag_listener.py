from abc import ABC, abstractmethod
from reference_frame import VectorRef, PointRef

class DragListener(ABC):

    def __init__(self, entity):
        self.entity = entity
    
    @abstractmethod
    def onStartDrag(self, mouse: PointRef):
        pass

    @abstractmethod
    def canDrag(self, mouse: PointRef) -> bool:
        pass

    @abstractmethod
    def onDrag(self, mouse: PointRef):
        pass

    @abstractmethod
    def onStopDrag(self):
        pass

class DragLambda(DragListener):

    def __init__(self, entity, FonStartDrag = lambda: None, FonDrag = lambda offset: True, FcanDrag = lambda: None, FonStopDrag = lambda: None):
        super().__init__(entity)
        
        self.FonStartDrag = FonStartDrag
        self.FonDrag = FonDrag
        self.FcanDrag = FcanDrag
        self.FonStopDrag = FonStopDrag

    def onStartDrag(self, mouse: PointRef):
        self.FonStartDrag(mouse)

    def canDrag(self, mouse: PointRef) -> bool:
        return self.FcanDrag(mouse)

    def onDrag(self, mouse: PointRef):
        self.FonDrag(mouse)

    def onStopDrag(self):
        self.FonStopDrag()