from __future__ import annotations
from typing import TYPE_CHECKING
from command_creation.command_type import CommandType

if TYPE_CHECKING:
    from root_container.path import Path
    from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer
    from root_container.panel_container.command_block.command_sequence_handler import CommandSequenceHandler
    from root_container.panel_container.command_block.command_block_container import CommandBlockContainer
    from models.command_models.command_model import CommandModel

from entity_base.listeners.drag_listener import DragLambda
from entity_base.entity import Entity

from adapter.path_adapter import PathAdapter

from root_container.panel_container.command_block.trash_button_entity import TrashEntity
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_expansion.command_expansion_container import CommandExpansionContainer
from root_container.panel_container.command_block.command_inserter import CommandInserter

from entity_handler.entity_manager import EntityManager
from entity_handler.interactor import Interactor

from common.font_manager import FontManager
from common.reference_frame import PointRef, Ref
from common.image_manager import ImageManager
from common.dimensions import Dimensions
import pygame

"""
CustomCommands have two additonal features compared to regular commands
- deletable
- can drag to reorder anywhere
"""

class CustomCommandBlockEntity(CommandBlockEntity):

    def __init__(self, parent: Entity, model: CommandModel):
        
        super().__init__(parent, model)

    def onDelete(self):
        self.model.delete()
        self.getRootEntity().recomputeEntity()