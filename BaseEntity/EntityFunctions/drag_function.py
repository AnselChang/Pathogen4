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
