from __future__ import annotations
from typing import TYPE_CHECKING

from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_sequence_handler import CommandSequenceHandler


from entity_base.entity import Entity
from adapter.path_adapter import PathAdapter

from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.custom_command_block_entity import CustomCommandBlockEntity
from root_container.panel_container.command_expansion.command_expansion_container import CommandExpansionContainer

from command_creation.command_definition_database import CommandDefinitionDatabase
from command_creation.command_type import CommandType

from entity_handler.entity_manager import EntityManager
from entity_handler.interactor import Interactor

from common.font_manager import FontManager
from common.image_manager import ImageManager
from common.dimensions import Dimensions


"""
Construct CommandBlockEntity objects
"""

class CommandBlockEntityFactory:

    def __init__(self, database: CommandDefinitionDatabase, container: BlockTabContentsContainer, commandExpansion: CommandExpansionContainer):
        self.database = database
        self.expansion = commandExpansion
        self.container = container

    def create(self, parent: Entity, commandHandler: CommandSequenceHandler, adapter: PathAdapter) -> CommandBlockEntity:
        if adapter.type == CommandType.CUSTOM:
            return CustomCommandBlockEntity(self.container, parent, commandHandler, adapter, self.database, self.expansion)
        else:
            return CommandBlockEntity(self.container, parent, commandHandler, adapter, self.database, self.expansion)