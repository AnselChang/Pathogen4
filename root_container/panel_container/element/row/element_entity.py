from entity_base.text_entity import TextEntity
from root_container.panel_container.element.row.row_entity import RowEntity

"""
Either a widget or readout. Inside a RowEntity, the label is always on the right column
"""

class ElementEntity(TextEntity):

    def __init__(self, parent: RowEntity):
        super().__init__(parent)

    def defineCenter(self) -> tuple:
        return self._px(0.7), self._py(0.5)

    def defineWidth(self) -> float:
        return self._pwidth(0.3)
    
    def defineHeight(self) -> float:
        return self._pheight(1)