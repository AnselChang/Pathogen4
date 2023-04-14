from __future__ import annotations
from typing import TYPE_CHECKING
from data_structures.observer import Observer
from root_container.panel_container.command_block.command_sequence_handler import CommandSequenceHandler

from root_container.panel_container.command_expansion.command_expansion_container import CommandExpansionContainer
if TYPE_CHECKING:
    from root_container.panel_container.tab.tab_handler import TabHandler
    from command_creation.command_definition_database import CommandDefinitionDatabase


from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref

from root_container.panel_container.tab.abstract_tab_contents_container import AbstractTabContentsContainer
from root_container.panel_container.gradient_separator.gradient_separator import TabsCommandsSeparator

import entity_base.entity as entity
from common.draw_order import DrawOrder

from utility.math_functions import distance
import pygame

"""
An entity for the panel on the right side. Holds other entities inside
"""

class BlockTabContentsContainer(AbstractTabContentsContainer, Observer):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, parentPanel, tabHandler: TabHandler, database: CommandDefinitionDatabase):
        super().__init__(parentPanel, tabHandler, "Blocks")

        # add gradient panels
        TabsCommandsSeparator(self)

        self.commandHandler = CommandSequenceHandler(self, database)

        # add command expansion
        # On command expansion button click, recalculate targets
        self.commandExpansion = CommandExpansionContainer(self)
        self.commandHandler.initCommandExpansion(self.commandExpansion)
        self.commandExpansion.subscribe(self, onNotify = self.commandHandler.onGlobalCommandExpansionChange)