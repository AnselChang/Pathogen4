from root_container.panel_container.panel_container import PanelContainer
from root_container.panel_container.tab.tab_entity import TabEntity
from root_container.panel_container.tab.tab_group_entity import TabGroupEntity
from entity_ui.group.radio_container import RadioContainer

"""
Manage correct instantiation of tabs
"""

class TabHandler:

    def __init__(self, panelContainer: PanelContainer):

        # Create tabs
        self.tabs = TabGroupEntity(panelContainer)
        for text in ["A", "B", "C"]:
            radio = RadioContainer(self.tabs, text)
            tab = TabEntity(radio, text,
                isOnFunction = lambda text=text: radio.group.isOptionOn(text),
                onClickFunction = radio.onClick
            )