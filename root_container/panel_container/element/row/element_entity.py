from entity_base.entity import Entity
from entity_base.text_entity import TextEntity

"""
Either a widget or readout. Inside a RowEntity, the label is always on the right column
"""

class ElementEntity(Entity):

    def __init__(self, parent):
        super().__init__(parent)

    def defineCenter(self) -> tuple:
        return self._px(0.775), self._py(0.5)

    # widgets and readouts should not use ElementEntity width
    # because they are dynamic
    def defineWidth(self) -> float:
        return self._pwidth(0)
    
    def defineHeight(self) -> float:
        return self._pheight(1)