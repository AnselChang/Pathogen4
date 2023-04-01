from Widgets.widget_type import WidgetType

from image_manager import ImageID
from reference_frame import PointRef, Ref
from pygame_functions import drawSurface
import pygame


"""
Click to toggle on or off
"""

class CheckboxWidget(WidgetType):

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

    def onLeftClick(self, widgetEntity):
        widgetEntity.setValue(not widgetEntity.getValue())