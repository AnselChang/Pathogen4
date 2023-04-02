from BaseEntity.entity import Entity
from EntityHandler.entity_manager import EntityManager
from EntityHandler.select_handler import SelectHandler
from EntityHandler.selector_box import SelectorBox
from reference_frame import PointRef, VectorRef
from dimensions import Dimensions
from field_transform import FieldTransform
from math_functions import isInsideBox

import pygame, time

"""
Deals with the mouse interaction of the software. Invokes callbacks for relevant
entities based on mouse input
"""

class Interactor:

    def __init__(self, dimensions: Dimensions, fieldTransform: FieldTransform):

        self.dimensions = dimensions
        self.fieldTransform = fieldTransform

        self.box = SelectorBox()

        self.hoveredEntity: Entity = None
        self.selected: SelectHandler = SelectHandler()

        self.leftDragging: bool = False
        self.rightDragging: bool = False

        self.mouseStartDrag: tuple = None
        self.didMove: bool = False

        # these variables deal with double clicking
        self.previousClickEntity = None
        self.previousClickTime = None
        self.DOUBLE_CLICK_TIME = 0.3 # second

        self.panning = False

        # Deselecting entities with this flag enabled blocks selection/click actions
        # immediately after deslect. set this to true when that happens
        self.greedyDeselect = False

    # objects in list A but not B
    def setDifference(self, listA, listB):
        return [obj for obj in listA if obj not in listB]

    def setSelectedEntities(self, newSelected: list[Entity]):
        add = self.setDifference(newSelected, self.selected.entities)
        sub = self.setDifference(self.selected.entities, newSelected)
        for entity in sub:
            self.removeEntity(entity)
        for entity in add:
            self.addEntity(entity)

    def addEntity(self, entity: Entity):
        if self.selected.add(entity):
            entity.select.onSelect(self)

    def removeEntity(self, entity: Entity):
        self.selected.remove(entity)
        entity.select.onDeselect(self)

    def removeAllEntities(self):
        for entity in self.selected.entities:
            entity.select.onDeselect(self)
        self.selected.removeAll()

    def isMultiselect(self) -> bool:
        return self.box.active
    
    def setHoveredEntity(self, entity: Entity, mouse: PointRef):
        
        if self.hoveredEntity is not entity:

            # previous entity stopped hovering, so onHoverOff callback
            if self.hoveredEntity is not None and self.hoveredEntity.hover is not None:
                self.hoveredEntity.hover.onHoverOff()

            # new entity hovered, so onHoverOn callback
            if entity is not None and entity.hover is not None:
                entity.hover.onHoverOn()

        
        if entity is not None and entity.hover is not None:
            entity.hover.whileHovering(mouse)

        # update hovered entity
        self.hoveredEntity = entity
        

    def onMouseDown(self, entities: EntityManager, mouse: PointRef, isRight: bool, shiftKey: bool):

        # prevent double clicks
        if self.leftDragging or self.rightDragging:
            return

        self.didMove = False
        self.mouseStartDrag = mouse.screenRef
        self.mousePrevious = mouse.copy()

        if isRight:
            self.onRightMouseDown(entities, mouse)
        else:
            self.onLeftMouseDown(entities, mouse, shiftKey)

    def onLeftMouseDown(self, entities: EntityManager, mouse: PointRef, shiftKey: bool):

        # handle double-click logic
        if self.hoveredEntity is not None and self.hoveredEntity.click is not None:
            if self.previousClickEntity is self.hoveredEntity and time.time() - self.previousClickTime < self.DOUBLE_CLICK_TIME:
                self.hoveredEntity.click.onDoubleLeftClick()
                self.previousClickEntity = None
            else: # single click logic
                self.previousClickEntity = self.hoveredEntity
                self.previousClickTime = time.time()


        self.leftDragging = True
        
        # disable multiselect
        self.box.disable()

        
        # If shift key is pressed and there's a hovered entity, add/delete to selected.entities
        if shiftKey and self.hoveredEntity is not None and self.hoveredEntity.select is not None:

            # If already in selected entities, remove
            if self.hoveredEntity in self.selected.entities:
                self.removeEntity(self.hoveredEntity)
                self.leftDragging = False
            else: # otherwise, add
                self.addEntity(self.hoveredEntity)

        # if there's a group selected but the mouse is not clicking on the group, deselect
        elif self.hoveredEntity is None or self.hoveredEntity not in self.selected.entities:
        
            # If deselecting an entity with greedySelect flag set to true, do not allow selecting another entity at this tick
            for entity in self.selected.entities:
                if entity.select is not None and entity.select.greedyDeselect:
                    self.greedyDeselect = True

            self.removeAllEntities()

        if not self.greedyDeselect and self.hoveredEntity is not None and self.hoveredEntity.select is not None:
            # if enableToggle flag set, disable selection if clicking and already seleected:
            if len(self.selected.entities) == 1 and self.hoveredEntity is self.selected.entities[0] and self.hoveredEntity.select.enableToggle:
                self.removeEntity(self.hoveredEntity)
            # Start dragging a single object
            elif len(self.selected.entities) == 0:
                self.addEntity(self.hoveredEntity)

        # start dragging all the selected entities
        for entity in self.selected.entities:
            if entity.drag is not None:
                entity.drag.onStartDrag(mouse)


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

    def onMouseUp(self, entities: EntityManager, mouse: PointRef, path):
        isRight = self.rightDragging
        self.leftDragging = False
        self.rightDragging = False

        for selected in self.selected.entities:
            if selected.drag is not None:
                selected.drag.onStopDrag()

        if not self.didMove:
            self.onMouseClick(entities, mouse, isRight, path)

        self.box.disable()
        self.panning = False

        self.greedyDeselect = False

    def canDragSelection(self, offset):
        for selected in self.selected.entities:
            if selected.drag is not None:
                if not selected.drag.canDrag(offset):
                    return False
        return True


    def onMouseMove(self, entities: EntityManager, mouse: PointRef):
        self.didMove = True

        # after this point, mouse movement was dragging and not just moving around
        if not self.rightDragging and not self.leftDragging:
            return
        
        # Update multiselect
        if self.box.isEnabled():
            self.setSelectedEntities(self.box.update(mouse.screenRef, entities))


        # Drag selection
        if self.leftDragging and not self.box.isEnabled() and self.canDragSelection(mouse):
            for selected in self.selected.entities:
                if selected.drag is not None:
                    selected.drag.onDrag(mouse)
        

        # pan field
        if self.leftDragging and self.panning:
            mx, my = mouse.screenRef

            self.fieldTransform.updatePan(mx - self.mouseStartDrag[0], my - self.mouseStartDrag[1])

    # It is guaranteed that onMouseMove() was not called if this function is called
    def onMouseClick(self, entities: EntityManager, mouse: PointRef, isRight: bool, path):
        if not self.greedyDeselect and self.hoveredEntity is not None and self.hoveredEntity.click is not None:
            if isRight:
                self.hoveredEntity.click.onRightClick()
            else:
                self.hoveredEntity.click.onLeftClick()

        # create new node if right click field
        elif isRight and self.hoveredEntity is None:
            if isInsideBox(*mouse.screenRef, 0, 0, self.dimensions.FIELD_WIDTH, self.dimensions.SCREEN_HEIGHT):
                path.addNode(mouse.copy())

    def drawSelectBox(self, screen: pygame.Surface):

        # Draw multiselect box
        self.box.draw(screen)