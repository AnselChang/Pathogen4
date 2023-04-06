from UIEntities.Generic.radio_group_entity import RadioGroupEntity
from dimensions import Dimensions

"""
The expand and collapse buttons on the bottom of the panel
Child of Panel Entity
"""
class ExpansionGroupEntity(RadioGroupEntity):

    def defineCenterX(self) -> float:
        return self._px(0.5)
    
    def defineBottomY(self) -> float:
        return self._py(1)

    def defineWidth(self) -> float:
        return self._pwidth(0)
    def defineHeight(self) -> float:
        return self._pheight(0.1)