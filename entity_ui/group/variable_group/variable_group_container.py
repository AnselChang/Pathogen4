from typing import Callable, Generic, TypeVar
from data_structures.linked_list import LinkedList
from data_structures.observer import Observable
from entity_base.container_entity import Container
from entity_base.entity import Entity
from entity_base.listeners.tick_listener import TickLambda
from entity_ui.group.variable_group.variable_container import VariableContainer


"""
Stores a linked list of VariableContainers, which are containers that have their own
variable width/height. The VariableGroupContainer should expand and contract to fit the
VariableContainers, and handles the absolute positioning of the VariableContainers
based on their width and height, and their order.

The goal is to minimize computation - height/width changes in multiple VariableContainers
in a single tick should only require a single recomputePosition() call.

This should also cache the total width/height of the VariableContainers
Use cases: Command blocks, CommandGroup block

If isHorizontal:
- VGC is defined at x = 0, y = center
If not isHorizontal:
- VGC is defined at x = center, y = 0

Calling recomputePosition() on this class does the following things in this order:
1. Get the left x (for horizontal) or top y (for vertical) of parent to define VGC position
2. In defineBefore(), update VariableContainer positions through container.setPosition()
3. Update width/height of VGC
3. Call recomputePosition() on all VariableContainers as specified in Entity class
It is an expensive operation. Attempt not to call this more than once per tick.
"""
T = TypeVar('T')
class VariableGroupContainer(Container, Generic[T], Observable):

    def __init__(self, parent: Entity, isHorizontal: bool, innerMargin: int = 0, outerMargin: int = 0,
                 name: str = ""):

        self.name = name
        self.isHorizontal = isHorizontal

        # linked list makes it easy to insert/remove VariableContainers
        self.containers: LinkedList[VariableContainer[T]] = LinkedList()
        self.innerMargin = innerMargin
        self.outerMargin = outerMargin

        super().__init__(parent = parent)

    def _getMargin(self, margin):
        return self._awidth(margin) if self.isHorizontal else self._aheight(margin)

    # Return the size of the VGC while setting the positions of the children
    def getSize(self) -> float:

        inner = self._getMargin(self.innerMargin)
        outer = self._getMargin(self.outerMargin)

        # add upper outer margin
        size = outer

        container = self.containers.head
        while container is not None:
            
            # use container size to find position of next container
            size += container.defineWidth() if self.isHorizontal else container.defineHeight()

            # Go to next container, if any
            container = container.getNext()

            if container is None:
                break
            else:
                size += inner
        size += outer

        return size
    
    # Return the size of the VGC while setting the positions of the children
    def updateContainerPositions(self) -> float:

        inner = self._getMargin(self.innerMargin)
        outer = self._getMargin(self.outerMargin)

        startPos = self._px(0) if self.isHorizontal else self._py(0)

        # add upper outer margin
        pos = startPos + outer

        container = self.containers.head
        while container is not None:

            # set the position of the container
            container.setPosition(pos)
            
            # use container size to find position of next container
            pos += container.defineWidth() if self.isHorizontal else container.defineHeight()

            # Go to next container, if any
            container = container.getNext()

            if container is None:
                break
            else:
                pos += inner


    def defineLeftX(self) -> float:
        if self.isHorizontal:
            return self._px(0)
        return None
    
    def defineCenterX(self) -> float:
        if not self.isHorizontal:
            return self._px(0.5)
        return None
    
    def defineTopY(self) -> float:
        if not self.isHorizontal:
            return self._py(0)
        return None
    
    def defineCenterY(self) -> float:
        if self.isHorizontal:
            return self._py(0.5)
        return None

    def defineWidth(self) -> float:
        if self.isHorizontal:
            return self.getSize()
        else:
            return self._pwidth(1)
        
    def defineHeight(self) -> float:
        if not self.isHorizontal:
            return self.getSize()
        else:
            return self._pheight(1)
        
    def defineAfter(self) -> None:
        self.updateContainerPositions()