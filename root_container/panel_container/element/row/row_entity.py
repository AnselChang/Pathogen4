from entity_ui.group.linear_container import LinearContainer
from root_container.panel_container.element.row.row_group_entity import RowGroupEntity
from entity_base.text_entity import TextEntity

"""
A single row of the command block containing a label on the left column and
a widget or readout on the right column
"""

class RowEntity(LinearContainer):
    
    def __init__(self, group: RowGroupEntity, id):
        super().__init__(group, id)        

    def defineWidth(self) -> float:
        return self._pwidth(0.95)
    
    def defineHeight(self) -> float:
        return self._pheight(0.9)