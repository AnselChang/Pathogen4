from BaseEntity.entity import Entity
from EntityHandler.entity_manager import EntityManager
from EntityHandler.select_handler import SelectHandler
from reference_frame import PointRef, Ref, VectorRef
from pygame_functions import drawTransparentRect
import pygame

"""
Left click actions are for selecting
Right click actions are for moving

Left click node -> select
Left drag over screen -> multiselect
Right drag node -> move
Right drag over screen -> move field
"""

class SelectorBox:

    def __init__(self):
        self.selector = SelectHandler()
        self.disable()

    def enable(self, start: PointRef):
        self.active = True
        self.start = start.copy()
        self.selector.startSelection(start)

    def disable(self):
        self.active = False

    def isEnabled(self):
        return self.active

    # return a list of selected entities
    def update(self, end: PointRef, entities: EntityManager) -> list[Entity]:

        self.end = end
        return self.selector.updateSelection(end, entities.entities)

    def draw(self, screen: pygame.Surface):

        if not self.active:
            return
        
        drawTransparentRect(screen, *self.start.screenRef, *self.end.screenRef, (173, 216, 230), 100)


class Interactor:

    def __init__(self):

        self.box = SelectorBox()

        self.hoveredEntity: Entity = None
        self.selectedEntities: list[Entity] = []

        self.leftDragging: bool = False
        self.rightDragging: bool = False

        self.mouseStartDrag: PointRef = None
        self.didMove: bool = False

    def isMultiselect(self) -> bool:
        return self.box.active

    def onMouseDown(self, entities: EntityManager, mouse: PointRef, isRight: bool):

        self.didMove = False
        self.mouseStartDrag = mouse.copy()
        self.mousePrevious = mouse.copy()

        if isRight:
            self.onRightMouseDown(entities, mouse)
        else:
            self.onLeftMouseDown(entities, mouse)

    def onLeftMouseDown(self, entities: EntityManager, mouse: PointRef):
        self.leftDragging = True
        
        self.box.disable()
        if self.hoveredEntity is None:
            self.box.enable(self.mouseStartDrag)
            self.box.update(mouse, entities)
        
        # if there's a group selected but the mouse is not clicking on the group, deselect
        if self.hoveredEntity is None or self.hoveredEntity not in self.selectedEntities:
            self.selectedEntities = []

        # Start dragging a single object
        if len(self.selectedEntities) == 0 and self.hoveredEntity is not None:
            self.selectedEntities = [self.hoveredEntity]

    def onRightMouseDown(self, entities: EntityManager, mouse: PointRef):
        self.rightDragging = True


    def onMouseUp(self, entities: EntityManager, mouse: PointRef):
        self.leftDragging = False
        self.rightDragging = False
        if not self.didMove:
            self.onMouseClick(entities, mouse)

        self.box.disable()

    def onMouseMove(self, entities: EntityManager, mouse: PointRef):
        self.didMove = True

        if not self.rightDragging and not self.leftDragging:
            return
        
        if self.box.isEnabled():
            self.selectedEntities = self.box.update(mouse, entities)

        mouseDelta: VectorRef = mouse - self.mousePrevious
        self.mousePrevious = mouse.copy()

        if self.leftDragging and not self.box.isEnabled():
            for selected in self.selectedEntities:
                if selected.drag is not None:
                    selected.drag.dragOffset(mouseDelta)

    # It is guaranteed that onMouseMove() was not called if this function is called
    def onMouseClick(self, entities: EntityManager, mouse: PointRef):
        pass

    def draw(self, screen: pygame.Surface):

        # Draw multiselect box
        self.box.draw(screen)