from Adapters.path_adapter import PathAdapter

from Commands.command_block_entity import CommandBlockEntity
from Commands.custom_command_block_entity import CustomCommandBlockEntity
from Commands.command_expansion import CommandExpansionHandler

from CommandCreation.command_definition_database import CommandDefinitionDatabase
from CommandCreation.command_type import CommandType

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from font_manager import FontManager
from image_manager import ImageManager
from dimensions import Dimensions


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