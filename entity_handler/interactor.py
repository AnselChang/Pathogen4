from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity_ui.selector_menu.selector_menu_manager import SelectorMenuManager

from entity_base.entity import Entity
from entity_handler.entity_manager import EntityManager
from entity_handler.select_handler import SelectHandler
from entity_handler.selector_box import SelectorBox
from common.reference_frame import PointRef, VectorRef
from common.dimensions import Dimensions
from common.field_transform import FieldTransform
from utility.math_functions import isInsideBox

import pygame, time

"""
Deals with the mouse interaction of the software. Invokes callbacks for relevant
entities based on mouse input
"""

class Interactor:

    def initInteractor(self, menuManager: SelectorMenuManager, fieldContainer):
        self.fieldContainer = fieldContainer
        self.selected.initMenuManager(menuManager)

    def __init__(self, dimensions: Dimensions, fieldTransform: FieldTransform):

        self.dimensions = dimensions
        self.fieldTransform = fieldTransform

        # the multiselect box
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

        # Deselecting entities with this flag enabled blocks selection/click actions
        # immediately after deslect. set this to true when that happens
        self.greedyEntity: Entity = None
        self.rawHoveredEntity: Entity = None

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
        if entity.select.greedy:
            self.greedyEntity = entity
        if self.selected.add(entity):
            entity.select.onSelect(self)

    def removeEntity(self, entity: Entity, forceRemove: bool = False):
        if self.selected.remove(entity, self.hoveredEntity, forceRemove):
            entity.select.onDeselect(self)

    def removeAllEntities(self, forceRemove: bool = False):
        for entity in self.selected.entities:
            self.removeEntity(entity, forceRemove)

    def isMultiselect(self) -> bool:
        return self.box.active
    
    def setHoveredEntity(self, entity: Entity, mouse: tuple):
        #print(entity)

        self.CURRENT_MOUSE_POSITION = mouse

        self.rawHoveredEntity = entity

        if self.greedyEntity is not None:
            return

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
        

    def onMouseDown(self, entities: EntityManager, mouse: tuple, isRight: bool, shiftKey: bool):

        # prevent double clicks
        if self.leftDragging or self.rightDragging:
            return

        self.didMove = False
        self.mouseStartDrag = mouse
        self.mousePrevious = mouse

        if isRight:
            self.onRightMouseDown(entities, mouse)
        else:
            self.onLeftMouseDown(mouse, shiftKey)

    def onLeftMouseDown(self, mouse: tuple, shiftKey: bool):

        # handle double-click logic
        if self.hoveredEntity is not None and self.hoveredEntity.click is not None:
            if self.previousClickEntity is self.hoveredEntity and time.time() - self.previousClickTime < self.DOUBLE_CLICK_TIME:
                self.hoveredEntity.click.onDoubleLeftClick(mouse)
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

            self.removeAllEntities()

        if self.greedyEntity is None and self.hoveredEntity is not None and self.hoveredEntity.select is not None:
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


    def onRightMouseDown(self, entities: EntityManager, mouse: tuple):
        self.rightDragging = True

        # start multiselect
        self.box.disable()
        if self.hoveredEntity is self.fieldContainer:
            self.box.enable(self.mouseStartDrag)
            self.box.update(mouse, entities)

    def onMouseUp(self, entities: EntityManager, mouse: tuple):
        isRight = self.rightDragging
        self.leftDragging = False
        self.rightDragging = False

        toRemove = []
        for selected in self.selected.entities:
            if selected.drag is not None:
                selected.drag.onStopDrag()
            if selected.select.deselectOnMouseUp:
                toRemove.append(selected)
        for entity in toRemove:
            self.removeEntity(entity)

        if not self.didMove:
            self.onMouseClick(mouse, isRight)

        self.box.disable()

        # release the mouse elsewhere from the greedy entity, so release greedy entity
        if self.greedyEntity is not None and self.rawHoveredEntity is not self.greedyEntity:
            self.removeEntity(self.greedyEntity)
            self.greedyEntity = None


    def canDragSelection(self, offset):
        for selected in self.selected.entities:
            if selected.drag is not None:
                if not selected.drag.canDrag(offset):
                    return False
        return True


    def onMouseMove(self, entities: EntityManager, mouse: tuple):
        self.didMove = True

        # after this point, mouse movement was dragging and not just moving around
        if not self.rightDragging and not self.leftDragging:
            return
        
        # Update multiselect
        if self.box.isEnabled():
            self.setSelectedEntities(self.box.update(mouse, entities))


        # Drag selection
        if self.leftDragging and not self.box.isEnabled() and self.canDragSelection(mouse):
            for selected in self.selected.entities:
                if selected.drag is not None:
                    selected.drag.onDrag(mouse)
    
    # It is guaranteed that onMouseMove() was not called if this function is called
    def onMouseClick(self, mouse: tuple, isRight: bool):
        if self.greedyEntity is None and self.hoveredEntity is not None and self.hoveredEntity.click is not None:
            if isRight:
                self.hoveredEntity.click.onRightClick(mouse)
            else:
                """
                On the special case onLeftClick returns an entity instead of None,
                start dragging that entity, even though mouse is up. it will stop
                dragging once mouse is pressed down again. One use case is creating
                new nodes with the "add new node" menu button
                """
                entityToStartDragging: Entity = self.hoveredEntity.click.onLeftClick(mouse)
                if entityToStartDragging is not None and entityToStartDragging.drag is not None:
                    print("start")
                    self.leftDragging = True
                    self.removeAllEntities(forceRemove = True)

                    self.addEntity(entityToStartDragging)
                    entityToStartDragging.drag.onStartDrag(mouse)



    def drawSelectBox(self, screen: pygame.Surface):

        # Draw multiselect box
        self.box.draw(screen)