from command_creation.command_definition_database import CommandDefinitionDatabase
from data_structures.observer import Observer
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

class TabHandler(Observer):

    def __init__(self, panel: PanelContainer, database: CommandDefinitionDatabase):

        FONT_ID = FontID.FONT_TITLE
        FONT_SIZE = 15

        self.tabs = None

        self.blockContainer = BlockTabContentsContainer(panel, self, database)
        self.codeContainer = CodeTabContentsContainer(panel, self)
        self.settingsContainer = SettingsTabContentsContainer(panel, self)

        self.tabContents: list[AbstractTabContentsContainer] = [self.blockContainer, self.codeContainer, self.settingsContainer]

        self.radioToContent: dict[RadioContainer, AbstractTabContentsContainer] = {}

        # Create tabs
        self.tabs = TabGroupEntity(panel)
        for i, tabContent in enumerate(self.tabContents):

            text = tabContent.tabName

            radio = RadioContainer(self.tabs, text)
            tab = TabEntity(radio, text, FONT_ID, FONT_SIZE,
                isOnFunction = lambda text=text: radio.group.isOptionOn(text),
                onClickFunction = radio.onClick
            )

            self.radioToContent[radio] = tabContent

            if i != 0:
                tabContent.setInvisible()
        
        self.tabs.subscribe(self, onNotify = self.onTabClicked)

    def onTabClicked(self):
        activeTabContent = self.radioToContent[self.tabs.getActiveOption()]
        for tabContent in self.tabContents:
            if tabContent is activeTabContent:
                tabContent.setVisible()
            else:
                tabContent.setInvisible()