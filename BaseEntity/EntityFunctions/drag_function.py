from abc import ABC, abstractmethod
from reference_frame import VectorRef

class Drag(ABC):
    
    @abstractmethod
    def startDragging(self):
        pass

    @abstractmethod
    def dragOffset(self, offset: VectorRef):
        pass

    @abstractmethod
    def stopDragging(self):
        pass

class DragLambda(Drag):

    def __init__(self, FstartDragging = lambda: None, FdragOffset = lambda: None, FstopDragging = lambda: None):
        self.FstartDragging = FstartDragging
        self.FdragOffset = FdragOffset
        self.FstopDragging = FstopDragging

    def startDragging(self):
        self.FstartDragging()

    def dragOffset(self, offset: VectorRef):
        self.FdragOffset(offset)

    def stopDragging(self):
        self.FstartDragging()