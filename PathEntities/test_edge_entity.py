from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from BaseEntity.EntityFunctions.click_function import Click
from BaseEntity.EntityFunctions.drag_function import Drag
from BaseEntity.EntityFunctions.select_function import Select
from BaseEntity.entity import Entity
from PathEntities.line_connector_entity import LineConnectorEnttiy


import pygame

class TestEdgeEntity(LineConnectorEnttiy):
    def __init__(self, first: Entity, second: Entity, drag: Drag = None, select: Select = None, click: Click = None) -> None:
        super().__init__(first = first,
                         second = second,
                         hitboxThickness = 5,
                         drag = drag,
                         select = select,
                         click = click)
    
    def getColor(self, isActive: bool, isHovered: bool) -> tuple:
        if isHovered:
            return [200, 200, 200]
        else:
            return [100,100,100]

    def getThickness(self, isActive: bool, isHovered: bool) -> int:
        return 3