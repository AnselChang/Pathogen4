from __future__ import annotations
from typing import TYPE_CHECKING
from common.draw_order import DrawOrder
from entity_base.image.image_state import ImageState
if TYPE_CHECKING:
    from entities.root_container.panel_container.command_block.command_block_entity import CommandBlockEntity


from entity_base.listeners.click_listener import ClickLambda
from entities.root_container.panel_container.element.widget.widget_entity import WidgetContainer
from entities.root_container.panel_container.element.widget.widget_definition import WidgetDefinition
from entities.root_container.panel_container.element.row.element_definition import ElementType

from common.image_manager import ImageID
from common.reference_frame import PointRef, Ref
from utility.pygame_functions import drawSurface
from utility.math_functions import distance
from entity_base.image.image_entity import ImageEntity
import pygame


class CheckboxWidgetContainer(WidgetContainer['CheckboxWidgetDefinition']):

    def __init__(self, parent, parentCommand: CommandBlockEntity, definition: 'CheckboxWidgetDefinition'):

        super().__init__(parent, parentCommand, definition)
        
        states = [
            ImageState(True, ImageID.CHECKBOX_ON),
            ImageState(False, ImageID.CHECKBOX_OFF)
        ]
        self.checkbox = ImageEntity(self,
            states = states,
            getStateID = self.getValue,
            onClick = self.onLeftClick,
        )

    # toggle boolean value on left click
    def onLeftClick(self, mouse: tuple):
        self.setValue(not self.getValue())

    # widgets and readouts should not use ElementEntity width
    # because they are dynamic
    def defineWidth(self) -> float:
        return self.defineHeight()
    
    def defineHeight(self) -> float:
        return self._pheight(0.6)
    
    def draw(self,b,c,d):
        #print(self.checkbox.RECT)
        pass

    

class CheckboxWidgetDefinition(WidgetDefinition):

    def __init__(self, variableName: str, defaultOn: bool, tooltipOn: str = None, tooltipOff: str = None):
        super().__init__(ElementType.CHECKBOX, variableName, defaultOn)
        self.defaultOn = defaultOn
        self.tooltipOn = tooltipOn
        self.tooltipOff = tooltipOff

    def makeElement(self, parent, parentCommand, pathAdapter) -> CheckboxWidgetContainer:
        return CheckboxWidgetContainer(parent, parentCommand, self)