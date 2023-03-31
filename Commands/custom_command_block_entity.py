from Adapters.path_adapter import PathAdapter

from Commands.trash import Trash
from Commands.command_block_entity import CommandBlockEntity
from Commands.command_expansion import CommandExpansion

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from image_manager import ImageManager
from dimensions import Dimensions

class CustomCommandBlockEntity(CommandBlockEntity):

    def __init__(self, path, pathAdapter: PathAdapter, database, entities: EntityManager, interactor: Interactor, commandExpansion: CommandExpansion, images: ImageManager, dimensions: Dimensions):
        
        super().__init__(path, pathAdapter, database, entities, interactor, commandExpansion, images, dimensions)

        self.trash = Trash(self, self.images, self.dimensions, onDelete = self.delete)
        self.entities.addEntity(self.trash)

    def delete(self):
        pass

    def isOtherHovering(self) -> bool:
        return self.trash.hover.isHovering