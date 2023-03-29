from abc import ABC, abstractmethod
from enum import Enum

class Adapter:
    pass

class SegmentAdapter(Adapter):

    class ID(Enum):
        STRAIGHT = 1
        ARC = 2
        BEZIER = 3

    def __init__(self, id: ID):
        self.id = id

class AdapterInterface(ABC):

    @abstractmethod
    def getAdapter(self) -> Adapter:
        pass

    @abstractmethod
    def updateAdapter(self) -> None:
        pass