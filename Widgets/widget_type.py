from BaseEntity.EntityListeners.click_listener import ClickListener, ClickLambda
from BaseEntity.EntityListeners.drag_listener import DragListener, DragLambda
from BaseEntity.EntityListeners.select_listener import SelectListener, SelectLambda
from BaseEntity.EntityListeners.tick_listener import TickListener, TickLambda
from BaseEntity.EntityListeners.hover_listener import HoverListener, HoverLambda

from draw_order import DrawOrder

from abc import ABC, abstractmethod
from reference_frame import PointRef
import pygame

"""
A generic widget type (slider, checkbox, etc).
Does not hold information for things specific to a CommandDefinition (location, name)
If implementing this, use widgetEntity to get and set the widget value.
DO NOT STORE ANY INTERNAL STATE SPECIFIC TO INDIVIDUAL COMMANDS HERE
"""

class WidgetType:

    def __init__(self, drag: DragListener = None, select: SelectListener = None, click: ClickListener = None, tick: TickListener = None, hover: HoverListener = None, drawOrder: int = 0):
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