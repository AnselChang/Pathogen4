from Widgets.widget_type import WidgetType

from image_manager import ImageID
from reference_frame import PointRef, Ref
from pygame_functions import drawSurface
from Tooltips.tooltip import Tooltip
import pygame


"""
Click to toggle on or off
"""

class CheckboxWidget(WidgetType):

    def __init__(self, tooltipOn: str = None, tooltipOff: str = None):
        if tooltipOn is None:
            self.tooltipOn = None
        else:
            self.tooltipOn = Tooltip(tooltipOn)

        if tooltipOff is None:
            self.tooltipOff = None
        else:
            self.tooltipOff = Tooltip(tooltipOff)

    def getDefaultValue(self) -> float:
        return False

    def isTouching(self, widgetEntity, position: PointRef) -> bool:
         distance = (widgetEntity.getPosition() - position).magnitude(Ref.SCREEN)
         return distance < 12

    def draw(self, widgetEntity, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        x, y = widgetEntity.getPosition().screenRef

        if widgetEntity.getValue():
            id = ImageID.CHECKBOX_ON_H if isHovered else ImageID.CHECKBOX_ON
        else:
            id = ImageID.CHECKBOX_OFF_H if isHovered else ImageID.CHECKBOX_OFF

        drawSurface(screen, widgetEntity.getImage(id, widgetEntity.getOpacity()), x, y)

    def getTooltip(self, widgetEntity) -> Tooltip | None:
        return self.tooltipOn if widgetEntity.getValue() else self.tooltipOff

    def onLeftClick(self, widgetEntity):
        widgetEntity.setValue(not widgetEntity.getValue())