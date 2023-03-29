from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from BaseEntity.EntityFunctions.click_function import Click
from BaseEntity.EntityFunctions.drag_function import Drag
from BaseEntity.EntityFunctions.select_function import Select
from BaseEntity.entity import Entity

from pygame_functions import drawLine
from math_functions import pointTouchingLine

import pygame

"""
Abstract class for a segment-type entity that connects two entities
"""

class SegmentEntity(Entity):
    def __init__(self, first: Entity, second: Entity, drag: Drag = None, select: Select = None, click: Click = None) -> None:
        super().__init__(drag = drag, select = select, click = click)

        self.first = first
        self.second = second