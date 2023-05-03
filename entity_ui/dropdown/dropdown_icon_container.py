from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity_ui.dropdown.dropdown_container import DropdownContainer

from common.draw_order import DrawOrder
from common.image_manager import ImageID
from entity_base.container_entity import Container
from entity_base.image.image_entity import ImageEntity
from entity_base.image.image_state import ImageState

"""
Defines the location of the dropdown icon
Left side of the top option
"""

class DropdownIconContainer(Container):
    
    def __init__(self, parent, dropdownContainer: DropdownContainer):
        super().__init__(parent)
        self.dropdownContainer = dropdownContainer

        ImageEntity(parent = self, 
            states = ImageState(0, ImageID.DROPDOWN_ICON),
            drawOrder = DrawOrder.DROPDOWN,
            disableTouching = True
        )

    def defineCenterX(self):
        return self._ax(self.dropdownContainer.ICON_LEFT_OFFSET)

    def defineCenterY(self):
        return self._py(0.5)
    
    def defineWidth(self):
        return self.defineHeight()
    
    def defineHeight(self):
        return self._pheight(self.dropdownContainer.ICON_SCALE)