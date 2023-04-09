from root_container.panel_container.panel_container import PanelContainer
from root_container.panel_container.tab.abstract_tab_contents_container import AbstractTabContentsContainer
from root_container.panel_container.tab.tab_entity import TabEntity
from root_container.panel_container.tab.tab_group_entity import TabGroupEntity
from entity_ui.group.radio_container import RadioContainer
from common.font_manager import FontID

from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer
from root_container.panel_container.tab.code_tab_contents_container import CodeTabContentsContainer
from root_container.panel_container.tab.settings_tab_contents_container import SettingsTabContentsContainer



"""
Manage correct instantiation of tabs
"""

class TabHandler:

    def __init__(self, panel: PanelContainer):

        FONT_ID = FontID.FONT_TITLE
        FONT_SIZE = 15

        self.tabs = None

        self.blockContainer = BlockTabContentsContainer(panel, self)
        self.codeContainer = CodeTabContentsContainer(panel, self)
        self.settingsContainer = SettingsTabContentsContainer(panel, self)

        # Create tabs
        self.tabs = TabGroupEntity(panel)
        for tabContent in [self.blockContainer, self.codeContainer, self.settingsContainer]:

            text = tabContent.tabName

            radio = RadioContainer(self.tabs, text)
            tab = TabEntity(radio, text, FONT_ID, FONT_SIZE,
                isOnFunction = lambda text=text: radio.group.isOptionOn(text),
                onClickFunction = radio.onClick
            )

    def isTabContentsVisible(self, tabContents: AbstractTabContentsContainer) -> bool:
        if self.tabs is None:
            return True
        return self.tabs.isOptionOn(tabContents.tabName)