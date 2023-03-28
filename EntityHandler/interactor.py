from BaseEntity.entity import Entity
from EntityHandler.entity_manager import EntityManager
from EntityHandler.select_handler import SelectHandler
from reference_frame import PointRef, Ref, VectorRef
from pygame_functions import drawTransparentRect
from dimensions import Dimensions
from field_transform import FieldTransform
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

    def enable(self, start: tuple):
        self.active = True
        self.start = start
        self.selector.startSelection(start)

    def disable(self):
        self.active = False

    def isEnabled(self):
        return self.active

    # return a list of selected entities
    def update(self, end: tuple, entities: EntityManager) -> list[Entity]:

        self.end = end
        return self.selector.updateSelection(end, entities.entities)

    def draw(self, screen: pygame.Surface):

        if not self.active:
            return
        
        drawTransparentRect(screen, *self.start, *self.end, (173, 216, 230), 100)


class Interactor:

    def __init__(self, dimensions: Dimensions, fieldTransform: FieldTransform):

        self.dimensions = dimensions
        self.fieldTransform = fieldTransform

        self.box = SelectorBox()

        self.hoveredEntity: Entity = None
        self.selectedEntities: list[Entity] = []

        self.leftDragging: bool = False
        self.rightDragging: bool = False

        self.mouseStartDrag: tuple = None
        self.didMove: bool = False

        self.panning = False

    def isMultiselect(self) -> bool:
        return self.box.active

    def onMouseDown(self, entities: EntityManager, mouse: PointRef, isRight: bool):

        # prevent double clicks
        if self.leftDragging or self.rightDragging:
            return

        self.didMove = False
        self.mouseStartDrag = mouse.screenRef
        self.mousePrevious = mouse.copy()

        if isRight:
            self.onRightMouseDown(entities, mouse)
        else:
            self.onLeftMouseDown(entities, mouse)

    def onLeftMouseDown(self, entities: EntityManager, mouse: PointRef):

        self.leftDragging = True
        
        # disable multiselect
        self.box.disable()
        
        # if there's a group selected but the mouse is not clicking on the group, deselect
        if self.hoveredEntity is None or self.hoveredEntity not in self.selectedEntities:
            self.selectedEntities = []

        # Start dragging a single object
        if len(self.selectedEntities) == 0 and self.hoveredEntity is not None:
            self.selectedEntities = [self.hoveredEntity]

        # start panning
        mx, my = mouse.screenRef
        if self.hoveredEntity is None and mx < self.dimensions.FIELD_WIDTH:
            self.panning = True
            self.fieldTransform.startPan()

    def onRightMouseDown(self, entities: EntityManager, mouse: PointRef):
        self.rightDragging = True

        # start multiselect
        self.box.disable()
        if self.hoveredEntity is None:
            self.box.enable(self.mouseStartDrag)
            self.box.update(mouse.screenRef, entities)

    def onMouseUp(self, entities: EntityManager, mouse: PointRef):
        isRight = self.rightDragging
        self.leftDragging = False
        self.rightDragging = False
        if not self.didMove:
            self.onMouseClick(entities, mouse, isRight)

        self.box.disable()
        self.panning = False

    def onMouseMove(self, entities: EntityManager, mouse: PointRef):
        self.didMove = True

        # after this point, mouse movement was dragging and not just moving around
        if not self.rightDragging and not self.leftDragging:
            return
        
        # Update multiselect
        if self.box.isEnabled():
            self.selectedEntities = self.box.update(mouse.screenRef, entities)

        # Calculate how much the mouse moved this tick
        mouseDelta: VectorRef = mouse - self.mousePrevious
        self.mousePrevious = mouse.copy()

        # Drag selection
        if self.leftDragging and not self.box.isEnabled():
            for selected in self.selectedEntities:
                if selected.drag is not None:
                    selected.drag.dragOffset(mouseDelta)

        # pan field
        if self.leftDragging and self.panning:
            mx, my = mouse.screenRef

            self.fieldTransform.updatePan(mx - self.mouseStartDrag[0], my - self.mouseStartDrag[1])

    # It is guaranteed that onMouseMove() was not called if this function is called
    def onMouseClick(self, entities: EntityManager, mouse: PointRef, isRight: bool):
        if self.hoveredEntity is not None and self.hoveredEntity.click is not None:
            if isRight:
                self.hoveredEntity.click.onRightClick()
            else:
                self.hoveredEntity.click.onLeftClick()

    def draw(self, screen: pygame.Surface):

        # Draw multiselect box
        self.box.draw(screen)