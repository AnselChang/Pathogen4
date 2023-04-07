from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity


from entity_base.listeners.click_listener import ClickLambda
from root_container.panel_container.element.widget.widget_entity import WidgetEntity
from root_container.panel_container.element.widget.widget_definition import WidgetDefinition

from common.image_manager import ImageID
from common.reference_frame import PointRef, Ref
from utility.pygame_functions import drawSurface
from utility.math_functions import distance
from entity_ui.tooltip import Tooltip, TooltipOwner
import pygame


class CheckboxWidgetEntity(WidgetEntity['CheckboxWidgetDefinition'], TooltipOwner):

    def __init__(self, parent, parentCommand: CommandBlockEntity, definition: 'CheckboxWidgetDefinition'):

        super().__init__(parent, parentCommand, definition,
                         click = ClickLambda(self, FonLeftClick = self.onLeftClick)
                         )

        self.value = definition.defaultOn

        self.onModifyDefinition()


    def getValue(self) -> float:
        return self.value
    
    def onModifyDefinition(self):
        if self.definition.tooltipOn is None:
            self.tooltipOn = None
        else:
            self.tooltipOn = Tooltip(self.definition.tooltipOn)

        if self.definition.tooltipOff is None:
            self.tooltipOff = None
        else:
            self.tooltipOff = Tooltip(self.definition.tooltipOff)

    def isTouchingWidget(self, position: tuple) -> bool:
         return self.distanceTo(position) < 12

    def drawWidget(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        if self.getValue():
            id = ImageID.CHECKBOX_ON_H if isHovered else ImageID.CHECKBOX_ON
        else:
            id = ImageID.CHECKBOX_OFF_H if isHovered else ImageID.CHECKBOX_OFF

        image = self.images.get(id, self.getOpacity())
        drawSurface(screen, image, self.CENTER_X, self.CENTER_Y)

    def getTooltip(self) -> Tooltip | None:
        return self.tooltipOn if self.getValue() else self.tooltipOff

    def onLeftClick(self):
        self.value = not self.value

class CheckboxWidgetDefinition(WidgetDefinition):

    def __init__(self, name: str, px: int, py: int, defaultOn: bool, tooltipOn: str = None, tooltipOff: str = None):
        super().__init__(name, px, py)
        self.defaultOn = defaultOn
        self.tooltipOn = tooltipOn
        self.tooltipOff = tooltipOff

    def makeElement(self, parent, parentCommand, pathAdapter) -> CheckboxWidgetEntity:
        return CheckboxWidgetEntity(parent, parentCommand, self)