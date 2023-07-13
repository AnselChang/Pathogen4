from __future__ import annotations
from enum import Enum, auto
import math
from typing import TYPE_CHECKING
from adapter.bezier_adapter import BezierAdapter
from adapter.path_adapter import AdapterState, PathAttributeID
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState

from models.path_models.path_segment_state.abstract_segment_state import AbstractSegmentState, SerializedSegmentStateState
from models.path_models.path_segment_state.segment_type import SegmentType
from models.path_models.segment_direction import SegmentDirection
from utility.bezier_functions_2 import fast_points_cubic_bezier, normalized_points_cubic_bezier
from utility.format_functions import formatInches
from utility.math_functions import addTuples, arcFromThreePoints, distanceTuples, divideTuple, midpoint, pointPlusVector, scaleTuple, subtractTuples, thetaFromPoints

if TYPE_CHECKING:
    from models.path_models.path_segment_model import PathSegmentModel

"""
For bezier segments.
"""
class SerializedBezierState(SerializedSegmentStateState):

    def __init__(self, adapterState: AdapterState, controlOffset1, controlOffset2):
        super().__init__(adapterState)
        self.controlOffset1 = controlOffset1
        self.controlOffset2 = controlOffset2

    def deserialize(self, model: PathSegmentModel) -> 'BezierSegmentState':
        bez = BezierSegmentState(model)
        bez.adapter = self.adapter.deserialize()
        bez.controlOffset1 = self.controlOffset1
        bez.controlOffset2 = self.controlOffset2
        return bez

class BezierIconID(Enum):
    BEZIER = auto()

class BezierSegmentState(AbstractSegmentState):

    def serialize(self) -> SerializedBezierState:
        return SerializedBezierState(self.adapter.serialize(), self.controlOffset1, self.controlOffset2)

    def __init__(self, model: PathSegmentModel):

        adapter = BezierAdapter([
            ImageState(BezierIconID.BEZIER, ImageID.BEZIER),
        ])

        super().__init__(model, adapter, SegmentType.BEZIER)

        # stores the location of the two bezier control nodes as offsets from segment endpoints
        self.controlOffset1 = None
        self.controlOffset2 = None

        self.FAST_POINTS: list[tuple] = None # cubic bezier
        self.SLOW_POINTS: list[tuple] = None # cubic bezier with arc length parametrization

        # higher is more detailed
        self.FAST_RESOLUTION = 0.3

        # lower is more detailed. each segment is that length in inches
        self.SLOW_RESOLUTION_INCHES = 0.5

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

            self.updateBezierSlow()

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
        self.model.getPrevious().onThetaChange()
        self.model.recomputeUI()

    def setControlOffset2(self, offset: tuple):
        self.controlOffset2 = offset
        self.model.updateThetas()
        self.model.getNext().onThetaChange()
        self.model.recomputeUI()

    def getConstraintsSolver(self, isFirst: bool):
        if isFirst:
            return self.model.bConstraints
        else:
            return self.model.aConstraints

    # return slow bezier points if it exists. Otherwise, return fast bezier points
    def getBezierPoints(self) -> list[tuple]:
        if self.SLOW_POINTS is not None:
            return self.SLOW_POINTS
        elif self.FAST_POINTS is not None:
            return self.FAST_POINTS
        else:
            raise Exception("Bezier points not defined")
    
    # return mouse points for hovering over bezier if it exists
    def getBezierMousePoints(self) -> list[tuple]:
        return self.FAST_POINTS

    # reset slow bezier points when they are no longer valid (user is dragging control points)
    def resetBezierSlow(self):
        self.SLOW_POINTS = None

    # generate a list of bezier points, for drawing while dragging
    # uses fast cubic bezier generation without arc length parameterization
    def updateBezierFast(self):

        p0 = self.model.getBeforePos()
        p1 = self.getControlPoint1()
        p2 = self.getControlPoint2()
        p3 = self.model.getAfterPos()

        self.FAST_POINTS = fast_points_cubic_bezier(self.FAST_RESOLUTION, p0, p1, p2, p3)

    def updateBezierSlow(self):

        p0 = self.model.getBeforePos()
        p1 = self.getControlPoint1()
        p2 = self.getControlPoint2()
        p3 = self.model.getAfterPos()
        
        self.SLOW_POINTS = normalized_points_cubic_bezier(self.SLOW_RESOLUTION_INCHES, p0, p1, p2, p3)

    def _update(self) -> tuple: # returns [startTheta, endTheta]

        before = self.model.getBeforePos()
        after = self.model.getAfterPos()

        # calculate thetas, based on angle to control points
        startTheta = thetaFromPoints(before, self.getControlPoint1())
        endTheta = thetaFromPoints(self.getControlPoint2(), after)

        self.updateBezierFast()

        return startTheta, endTheta
        
    def _defineCenterInches(self) -> tuple:
        return midpoint(self.model.getBeforePos(), self.model.getAfterPos())
    
    def _updateIcon(self):
        self.adapter.setIconStateID(BezierIconID.BEZIER)