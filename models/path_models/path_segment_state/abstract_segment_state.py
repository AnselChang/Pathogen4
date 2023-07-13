from __future__ import annotations
from typing import TYPE_CHECKING

from adapter.path_adapter import AdapterState, PathAdapter

from typing import TypeVar, Generic

from models.path_models.path_segment_state.segment_type import SegmentType
from serialization.serializable import Serializable, SerializedState

if TYPE_CHECKING:
    from models.path_models.path_segment_model import PathSegmentModel

"""
An interface for some segment shape, ie Straight, Arc, Bezier.
"""

class SerializedSegmentStateState(SerializedState):

    def __init__(self, adapterState: AdapterState):
        self.adapter = adapterState

    def deserialize(self, model: PathSegmentModel) -> 'AbstractSegmentState':
        raise NotImplementedError()

T = TypeVar('T')
class AbstractSegmentState(Serializable, Generic[T]):

    def __init__(self, model: PathSegmentModel, adapter: PathAdapter, type: SegmentType):
        self.model = model
        self.adapter: PathAdapter | T = adapter
        self.type = type

        self.START_THETA = None
        self.END_THETA = None

    def onUpdate(self):
        self.START_THETA, self.END_THETA = self._update()
        self._updateIcon()

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
    
    def _updateIcon(self):
        raise NotImplementedError()

    # can overwrite this to specify behavior when transition to this state
    def onSwitchToState(self):
        pass