from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable
from common.reference_frame import PointRef, Ref

from common.dimensions import Dimensions
from data_structures.observer import Observer

from entity_base.container_entity import Container
from common.draw_order import DrawOrder
from entities.root_container.field_container.field_container import FieldContainer
from entities.root_container.panel_container.panel_container import PanelContainer
from entities.root_container.top_bar_container.top_bar_container import TopBarContainer

from utility.math_functions import distance
import pygame

"""
The entity that holds all other entities. Set to dimensions size, and recomputes
children when dimensions change
"""

class MainWindowContainer(Container):

    def __init__(self, parent, projectModel, runCommandsEditorFunction: Callable):

        self.BACKGROUND_COLOR = (168, 168, 168)

        super().__init__(parent)

        # Add permanent static entities
        self.PANEL_CONTAINER = PanelContainer()
        self.FIELD_CONTAINER = FieldContainer()
        self.TOP_BAR_CONTAINER = TopBarContainer(projectModel, runCommandsEditorFunction)