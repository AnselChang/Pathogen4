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