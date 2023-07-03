from __future__ import annotations
from typing import TYPE_CHECKING

from adapter.path_adapter import PathAdapter

from typing import TypeVar, Generic

from models.path_models.path_segment_state.segment_type import SegmentType

if TYPE_CHECKING:
    from models.path_models.path_segment_model import PathSegmentModel

"""
An interface for some segment shape, ie Straight, Arc, Bezier.
"""

T = TypeVar('T')
class AbstractSegmentState(Generic[T]):

    def __init__(self, model: PathSegmentModel, adapter: PathAdapter, type: SegmentType):
        self.model = model
        self.adapter: PathAdapter | T = adapter
        self.type = type

        self.START_THETA = None
        self.END_THETA = None

    def onUpdate(self):
        self.START_THETA, self.END_THETA = self._update()

    def getStartTheta(self) -> float:
        return self.START_THETA
    
    def getEndTheta(self) -> float:
        return self.END_THETA
    
    def getAdapter(self) -> PathAdapter | T:
        return self.adapter
    
    def getType(self) -> SegmentType:
        return self.type

    """
    Update startTheta, endTheta, distance
    """
    def _update(self) -> tuple: # returns [startTheta, endTheta, distance]
        raise NotImplementedError()
    
    def _defineCenterInches(self) -> tuple:
        raise NotImplementedError()


    
