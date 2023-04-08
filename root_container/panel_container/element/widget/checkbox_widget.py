from __future__ import annotations
from typing import TYPE_CHECKING
from common.draw_order import DrawOrder
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity


from entity_base.listeners.click_listener import ClickLambda
from root_container.panel_container.element.widget.widget_entity import WidgetContainer
from root_container.panel_container.element.widget.widget_definition import WidgetDefinition

from common.image_manager import ImageID
from common.reference_frame import PointRef, Ref
from utility.pygame_functions import drawSurface
from utility.math_functions import distance
from entity_base.image.toggle_image_entity import ToggleImageEntity
import pygame


class CheckboxWidgetContainer(WidgetContainer['CheckboxWidgetDefinition']):

    def __init__(self, parent, parentCommand: CommandBlockEntity, definition: 'CheckboxWidgetDefinition'):

        super().__init__(parent, parentCommand, definition)

        self.value = definition.defaultOn

        self.recomputePosition()

        self.checkbox = ToggleImageEntity(self,
            ImageID.CHECKBOX_ON, ImageID.CHECKBOX_OFF,
            drawOrder = DrawOrder.WIDGET,
            onClick = self.onLeftClick,
            isOn = self.getValue
            )

    def getValue(self) -> bool:
        return self.value

    def onLeftClick(self, mouse: tuple):
        
        self.value = not self.value

    # widgets and readouts should not use ElementEntity width
    # because they are dynamic
    def defineWidth(self) -> float:
        return self._pheight(0.8)
    
    def defineHeight(self) -> float:
        return self._pheight(0.8)
    
    def draw(self,b,c,d):
        #print(self.checkbox.RECT)
        pass

    

class CheckboxWidgetDefinition(WidgetDefinition):

    def __init__(self, variableName: str, defaultOn: bool, tooltipOn: str = None, tooltipOff: str = None):
        super().__init__(variableName)
        self.defaultOn = defaultOn
        self.tooltipOn = tooltipOn
        self.tooltipOff = tooltipOff

    def makeElement(self, parent, parentCommand, pathAdapter) -> CheckboxWidgetContainer:
        return CheckboxWidgetContainer(parent, parentCommand, self)