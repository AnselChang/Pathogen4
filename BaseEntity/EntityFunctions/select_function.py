from abc import ABC, abstractmethod
from enum import Enum

from reference_frame import PointRef

class Select(ABC):

    def __init__(self, entity, id: str, FgetHitboxPoints = lambda : []):
        self.entity = entity
        self.id = id
        self.FgetHitboxPoints = FgetHitboxPoints

    def getHitboxPoints(self) -> list[PointRef]:
        return self.FgetHitboxPoints()