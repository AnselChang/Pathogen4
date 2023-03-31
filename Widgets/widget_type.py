from BaseEntity.EntityListeners.click_listener import Click, ClickLambda
from BaseEntity.EntityListeners.drag_listener import Drag, DragLambda
from BaseEntity.EntityListeners.select_listener import Select, SelectLambda
from BaseEntity.EntityListeners.tick_listener import Tick, TickLambda
from BaseEntity.EntityListeners.hover_listener import Hover, HoverLambda

from draw_order import DrawOrder

from abc import ABC, abstractmethod
from reference_frame import PointRef
import pygame

"""
A generic widget type (slider, checkbox, etc).
Does not hold information for things specific to a CommandDefinition (location, name)
"""

class WidgetType:

    def __init__(self, drag: Drag = None, select: Select = None, click: Click = None, tick: Tick = None, hover: Hover = None, drawOrder: int = 0):
        self.drag = drag
        self.select = select
        self.click = click
        self.tick = tick

    @abstractmethod
    def getDefaultName(self) -> str:
        pass

    @abstractmethod
    def getDefaultValue(self) -> float:
        pass

    @abstractmethod
    def isTouching(self, widgetEntity, position: PointRef) -> bool:
        pass

    @abstractmethod
    def draw(self, widgetEntity, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pass

    def onLeftClick(self, widgetEntity):
        pass

    def onRightClick(self, widgetEntity):
        pass

    def onStartDrag(self, widgetEntity):
        pass

    def onDragOffset(self, widgetEntity):
        pass

    def onStopDrag(self, widgetEntity):
        pass