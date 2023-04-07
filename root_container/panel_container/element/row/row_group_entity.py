from entity_base.entity import Entity
from entity_ui.group.linear_group_entity import LinearGroupEntity

"""
Manages all the rows of the command block
Each row has a left column (label), and right column (widget or readout)
"""

class RowGroupEntity(LinearGroupEntity):
    
    def __init__(self, parent: Entity):

        super().__init__(parent, isHorizontal = False)