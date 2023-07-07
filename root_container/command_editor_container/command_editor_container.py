from __future__ import annotations
from typing import TYPE_CHECKING
from entity_base.container_entity import Container

import entity_base.entity as entity
from root_container.command_editor_container.command_editor_panel import CommandEditorPanel
from utility.math_functions import distance
import pygame

"""
Defines the static boundaries of the command editor.
"""

class CommandEditorContainer(Container):

    def __init__(self):
        super().__init__(entity.ROOT_CONTAINER)

        CommandEditorPanel(self)

    def defineTopLeft(self) -> tuple:
        return 0, self.dimensions.TOP_HEIGHT

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self.dimensions.SCREEN_WIDTH
    def defineHeight(self) -> float:
        return self.dimensions.FIELD_HEIGHT
