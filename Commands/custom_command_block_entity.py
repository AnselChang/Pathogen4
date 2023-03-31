from BaseEntity.entity import Entity

from Adapters.path_adapter import PathAdapter

from Commands.command_state import CommandState
from Commands.trash import Trash
from CommandCreation.command_type import COMMAND_INFO, CommandType
from Commands.command_block_entity import CommandBlockEntity

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor


from image_manager import ImageManager, ImageID
from dimensions import Dimensions
from reference_frame import PointRef, Ref
import pygame

class CustomCommandBlockEntity(CommandBlockEntity):

    def __init__(self, state: CommandState, entities: EntityManager, interactor: Interactor, images: ImageManager, dimensions: Dimensions):
        
        super().__init__(state, entities, interactor, images, dimensions)

        self.trash = Trash(self, self.images, self.dimensions, onDelete = self.delete)
        self.entities.addEntity(self.trash)

    def delete(self):
        pass