from BaseEntity.EntityListeners.click_listener import ClickLambda
from Widgets.widget_entity import WidgetEntity
from Widgets.widget_definition import WidgetDefinition

from image_manager import ImageID
from reference_frame import PointRef, Ref
from pygame_functions import drawSurface
from Tooltips.tooltip import Tooltip, TooltipOwner
import pygame


class CheckboxWidgetEntity(WidgetEntity, TooltipOwner):

    def __init__(self, parentCommand, definition: 'CheckboxWidgetDefinition'):

        super().__init__(parentCommand, definition,
                         click = ClickLambda(self, FonLeftClick = self.onLeftClick)
                         )

        if definition.tooltipOn is None:
            self.tooltipOn = None
        else:
            self.tooltipOn = Tooltip(definition.tooltipOn)

        if definition.tooltipOff is None:
            self.tooltipOff = None
        else:
            self.tooltipOff = Tooltip(definition.tooltipOff)

    def getDefaultValue(self) -> float:
        return False

    def isTouchingWidget(self, position: PointRef) -> bool:
         distance = (self.getPosition() - position).magnitude(Ref.SCREEN)
         return distance < 12

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        x, y = self.getPosition().screenRef

        if self.getValue():
            id = ImageID.CHECKBOX_ON_H if isHovered else ImageID.CHECKBOX_ON
        else:
            id = ImageID.CHECKBOX_OFF_H if isHovered else ImageID.CHECKBOX_OFF

        image = self.images.get(id, self.getOpacity())
        drawSurface(screen, image, x, y)

    def getTooltip(self) -> Tooltip | None:
        return self.tooltipOn if self.getValue() else self.tooltipOff

    def onLeftClick(self):
        self.setValue(not self.getValue())

class CheckboxWidgetDefinition(WidgetDefinition):

    def __init__(self, name: str, px: int, py: int, tooltipOn: str = None, tooltipOff: str = None):
        super().__init__(name, px, py)
        self.tooltipOn = tooltipOn
        self.tooltipOff = tooltipOff

    def make(self, parentCommand) -> CheckboxWidgetEntity:
        return CheckboxWidgetEntity(parentCommand, self)