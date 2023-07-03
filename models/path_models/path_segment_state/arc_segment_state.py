from __future__ import annotations
from enum import Enum, auto
from typing import TYPE_CHECKING
from adapter.arc_adapter import ArcAdapter
from adapter.straight_adapter import StraightAdapter
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState

from models.path_models.path_segment_state.abstract_segment_state import AbstractSegmentState
from models.path_models.path_segment_state.segment_type import SegmentType
from models.path_models.segment_direction import SegmentDirection
from utility.math_functions import distanceTuples, divideTuple, midpoint, thetaFromPoints

if TYPE_CHECKING:
    from models.path_models.path_segment_model import PathSegmentModel

"""
For straight segments. In this case, calculating thetas is just
the angle between the start and end points
"""

class ArcIconID(Enum):
    FORWARD_LEFT = auto()
    FORWARD_RIGHT = auto()
    REVERSE_LEFT = auto()
    REVERSE_RIGHT = auto()

class ArcSegmentState(AbstractSegmentState):

    def __init__(self, model: PathSegmentModel):

        adapter = ArcAdapter([
            ImageState(ArcIconID.FORWARD_LEFT, ImageID.CURVE_LEFT_FORWARD),
            ImageState(ArcIconID.FORWARD_RIGHT, ImageID.CURVE_RIGHT_FORWARD),
            ImageState(ArcIconID.REVERSE_LEFT, ImageID.CURVE_LEFT_REVERSE),
            ImageState(ArcIconID.REVERSE_RIGHT, ImageID.CURVE_RIGHT_REVERSE),
        ])

        super().__init__(model, adapter, SegmentType.ARC)

        
    def _update(self) -> tuple: # returns [startTheta, endTheta]
        before = self.model.getBeforePos()
        after = self.model.getAfterPos()
        theta = thetaFromPoints(before, after)

        distance = distanceTuples(before, after)

        # straight segments have a constant theta from start to end
        return theta, theta, distance
    
    def _defineCenterInches(self) -> tuple:
        return midpoint(self.model.getBeforePos(), self.model.getAfterPos())