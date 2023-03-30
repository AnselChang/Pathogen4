from abc import ABC, abstractmethod
from reference_frame import VectorRef

class Drag(ABC):

    def __init__(self, entity):
        self.entity = entity
    
    @abstractmethod
    def startDragging(self):
        pass

    @abstractmethod
    def canDragOffset(self, offset: VectorRef) -> bool:
        pass

    @abstractmethod
    def dragOffset(self, offset: VectorRef):
        pass

    @abstractmethod
    def stopDragging(self):
        pass

class DragLambda(Drag):

    def __init__(self, entity, FstartDragging = lambda: None, FcanDragOffset = lambda offset: True, FdragOffset = lambda: None, FstopDragging = lambda: None):
        super().__init__(entity)
        
        self.FstartDragging = FstartDragging
        self.FcanDragOffset = FcanDragOffset
        self.FdragOffset = FdragOffset
        self.FstopDragging = FstopDragging

    def startDragging(self):
        self.FstartDragging()

    def canDragOffset(self, offset: VectorRef) -> bool:
        return self.FcanDragOffset(offset)

    def dragOffset(self, offset: VectorRef):
        self.FdragOffset(offset)

    def stopDragging(self):
        self.FstartDragging()