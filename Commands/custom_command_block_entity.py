from BaseEntity.EntityListeners.drag_listener import DragLambda
from BaseEntity.static_entity import StaticEntity

from Adapters.path_adapter import PathAdapter

from Commands.trash_entity import TrashEntity
from Commands.command_block_entity import CommandBlockEntity
from Commands.command_expansion import CommandExpansion
from Commands.command_inserter import CommandInserter

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from font_manager import FontManager
from reference_frame import PointRef, Ref
from image_manager import ImageManager
from dimensions import Dimensions
import pygame

"""
CustomCommands have two additonal features compared to regular commands
- deletable
- can drag to reorder anywhere
"""

class CustomCommandBlockEntity(CommandBlockEntity):

    def __init__(self, path, pathAdapter: PathAdapter, database, entities: EntityManager, interactor: Interactor, commandExpansion: CommandExpansion, images: ImageManager, fontManager: FontManager, dimensions: Dimensions):
        
        super().__init__(path, pathAdapter, database, entities, interactor, commandExpansion, images, fontManager, dimensions,
                         drag = DragLambda(self, FonStartDrag = self.onStartDrag, FonDrag = self.onDrag, FonStopDrag = self.onStopDrag),
                         defaultExpand = True
                         )

        self.trashEntity = TrashEntity(self, self.images, self.dimensions, onDelete = self.delete)
        self.entities.addEntity(self.trashEntity, self)

        self.dragging = False

    def delete(self):
        self.path.deleteCustomCommand(self)

    def isWidgetHovering(self) -> bool:
        return super().isWidgetHovering() or self.trashEntity.hover.isHovering
    
    def onStartDrag(self, mouse: PointRef):
        self.dragging = True
        self.startDragY = self.position.animatedDragPosition.get()
        self.startMouseY = mouse.screenRef[1]

    def onStopDrag(self):
        self.dragging = False
        self.dragOffset = 0

    # return 1 if not dragging, and dragged opacity if dragging
    # not applicable for regular command blocks
    def isDragging(self):
        return self.dragging
    
    def onDrag(self, mouse: PointRef):
        self.dragOffset = mouse.screenRef[1] - self.startMouseY
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

    # draw drag dots
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):

        super().draw(screen, isActive, isHovered)

        DY = 4
        WIDTH = 17
        HEIGHT = 2
        COLOR = [200]*3

        x = self.dimensions.FIELD_WIDTH + self.dimensions.PANEL_WIDTH - 43
        y = self.getY() + 10

        for i in range(3):
            pygame.draw.rect(screen, COLOR, (x, y, WIDTH, HEIGHT), border_radius = 3)
            y += DY