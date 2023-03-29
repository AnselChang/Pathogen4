from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from BaseEntity.EntityFunctions.click_function import Click
from BaseEntity.EntityFunctions.drag_function import Drag
from BaseEntity.EntityFunctions.select_function import Select
from BaseEntity.entity import Entity
from PathEntities.segment_entity import SegmentEntity
from draw_order import DrawOrder

from pygame_functions import drawLine
from math_functions import pointTouchingLine

import pygame

"""
Segments specifically for connecting path nodes
Subclasses are responsbible for defining the shape (straight/arc/bezier) and drawing the segment
This class provides an interface for getting thetas at both sides, and holding references to nodes
"""

class PathSegmentEntity(SegmentEntity):
    def __init__(self, first: Entity, second: Entity, drag: Drag = None, select: Select = None, click: Click = None) -> None:
        super().__init__(first, second, drag = drag, select = select, click = click, drawOrder = DrawOrder.SEGMENT)

