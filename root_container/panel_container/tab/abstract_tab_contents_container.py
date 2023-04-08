from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.tab.tab_handler import TabHandler

from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref
from entity_base.container_entity import Container

import entity_base.entity as entity
from common.draw_order import DrawOrder

from utility.math_functions import distance
import pygame

"""
An entity for the panel on the right side. Holds other entities inside
"""

class AbstractTabContentsContainer(Container):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, parentPanel, tabHandler: TabHandler, tabName: str) -> None:
        
        super().__init__(parent = parentPanel)
        
        self.tabHandler = tabHandler
        self.color = parentPanel.color
        self.tabName = tabName
        self.recomputePosition()

    # only the currently-selected tab is visible
    def isVisible(self) -> bool:
        return self.tabHandler.isTabContentsVisible(self)

    # Sits right below where the tabs are
    def defineTopLeft(self) -> tuple:
        return self._px(0), self._py(0.05)
    
    def defineBottomY(self) -> tuple:
        return self._py(1)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self._pwidth(1)