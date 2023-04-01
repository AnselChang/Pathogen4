from BaseEntity.EntityListeners.drag_listener import DragLambda

from Adapters.path_adapter import PathAdapter

from Commands.trash_entity import TrashEntity
from Commands.command_block_entity import CommandBlockEntity
from Commands.command_expansion import CommandExpansion

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from reference_frame import PointRef, Ref
from image_manager import ImageManager
from dimensions import Dimensions

"""
CustomCommands have two additonal features compared to regular commands
- deletable
- can move anywhere
"""

class CustomCommandBlockEntity(CommandBlockEntity):

    def __init__(self, path, pathAdapter: PathAdapter, database, entities: EntityManager, interactor: Interactor, commandExpansion: CommandExpansion, images: ImageManager, dimensions: Dimensions):
        
        super().__init__(path, pathAdapter, database, entities, interactor, commandExpansion, images, dimensions,
                         drag = DragLambda(self, FonStartDrag = self.onStartDrag, FonDrag = self.onDrag)
                         )

        self.trash = TrashEntity(self, self.images, self.dimensions, onDelete = self.delete)
        self.entities.addEntity(self.trash, self)

    def delete(self):
        self.path.deleteCustomCommand(self)

    def isOtherHovering(self) -> bool:
        return self.trash.hover.isHovering
    
    def onStartDrag(self, mouse: PointRef):
        print("start")
    
    def onDrag(self, mouse: PointRef):
        print("drag")