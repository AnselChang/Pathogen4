from UIEntities.Generic.radio_group_entity import RadioGroupEntity
from dimensions import Dimensions

"""a group of radio_entities, where only one is selected at a time
If allowNoSelect is True, then no option being selected is allowed
Child of Panel Entity
"""
class TabGroupEntity(RadioGroupEntity):

    def defineTopLeft(self) -> tuple:
        return self._px(0), self._py(0)

    def defineWidth(self) -> float:
        return self._pwidth(0)
    def defineHeight(self) -> float:
        return self._pheight(0.05)