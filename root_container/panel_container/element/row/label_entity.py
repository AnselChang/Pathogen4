from entity_base.text_entity import TextEntity
from root_container.panel_container.element.row.row_entity import RowEntity

"""
A subclass of TextEntity. Inside a RowEntity, the label is always on the left column
"""

class LabelEntity(TextEntity):

    def __init__(self, parent: RowEntity, font, size, staticText: str = None):
        super().__init__(parent, font, size, staticText)

    def defineCenter(self) -> tuple:
        return self._px(0.3), self._py(0.5)

    # widgets and readouts should not use ElementEntity width
    # because they are dynamic
    def defineWidth(self) -> float:
        return self._pwidth(0)
    
    def defineHeight(self) -> float:
        return self._pheight(1)