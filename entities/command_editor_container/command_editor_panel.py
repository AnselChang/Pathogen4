from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.listeners.mousewheel_listener import MousewheelLambda
from entity_base.panel_container import PanelContainer
from entities.command_editor_container.code_panel.code_panel import CodePanel
from entities.command_editor_container.command_panel.command_panel import CommandPanel
from entities.command_editor_container.widget_panel.widget_panel import WidgetPanel

from utility.math_functions import distance
import pygame

"""
Adds padding to command editor
"""

class CommandEditorPanel(PanelContainer):

    def __init__(self, parent):

        OUTER_PADDING = 8

        super().__init__(
            parent, 0, 0, 1, 1, OUTER_PADDING
        )
        
        BRIGHT_BACKGROUND = [243, 243, 243]
        DARK_BACKGROUND = [111, 111, 111]

        PADDING = 4
        RADIUS = 15

        self.COMMAND_PANEL = CommandPanel(self, 0.4, 0, 0.6, 1, PADDING, BRIGHT_BACKGROUND, RADIUS)
        self.WIDGET_PANEL = WidgetPanel(self, 0, 0, 0.4, 0.7, PADDING, BRIGHT_BACKGROUND, RADIUS)
        self.CODE_PANEL = CodePanel(self, 0, 0.7, 0.4, 0.3, PADDING, DARK_BACKGROUND, RADIUS)
