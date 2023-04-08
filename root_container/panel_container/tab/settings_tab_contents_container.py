from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.tab.tab_handler import TabHandler

from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref

from root_container.panel_container.tab.abstract_tab_contents_container import AbstractTabContentsContainer

import entity_base.entity as entity
from common.draw_order import DrawOrder

from utility.math_functions import distance
import pygame

"""
An entity for the panel on the right side. Holds other entities inside
"""

class SettingsTabContentsContainer(AbstractTabContentsContainer):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, parentPanel, tabHandler: TabHandler):
        super().__init__(parentPanel, tabHandler, "Settings")

        