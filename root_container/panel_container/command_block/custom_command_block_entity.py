from entity_base.listeners.drag_listener import DragLambda
from entity_base.static_entity import StaticEntity

from adapter.path_adapter import PathAdapter

from root_container.panel_container.command_block.trash_button_entity import TrashEntity
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_expansion.command_expansion_handler import CommandExpansionHandler
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

    def __init__(self, path, pathAdapter: PathAdapter, database, commandExpansion: CommandExpansionHandler):
        
        super().__init__(path, pathAdapter, database, commandExpansion,
                         drag = DragLambda(self, FonStartDrag = self.onStartDrag, FonDrag = self.onDrag, FonStopDrag = self.onStopDrag),
                         defaultExpand = True
                         )

        self.trashEntity = TrashEntity(self, onDelete = self.delete)
        self.entities.addEntity(self.trashEntity, self.headerEntity)

        self.dragging = False

    def delete(self):
        self.path.deleteCustomCommand(self)

    def isWidgetHovering(self) -> bool:
        return super().isWidgetHovering() or self.trashEntity.hover.isHovering
    
    def onStartDrag(self, mouse: PointRef):
        self.dragging = True
        self.startDragY = self.CENTER_Y
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
                oldAfter.onUpdateLinkedListPosition()

        oldPrev.onUpdateLinkedListPosition()
        oldNext.onUpdateLinkedListPosition()
        inserter.onUpdateLinkedListPosition()
        self.onUpdateLinkedListPosition()

        oldPrev.recomputePosition()

    # draw drag dots
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):
        pass