from entity_ui.group.radio_group_container import RadioGroupContainer
from root_container.panel_container.panel_container import PanelContainer
from root_container.panel_container.tab.tab_entity import TabEntity
from common.dimensions import Dimensions

"""a group of radio_entities, where only one is selected at a time
If allowNoSelect is True, then no option being selected is allowed
Child of Panel Entity
"""
class TabGroupEntity(RadioGroupContainer):

    def __init__(self, parentPanel: PanelContainer):
        super().__init__(parentPanel, isHorizontal = True, allowNoSelect = False)

    def defineTopLeft(self) -> tuple:
        return self._px(0), self._py(0)

    def defineWidth(self) -> float:
        return self._pwidth(1)
    def defineHeight(self) -> float:
        return self._pheight(0.05)