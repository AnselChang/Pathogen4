from data_structures.linked_list import LinkedList
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

Calling recomputePosition() on this class does the following things in this order:
1. update VarialbleGroupContainer position, and height (if isHorizontal) or width (if not)
2. In defineAfter(), update VariableContainer positions through container.setPosition()
3. Call recomputePosition() on all VariableContainers as specified in Entity class
It is an expensive operation. Attempt not to call this more than once per tick.
"""

class VariableGroupContainer(Container):

    def __init__(self, parent: Entity, isHorizontal: bool, margin: int = 0):

        self.isHorizontal = isHorizontal

        # linked list makes it easy to insert/remove VariableContainers
        self.containers: LinkedList[VariableContainer] = LinkedList()
        self.TOTAL_SIZE = 0
        self.margin = margin

        super().__init__(parent = parent, tick = TickLambda(self, FonTickEnd = self.onTickEnd))
        self.needToRecompute = False

    # VariableContainer should call this whenever its size changes. O(1), so call as many
    # times as you want in a single tick
    def onChangeInContainerSize(self):
        # Instead of calling updateContainerPositions() directly, set a flag
        # so it will be called on tick end
        self.needToRecompute = True
        
    # onTickEnd guarantees that, if there's nesting, children VGCs will update
    # before parent VGCs
    def onTickEnd(self):
        if self.needToRecompute:
            self.recomputePosition() # this calls updateContainerPositions() at some point
            self.needToRecompute = False

    # after VariableGroupContainer's position has been changed, recompute the position of
    # all VariableContainers
    def defineAfter(self) -> None:
        self.updateContainerPositions()

    # Iteratively update the position of each VariableContainer
    def updateContainerPositions(self):

        startPos = self.LEFT_X if self.isHorizontal else self.TOP_Y
        pos = startPos
        container = self.containers.head
        while True:

            # set the position of the container
            container.setPosition(pos)

            # use container size to find position of next container
            pos += container.defineWidth() if self.isHorizontal else container.defineHeight()

            # Go to next container, if any
            container = container.getNext()

            if container is None:
                break
            else:
                pos += self._awidth(self.margin) if self.isHorizontal else self._aheight(self.margin)

        # Now that we're at the end, we know the total width/height of the group
        self.TOTAL_SIZE = pos - startPos

    
