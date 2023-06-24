from __future__ import annotations
from typing import TYPE_CHECKING

from data_structures.observer import Observer
from entity_base.listeners.mousewheel_listener import MousewheelLambda
if TYPE_CHECKING:
    from root_container.path import Path

from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref

import entity_base.entity as entity
from common.draw_order import DrawOrder
from common.field_transform import FieldTransform
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.drag_listener import DragLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType

from utility.math_functions import distance
import pygame

"""
An entity for the field.
Passes events to fieldTransform, and subscribes to it to update entities on field
"""

class FieldContainer(entity.Entity, Observer):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, fieldTransform: FieldTransform):
        super().__init__(
            parent = entity.ROOT_CONTAINER,
            select = SelectLambda(self, "field", type = SelectorType.SOLO, deselectOnMouseUp = True),
            drag = DragLambda(self,
                              FonStartDrag = self.onStartDrag,
                              FonDrag = self.onDrag,
                              FonStopDrag = self.onStopDrag
                              ),
            click = ClickLambda(self, FonRightClick = self.onRightClick),
            mousewheel = MousewheelLambda(self, FonMousewheel = self.onMousewheel),
            drawOrder = DrawOrder.FIELD_BACKGROUND)
        self.fieldTransform = fieldTransform

        # Whenever field is dragged, update entities on field
        self.fieldTransform.subscribe(self, onNotify = self.recomputeEntity)

    def initPath(self, path: Path):
        self.path = path

    def onMousewheel(self, offset: int) -> bool:
        self.fieldTransform.changeZoom(self.mousewheel.mouseRef, offset * 0.01)

    def defineTopLeft(self) -> tuple:
        return 0, self.dimensions.TOP_HEIGHT

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self.dimensions.FIELD_WIDTH
    def defineHeight(self) -> float:
        return self.dimensions.FIELD_HEIGHT
    
    # Add a new node at location
    def onRightClick(self, mousePos: tuple):
        self.path.addNode(PointRef(Ref.SCREEN, mousePos))
    
    def onStartDrag(self, mousePos: tuple):
        self.startX, self.startY = mousePos
        self.fieldTransform.startPan()

    def onDrag(self, mousePos: tuple):
        mx, my = mousePos
        self.fieldTransform.updatePan(mx - self.startX, my - self.startY)

    def onStopDrag(self):
        pass
    
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):
        pygame.draw.rect(screen, (255, 255, 255), self.RECT)
        self.fieldTransform.draw(screen)
        self.drawRect(screen)