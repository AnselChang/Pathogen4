from __future__ import annotations
from typing import TYPE_CHECKING
from adapter.path_adapter import AdapterState
from adapter.straight_adapter import StraightAdapter
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState

from models.path_models.path_segment_state.abstract_segment_state import AbstractSegmentState, SerializedSegmentStateState
from models.path_models.path_segment_state.segment_type import SegmentType
from models.path_models.segment_direction import SegmentDirection
from utility.math_functions import distanceTuples, divideTuple, midpoint, thetaFromPoints

if TYPE_CHECKING:
    from models.path_models.path_segment_model import PathSegmentModel

"""
For straight segments. In this case, calculating thetas is just
the angle between the start and end points
"""

class SerializedStraightState(SerializedSegmentStateState):

    def __init__(self, adapterState: AdapterState):
        super().__init__(adapterState)

    def deserialize(self, model: PathSegmentModel) -> 'StraightSegmentState':
        straight = StraightSegmentState(model)
        straight.adapter = self.adapter.deserialize()
        return straight

class StraightSegmentState(AbstractSegmentState):

    def serialize(self) -> SerializedStraightState:
        return SerializedStraightState(self.adapter.serialize())

    def __init__(self, model: PathSegmentModel):

        adapter = StraightAdapter([
            ImageState(SegmentDirection.FORWARD, ImageID.STRAIGHT_FORWARD),
            ImageState(SegmentDirection.REVERSE, ImageID.STRAIGHT_REVERSE),
        ])

        super().__init__(model, adapter, SegmentType.STRAIGHT)

        
    def _update(self) -> tuple: # returns [startTheta, endTheta]
        before = self.model.getBeforePos()
        after = self.model.getAfterPos()
        theta = thetaFromPoints(before, after)

        # straight segments have a constant theta from start to end
        return theta, theta
    
    def _updateIcon(self):
        self.adapter.setIconStateID(self.model.getDirection())
    
    def _defineCenterInches(self) -> tuple:
        return midpoint(self.model.getBeforePos(), self.model.getAfterPos())