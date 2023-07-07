from abc import ABC, abstractmethod
from enum import Enum
from common.reference_frame import PointRef, Ref

from common.dimensions import Dimensions
from data_structures.observer import Observer

from entity_base.container_entity import Container
from common.draw_order import DrawOrder
from root_container.command_editor_container.command_editor_container import CommandEditorContainer
from root_container.field_container.field_container import FieldContainer
from root_container.panel_container.panel_container import PanelContainer
from root_container.top_bar_container.top_bar_container import TopBarContainer

from utility.math_functions import distance
import pygame

"""
The entity that holds all other entities. Set to dimensions size, and recomputes
children when dimensions change
"""

class RootContainer(Container, Observer):

    def __init__(self):

        self.BACKGROUND_COLOR = (168, 168, 168)

        super().__init__(None, drawOrder = DrawOrder.BACKGROUND)
        self.dimensions.subscribe(self, onNotify = self.recomputeEntity)
        self.recomputeEntity()

    def initComponents(self, projectModel):
        # Add permanent static entities
        self.PANEL_CONTAINER = PanelContainer()
        self.FIELD_CONTAINER = FieldContainer()
        self.TOP_BAR_CONTAINER = TopBarContainer(projectModel)

        self.COMMAND_EDITOR_CONTAINER = CommandEditorContainer()
        self.COMMAND_EDITOR_CONTAINER.setInvisible()

    def defineTopLeft(self) -> tuple:
        return 0, 0

    # dimensions set to the full screen size
    def defineWidth(self) -> float:
        return self.dimensions.SCREEN_WIDTH
    def defineHeight(self) -> float:
        return self.dimensions.SCREEN_HEIGHT

    # Draw screen background
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        screen.fill(self.BACKGROUND_COLOR)