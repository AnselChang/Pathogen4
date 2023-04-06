from adapter.path_adapter import PathAdapter

from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.custom_command_block_entity import CustomCommandBlockEntity
from root_container.panel_container.command_expansion.command_expansion_handler import CommandExpansionHandler

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

    def __init__(self, database: CommandDefinitionDatabase, commandExpansion: CommandExpansionHandler):
        self.database = database
        self.expansion = commandExpansion

    def create(self, path, adapter: PathAdapter) -> CommandBlockEntity:
        if adapter.type == CommandType.CUSTOM:
            return CustomCommandBlockEntity(path, adapter, self.database, self.expansion)
        else:
            return CommandBlockEntity(path, adapter, self.database, self.expansion)