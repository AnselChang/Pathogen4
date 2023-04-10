
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
    
    def __init__(self, parent):
        super().__init__(parent)

        self.recomputePosition()

        ImageEntity(parent = self, 
            states = ImageState(0, ImageID.DROPDOWN_ICON),
            drawOrder = DrawOrder.DROPDOWN_TEXT,
        )

    def defineCenterX(self):
        return self._ax(7)

    def defineCenterY(self):
        return self._py(0.5)
    
    def defineWidth(self):
        return self.defineHeight()
    
    def defineHeight(self):
        return self._pheight(0.6)