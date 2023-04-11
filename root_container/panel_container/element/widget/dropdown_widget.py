from __future__ import annotations
from typing import TYPE_CHECKING
from common.draw_order import DrawOrder
from common.font_manager import FontID
from entity_base.image.image_state import ImageState
from entity_ui.dropdown.dropdown_container import DropdownContainer
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity


from entity_base.listeners.click_listener import ClickLambda
from root_container.panel_container.element.widget.widget_entity import WidgetContainer
from root_container.panel_container.element.widget.widget_definition import WidgetDefinition

from common.image_manager import ImageID
from common.reference_frame import PointRef, Ref
from utility.pygame_functions import drawSurface
from utility.math_functions import distance
from entity_base.image.image_entity import ImageEntity
import pygame


class DropdownWidgetContainer(WidgetContainer['DropdownWidgetDefinition']):

    def __init__(self, parent, parentCommand: CommandBlockEntity, definition: 'DropdownWidgetDefinition'):

        super().__init__(parent, parentCommand, definition)

        self.recomputePosition()
        
        colorSelectedHovered = [176, 200, 250]
        colorSelected = [176, 200, 250]
        colorHovered = [52, 132, 240]
        colorOff = [196, 219, 250]
        self.dropdown = DropdownContainer(self, definition.options, FontID.FONT_NORMAL, 11,
                                          colorSelectedHovered, colorSelected, colorHovered, colorOff,
                                          dynamicWidth = False, verticalTextPadding = 1)

    def getValue(self) -> bool:
        return self.dropdown.getSelectedOptionText()

class DropdownWidgetDefinition(WidgetDefinition):

    def __init__(self, variableName: str, options: list[str]):
        super().__init__(variableName)
        self.options = options

    def makeElement(self, parent, parentCommand, pathAdapter) -> DropdownWidgetContainer:
        return DropdownWidgetContainer(parent, parentCommand, self)