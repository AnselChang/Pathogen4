from __future__ import annotations
from typing import TYPE_CHECKING
from command_creation.command_type import CommandType


if TYPE_CHECKING:
    from root_container.path import Path
    from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer
    from root_container.panel_container.command_block.command_sequence_handler import CommandSequenceHandler
    from root_container.panel_container.command_block.command_block_container import CommandBlockContainer


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

    def __init__(self, parent: CommandBlockContainer, handler: CommandSequenceHandler, pathAdapter: PathAdapter, database, commandExpansion: CommandExpansionContainer):
        
        super().__init__(parent, handler, pathAdapter, database, commandExpansion,
                         drag = DragLambda(self, FonStartDrag = self.onStartDrag, FonDrag = self.onDrag, FonStopDrag = self.onStopDrag),
                         defaultExpand = True, isCustom = True
                         )

        self.dragging = False

    def onDelete(self, mouse: tuple):
        self.handler.deleteCommand(self)
        self.handler.recomputePosition()

    def onStartDrag(self, mouse: tuple):
        self.mouseOffset = self.CENTER_Y - mouse[1]
        self.dragPosition = mouse[1] + self.mouseOffset

    def onStopDrag(self):
        self.dragPosition = None
        self.recomputeEntity()
    
    def onDrag(self, mouse: tuple):

        # if not custom and not task
        considerInsertersInsideTask = self.type != CommandType.CUSTOM or not self.isTask()

        self.dragPosition = mouse[1] + self.mouseOffset
        inserter: CommandInserter = self.handler.getClosestInserter(mouse, considerInsertersInsideTask)

        # if dragged to a different position to swap commands
        if self.getNextInserter() is not inserter and self.getNextInserter() is not inserter:
            self.handler.moveCommand(self, inserter)
            self.handler.recomputePosition()
        else:
            self.recomputeEntity()

    def defineCenterY(self):
        if self.drag.isDragging:
            return self.dragPosition
        else:
            return None