from __future__ import annotations
from typing import TYPE_CHECKING
from models.path_models.path_segment_state.segment_type import SegmentType
from root_container.field_container.field_entity import FieldEntity

from models.path_models.segment_direction import SegmentDirection
from root_container.field_container.node.i_path_node_entity import IPathNodeEntity
from services.constraint_solver_service import LineConstraintSolver
if TYPE_CHECKING:
    from models.path_models.path_node_model import PathNodeModel

from enum import Enum
from entity_base.entity import Entity
from common.reference_frame import PointRef, Ref, VectorRef
from entity_base.image.image_state import ImageState
from entity_base.listeners.drag_listener import DragLambda
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.select_listener import SelectListener, SelectLambda
from entity_base.listeners.key_listener import KeyLambda
from entity_base.listeners.hover_listener import HoverLambda
from root_container.field_container.segment.straight_segment_entity import StraightSegmentEntity
from root_container.field_container.field_container import FieldContainer
from common.draw_order import DrawOrder
from entity_handler.interactor import Interactor
from entity_handler.entity_manager import EntityManager

from adapter.path_adapter import AdapterInterface, PathAttributeID
from adapter.turn_adapter import TurnAdapter

from common.image_manager import ImageID
from data_structures.linked_list import LinkedListNode

from utility.math_functions import addTuples, isInsideBox
from utility.pygame_functions import shade
from utility.angle_functions import deltaInHeading, headingDiff
from utility.format_functions import formatDegrees

import pygame

"""
Interactable path nodes
Neighbors PathSegmentEntities
Referenced in PathSection
"""

class PathNodeEntity(Entity, IPathNodeEntity):

    def __init__(self, fieldEntity: FieldEntity, model: PathNodeModel):
        self.field = fieldEntity
        self.model = model
        Entity.__init__(self,
                parent = fieldEntity,
                hover = HoverLambda(self),
                drag = DragLambda(self,
                    FonStartDrag = self.onStartDrag,
                    FonDrag = self.onDrag,
                    FcanDrag= self.canDrag,
                    FonStopDrag = self.onStopDrag
                ),
                select = SelectLambda(self, "path node", FgetHitbox = self.getHitbox),
                key = KeyLambda(self, FonKeyDown = self.onKeyDown, FonKeyUp = self.onKeyUp),
                drawOrder = DrawOrder.NODE
        )

        self.RADIUS = 10
        self.RADIUS_HOVERED = 12

        self.TURN_DISABLED_COLOR = (168, 194, 255)
        self.BLUE_COLOR = (102, 153, 255)
        self.FIRST_BLUE_COLOR = (40, 40, 255)
        self.RED_COLOR = (255, 102, 102)

        self.lastDragPositionValid = True


    def onStartDrag(self, mouse: tuple):

        # figure out initial offset in inches to determine offset when dragging
        mouseInchesX, mouseInchesY = self.field.mouseToInches(mouse)
        nodeInchesX, nodeInchesY = self.model.getPosition()
        self.dx, self.dy = mouseInchesX - nodeInchesX, mouseInchesY - nodeInchesY

        self.model.initConstraints()

        # old bezier curve is now out-of-date
        prevSegment = self.model.getPrevious()
        if prevSegment is not None and prevSegment.getType() == SegmentType.BEZIER:
            prevSegment.getBezierState().resetBezierSlow()
        nextSegment = self.model.getNext()
        if nextSegment is not None and nextSegment.getType() == SegmentType.BEZIER:
            nextSegment.getBezierState().resetBezierSlow()

    def canDrag(self, mouse: tuple) -> bool:
        mouseInches = self.field.mouseToInches(mouse)
        newPos = addTuples(mouseInches, [-self.dx, -self.dy])
        
        cd = self.field.inBoundsInches(newPos)

        if not cd:
            self.lastDragPositionValid = False
        return cd

    def onDrag(self, mouse: tuple):

        # compute dragged position, taking into account mouse offset from node center when starting drag
        rawPosX, rawPosY = self.field.mouseToInches(mouse)
        newPos = rawPosX - self.dx, rawPosY - self.dy

        # Cannot drag outside of field
        if not self.field.inBoundsInches(newPos):
            self.lastDragPositionValid = False
            return
                
        # update model with new position
        self.model.setAndConstrainPosition(newPos)
        self.lastDragPositionValid = True

    def onStopDrag(self):
        if self.model.isTemporary():
            if self.lastDragPositionValid:
                self.model.makePermanent()
            else:
                self.model.path.deleteNode(self.model)
                return
            
        # if neighbor segment is bezier, update bezier slow
        prevSegment = self.model.getPrevious()
        if prevSegment is not None and prevSegment.getType() == SegmentType.BEZIER:
            prevSegment.getBezierState().updateBezierSlow()
            prevSegment.recomputeUI()
        nextSegment = self.model.getNext()
        if nextSegment is not None and nextSegment.getType() == SegmentType.BEZIER:
            nextSegment.getBezierState().updateBezierSlow()
            nextSegment.recomputeUI()

    def onKeyDown(self, key):

        # delete node if temporary
        if (key == pygame.K_ESCAPE or key == pygame.K_BACKSPACE) and self.model.isTemporary():
            self.model.path.deleteNode(self.model)
            self.interactor.removeEntity(self)
            self.interactor.disableUntilMouseUp = False
            self.interactor.leftDragging = False

    def onKeyUp(self, key):
        pass

    # get the hitbox rect approximately spanning the circle
    def getHitbox(self) -> pygame.Rect:

        hitbox = pygame.Rect(0, 0, self.RADIUS * 1.5, self.RADIUS * 1.5)
        hitbox.center = self.CENTER_X, self.CENTER_Y
        return hitbox
        
    def defineCenter(self) -> tuple:
        return self.field.inchesToMouse(self.model.getPosition())
    
    def defineAfter(self) -> None:
        if self.model.isFirstNode():
            self.COLOR = self.FIRST_BLUE_COLOR
        elif not self.model.isTurnEnabled():
            self.COLOR = self.TURN_DISABLED_COLOR
        else:
            self.COLOR = self.BLUE_COLOR
    
    def isTouching(self, position: tuple) -> bool:
        MARGIN = 4
        return self.distanceTo(position) <= self.RADIUS + MARGIN
    
    def draw(self, screen, isActive, isHovered):

        if self.model.isTemporary():
            color = self.RED_COLOR
        else:
            color = self.COLOR

        POSITION = [self.CENTER_X, self.CENTER_Y]
        radius = self.RADIUS_HOVERED if self.hover.isHovering else self.RADIUS
        pygame.draw.circle(screen, color, POSITION, radius)
        
        if isActive:
            pygame.draw.circle(screen, (0,0,0), POSITION, radius, 2)