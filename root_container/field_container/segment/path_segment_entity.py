from __future__ import annotations
from typing import TYPE_CHECKING
from data_structures.observer import Observer
from entity_base.listeners.tick_listener import TickLambda
from models.path_models.path_segment_model import PathSegmentModel
from root_container.field_container.field_entity import FieldEntity
from root_container.field_container.node.arc_curve_node import ArcCurveNode
from root_container.field_container.node.bezier_lines import BezierLines
from root_container.field_container.node.bezier_theta_node import BezierThetaNode

from root_container.field_container.segment.segment_type import PathSegmentType
if TYPE_CHECKING:
    from root_container.path import Path

from entity_base.listeners.drag_listener import DragLambda
from models.path_models.segment_direction import SegmentDirection
from utility.math_functions import isInsideBox
if TYPE_CHECKING:

from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref, VectorRef

from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType
from entity_base.entity import Entity

from root_container.field_container.segment.path_segment_state import PathSegmentState
from root_container.field_container.segment.PathSegmentStates.bezier_segment_state import BezierSegmentState
from root_container.field_container.segment.PathSegmentStates.arc_segment_state import ArcSegmentState
from root_container.field_container.segment.PathSegmentStates.straight_segment_state import StraightSegmentState

from adapter.path_adapter import PathAdapter, AdapterInterface

from data_structures.linked_list import LinkedListNode

from common.draw_order import DrawOrder
from utility.pygame_functions import shade, drawLine
import pygame

"""
Acts as a "context" class in the state design pattern. Owns PathSegmentState objects
that define behavior for straight/arc/bezier shapes. Easy to switch between states
We also define the constants that apply across all segment types here, like color and thickness
"""

class PathSegmentEntity(Entity):
    def __init__(self, field: FieldEntity, model: PathSegmentModel):
        self.model = model
        self.field = field
        super().__init__(parent = field)


        self.COLOR = (0, 255, 0)
        self.THICKNESS = 3

    def defineAfter(self) -> None:
        self.beforePos = self.field.inchesToMouse(self.model.getBeforePos())
        self.afterPos = self.field.inchesToMouse(self.model.getAfterPos())

    def draw(self, screen, isActive, isHovering):
        
        # draw segment from beforePos to afterPos
        drawLine(screen, self.COLOR, *self.beforePos, *self.afterPos, self.THICKNESS)