from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.listeners.drag_listener import DragLambda
from entities.root_container.field_container.segment.bezier_line_entity import BezierLineEntity
from models.project_history_interface import ProjectHistoryInterface
from utility.math_functions import addTuples, distancePointToLine, hypo, thetaFromVector, vectorFromThetaAndMagnitude
if TYPE_CHECKING:
    from root_container.field_container.segment.bezier_segment_entity import BezierSegmentEntity
    from models.path_models.path_node_model import PathNodeModel

from entity_base.entity import Entity
from entity_base.listeners.hover_listener import HoverLambda

import pygame
from utility.pygame_functions import shade

"""
Moveable control point for bezier curves. There are two of these per curve.
Does not store state, but reads and writes to SegmentModel through BezierSegmentState
"""

class BezierNodeEntity(Entity):

    def __init__(self, segment: BezierSegmentEntity, isFirstControlPoint: bool):

        super().__init__(parent = segment,
            hover = HoverLambda(self),
            drag = DragLambda(self, selectEntityNotThis = segment, FonStartDrag = self.onStartDrag, FonDrag = self.onDrag, FonStopDrag = self.onStopDrag),
        )

        self.field = segment.field
        self.segment = segment
        self.model = segment.model

        self.COLOR = [255, 0, 255]
        self.COLOR_H = shade(self.COLOR, 0.9)

        self.RADIUS = 5
        self.RADIUS_H = 6

        self.isFirst = isFirstControlPoint

        # draw line from node to control point
        BezierLineEntity(self)

    def getNeighborNode(self) -> PathNodeModel:
        if self.isFirst:
            return self.segment.model.getPrevious()
        else:
            return self.segment.model.getNext()

    def getPosition(self):
        state = self.segment.getBezierState()
        return state.getControlPoint1() if self.isFirst else state.getControlPoint2()

    def getOffset(self):
        state = self.segment.getBezierState()
        return state.getControlOffset1() if self.isFirst else state.getControlOffset2()

    def onStartDrag(self, mouse: tuple):

        # initialize start offset to calculate offset while dragging
        self.startOffset = self.getOffset()

        # old slow bezier curve is now out-of-date
        self.segment.getBezierState().resetBezierSlow()

        # recalculate constraints for corresponding node
        if self.isFirst:
            self.model.initBeforeThetaConstraints()
        else:
            self.model.initAfterThetaConstraints()

    def onDrag(self, mouse: tuple):

        # First, find the new offset after dragging
        state = self.segment.getBezierState()

        offsetPixels = [self.drag.totalOffsetX, self.drag.totalOffsetY]
        offsetInches = self.field.mouseToInchesScaleOnly(offsetPixels)

        offset = addTuples(self.startOffset, offsetInches)
        
        # constrain bezier control points to be parallel with snappable angles
        offsetTheta = thetaFromVector(offset)
        offsetMagnitude = hypo(*offset)
        newOffsetTheta = state.getConstraintsSolver(self.isFirst).constrainAngle(offsetTheta)

        # recalculate offset if snapping
        if newOffsetTheta is not None:
            offset = vectorFromThetaAndMagnitude(newOffsetTheta, offsetMagnitude)

        # update model
        state.setControlOffset1(offset) if self.isFirst else state.setControlOffset2(offset)

        # Then, recompute the bezier curve (fast only for drawing)
        self.segment.getBezierState().updateBezierFast()

    # there's time to recompute the slow bezier curve once on mouse release
    def onStopDrag(self):
        self.segment.getBezierState().updateBezierSlow()
        self.segment.recomputeEntity()

        # make a save state
        ProjectHistoryInterface.getInstance().save()

    def defineCenter(self) -> tuple:
        return self.field.inchesToMouse(self.getPosition())
    
    def isTouching(self, position: tuple) -> bool:

        if not self.segment.isBezierHovered():
            return

        MARGIN = 4
        return self.distanceTo(position) <= self.RADIUS + MARGIN
    
    def getColor(self) -> tuple:
        return self.COLOR_H if self.hover.isHovering else self.COLOR
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        if not self.segment.isBezierHovered():
            return
        
        RADIUS = self.RADIUS_H if self.hover.isHovering else self.RADIUS
        POSITION = [self.CENTER_X, self.CENTER_Y]
        pygame.draw.circle(screen, self.getColor(), POSITION, RADIUS)