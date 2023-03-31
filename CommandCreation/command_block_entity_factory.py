from Adapters.path_adapter import PathAdapter
from Commands.command_block_entity import CommandBlockEntity
from CommandCreation.command_definition_database import CommandDefinitionDatabase

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from image_manager import ImageManager
from dimensions import Dimensions

class CommandBlockEntityFactory:

    def __init__(self, database: CommandDefinitionDatabase, entities: EntityManager, interactor: Interactor, images: ImageManager, dimensions: Dimensions):
        self.database = database
        self.entities = entities
        self.interactor = interactor
        self.images = images
        self.dimensions = dimensions

    def create(self, adapter: PathAdapter) -> CommandBlockEntity:
        return CommandBlockEntity(adapter, self.database, self.entities, self.interactor, self.images, self.dimensions)