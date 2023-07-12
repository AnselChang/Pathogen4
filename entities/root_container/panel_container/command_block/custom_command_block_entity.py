from __future__ import annotations
from typing import TYPE_CHECKING
from command_creation.command_type import CommandType
from models.project_history_interface import ProjectHistoryInterface

if TYPE_CHECKING:
    from models.command_models.command_model import CommandModel

from entity_base.listeners.drag_listener import DragLambda
from entity_base.entity import Entity

from adapter.path_adapter import PathAdapter

from entities.root_container.panel_container.command_block.trash_button_entity import TrashEntity
from entities.root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from entities.root_container.panel_container.command_block.command_inserter import CommandInserter

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

        # add save state to undo/redo stack
        ProjectHistoryInterface.getInstance().save()