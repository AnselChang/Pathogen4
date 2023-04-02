from BaseEntity.EntityListeners.drag_listener import DragLambda

from Adapters.path_adapter import PathAdapter

from Commands.trash_entity import TrashEntity
from Commands.command_block_entity import CommandBlockEntity
from Commands.command_expansion import CommandExpansion
from Commands.command_inserter import CommandInserter

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from reference_frame import PointRef, Ref
from image_manager import ImageManager
from dimensions import Dimensions

"""
CustomCommands have two additonal features compared to regular commands
- deletable
- can drag to reorder anywhere
"""

class CustomCommandBlockEntity(CommandBlockEntity):

    def __init__(self, path, pathAdapter: PathAdapter, database, entities: EntityManager, interactor: Interactor, commandExpansion: CommandExpansion, images: ImageManager, dimensions: Dimensions):
        
        super().__init__(path, pathAdapter, database, entities, interactor, commandExpansion, images, dimensions,
                         drag = DragLambda(self, FonStartDrag = self.onStartDrag, FonDrag = self.onDrag, FonStopDrag = self.onStopDrag),
                         defaultExpand = True
                         )

        self.trash = TrashEntity(self, self.images, self.dimensions, onDelete = self.delete)
        self.entities.addEntity(self.trash, self)

    def delete(self):
        self.path.deleteCustomCommand(self)

    def isOtherHovering(self) -> bool:
        return self.trash.hover.isHovering
    
    def onStartDrag(self, mouse: PointRef):
        pass

    def onStopDrag(self):
        pass

    
    
    def onDrag(self, mouse: PointRef):
        inserter: CommandInserter = self.path.getClosestInserter(mouse)

        # no change in position if dragging to immediate neighbor inserter
        if self.getNext() is inserter or self.getPrevious() is inserter:
            return
        
        self.moveAfter(inserter)

    def moveAfter(self, inserter: CommandInserter):

        if inserter._next is None:
            oldPrev = self._prev
            oldNext = self._next._next
            oldPrev._next = oldNext
            oldNext._prev = oldPrev

            oldTail = inserter
            self.path.commandList.tail = self._next
            self._next._next = None
            self._prev = oldTail
            oldTail._next = self
        else:

            if self._next is self.path.commandList.tail:
                self.path.commandList.tail = self._prev

            oldPrev = self._prev
            oldAfter = self._next._next

            newNext = inserter._next
            self._prev = inserter
            inserter._next = self
            self._next._next = newNext
            newNext._prev = self._next

            oldPrev._next = oldAfter
            if oldAfter is not None:
                oldAfter._prev = oldPrev

        self.path.recomputeY()