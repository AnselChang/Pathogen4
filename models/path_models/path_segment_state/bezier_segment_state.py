from __future__ import annotations
from enum import Enum, auto
import math
from typing import TYPE_CHECKING
from adapter.bezier_adapter import BezierAdapter
from adapter.path_adapter import PathAttributeID
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState

from models.path_models.path_segment_state.abstract_segment_state import AbstractSegmentState
from models.path_models.path_segment_state.segment_type import SegmentType
from models.path_models.segment_direction import SegmentDirection
from utility.format_functions import formatInches
from utility.math_functions import addTuples, arcFromThreePoints, distanceTuples, divideTuple, midpoint, pointPlusVector, scaleTuple, subtractTuples, thetaFromPoints

if TYPE_CHECKING:
    from models.path_models.path_segment_model import PathSegmentModel

"""
For bezier segments.
"""

class BezierIconID(Enum):
    BEZIER = auto()

class BezierSegmentState(AbstractSegmentState):

    def __init__(self, model: PathSegmentModel):

        adapter = BezierAdapter([
            ImageState(BezierIconID.BEZIER, ImageID.BEZIER),
        ])

        super().__init__(model, adapter, SegmentType.BEZIER)

        # stores the location of the two bezier control nodes as offsets from segment endpoints
        self.controlOffset1 = None
        self.controlOffset2 = None

    # get the location between nodes, with percent (0-1).
    # 0 means at first node, 1 means at second node
    def getLocationBetweenNodes(self, percent):
        before = self.model.getBeforePos()
        after = self.model.getAfterPos()
        offset = subtractTuples(after, before)
        scaledOffset = scaleTuple(offset, percent)
        return addTuples(before, scaledOffset)
    
    def onSwitchToState(self):
        
        # If first time switching to bezier, set control points to 1/3 and 2/3 of the way between nodes
        if self.controlOffset1 is None:
            pos1 = self.getLocationBetweenNodes(1/3)
            self.controlOffset1 = subtractTuples(pos1, self.model.getBeforePos())

            pos2 = self.getLocationBetweenNodes(2/3)
            self.controlOffset2 = subtractTuples(pos2, self.model.getAfterPos())

    # first control point is defined relative to before node
    def getControlPoint1(self) -> tuple:
        return addTuples(self.model.getBeforePos(), self.controlOffset1)
    
    # second control point is defined relative to after node
    def getControlPoint2(self) -> tuple:
        return addTuples(self.model.getAfterPos(), self.controlOffset2)
    
    def getControlOffset1(self) -> tuple:
        return self.controlOffset1
    
    def getControlOffset2(self) -> tuple:
        return self.controlOffset2
    
    def setControlOffset1(self, offset: tuple):
        self.controlOffset1 = offset
        self.model.updateThetas()
        self.model.recomputeUI()

    def setControlOffset2(self, offset: tuple):
        self.controlOffset2 = offset
        self.model.updateThetas()
        self.model.recomputeUI()

    def _update(self) -> tuple: # returns [startTheta, endTheta]

        before = self.model.getBeforePos()
        after = self.model.getAfterPos()

        # calculate thetas, based on angle to control points
        startTheta = thetaFromPoints(before, self.getControlPoint1())
        endTheta = thetaFromPoints(self.getControlPoint2(), after)

        return startTheta, endTheta
        
    def _defineCenterInches(self) -> tuple:
        return midpoint(self.model.getBeforePos(), self.model.getAfterPos())
    
    def _updateIcon(self):
        self.adapter.setIconStateID(BezierIconID.BEZIER)