from __future__ import annotations
import math
from typing import TYPE_CHECKING

from root_container.field_container.node.node_line import NodeLine
from root_container.field_container.path_element import PathElement
from root_container.field_container.segment.segment_direction import SegmentDirection
if TYPE_CHECKING:
    from root_container.path import Path

from enum import Enum
from entity_base.abstract_circle_entity import AbstractCircleEntity
from entity_base.entity import Entity
from common.reference_frame import PointRef, Ref, VectorRef
from entity_base.image.image_state import ImageState
from entity_base.listeners.drag_listener import DragLambda
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.select_listener import SelectListener, SelectLambda
from entity_base.listeners.key_listener import KeyLambda
from entity_base.listeners.hover_listener import HoverLambda
from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
from root_container.field_container.field_container import FieldContainer
from common.draw_order import DrawOrder
from entity_handler.interactor import Interactor
from entity_handler.entity_manager import EntityManager

from adapter.path_adapter import AdapterInterface, PathAttributeID
from adapter.turn_adapter import TurnAdapter

from root_container.field_container.node.constraints import Constraints
from root_container.field_container.node.bezier_theta_node import BezierThetaNode

from common.image_manager import ImageID
from data_structures.linked_list import LinkedListNode

from utility.math_functions import isInsideBox
from utility.pygame_functions import shade
from utility.angle_functions import deltaInHeading, headingDiff
from utility.format_functions import formatDegrees

import pygame

"""
Interactable path nodes
Neighbors PathSegmentEntities
Referenced in PathSection
"""

class TurnDirection(Enum):
    LEFT = 1
    RIGHT = 2

class PathNodeEntity(AbstractCircleEntity, AdapterInterface, PathElement[PathSegmentEntity]):

    TURN_DISABLED_COLOR = (0,0,0)
    BLUE_COLOR = (102, 153, 255)
    FIRST_BLUE_COLOR = (40, 40, 255)
    RED_COLOR = (255, 102, 102)

    def __init__(self, fieldContainer: FieldContainer, path: Path, position: PointRef, temporary: bool = False):
        self.fieldContainer = fieldContainer
        Entity.__init__(self,
                parent = fieldContainer,
                drag = DragLambda(
                self,
                FonStartDrag = self.onStartDrag,
                FcanDrag = self.canDrag,
                FonDrag = self.onDrag,
                FonStopDrag = self.onStopDrag
            ),
            select = SelectLambda(self, "path node", FgetHitbox = self.getHitbox),
            hover = HoverLambda(self, FonHoverOff = self.onHoverOff, FonHoverOn = self.onHoverOn),
            key = KeyLambda(self, FonKeyDown = self.onKeyDown, FonKeyUp = self.onKeyUp),
            drawOrder = DrawOrder.NODE
            )
        
        LinkedListNode.__init__(self)

        self.path = path
        self.position: PointRef = position
        self.adapter = TurnAdapter([
            ImageState(TurnDirection.RIGHT, ImageID.TURN_RIGHT),
            ImageState(TurnDirection.LEFT, ImageID.TURN_LEFT)
        ])

        # A bit like a "hover" node. If user doesn't successfully place it,
        # it will be deleted. Visually it is semi-transparent to indicate this.
        self.temporary = temporary
        self.lastDragPositionValid = False


        self.dragging = True
        SNAPPING_POWER = 5 # in pixels
        self.constraints = Constraints(fieldContainer, SNAPPING_POWER)

        self.shiftKeyPressed = False

        self.updateAdapter()

        NodeLine(self)
        


    def defineCenter(self) -> tuple:
        return self.position.screenRef

    def getColor(self, isHovered: bool) -> tuple:

        if self.isFirstNode():
            color = self.FIRST_BLUE_COLOR
        elif self.isTurnEnabled():
            color = self.BLUE_COLOR
        else:
            color = self.TURN_DISABLED_COLOR

        # That means we're on the verge of deleting this node, as it
        # is not in a valid location, and will be deleted if mouse down
        if self.temporary and self.lastDragPositionValid is False:
            color = self.RED_COLOR

        if isHovered:
            return shade(color, 0.9)
        return color
    
    def getOpacity(self) -> float:
        return 0.75 if self.isTemporary() else 1

    def getRadius(self, isHovered: bool = False) -> float:
        if self.isTurnEnabled() or self.isFirstNode():
            return 10
        else:
            return 7 if isHovered else 6

    def getAdapter(self) -> TurnAdapter:
        return self.adapter
    
    def getPositionRef(self) -> PointRef:
        return self.position
    
    def updateAdapter(self) -> None:
        start = self.getStartTheta()
        end = self.getStopTheta()

        if start is None: # (and end is None)
            start, end = 0,0

        self.START_THETA, self.END_THETA = start, end
            
        self.adapter.set(PathAttributeID.THETA1, start, formatDegrees(start, 1))
        self.adapter.set(PathAttributeID.THETA2, end, formatDegrees(end, 1))

        direction = deltaInHeading(start, end)
        self.adapter.setIconStateID(TurnDirection.RIGHT if direction >= 0 else TurnDirection.LEFT)

        self.adapter.setTurnEnabled(self.isTurnEnabled())
        self.recomputeEntity()

    # gets the start theta, adjusted for segment direction.
    # returns None if there is no previous node
    def getStartTheta(self):
        if self.getPrevious() is None:
            if self.getNext() is None:
                return None
            else:
                return self.getStopTheta()
        
        theta = self.getPrevious().getEndTheta()
        if self.getPrevious().getDirection() == SegmentDirection.REVERSE:
            theta = (theta + math.pi) % (math.pi*2)
        return theta

    # gets the stop theta, adjusted for segment direction.
    # returns None if there is no next node
    def getStopTheta(self):
        if self.getNext() is None:
            if self.getPrevious() is None:
                return None
            else:
                return self.getStartTheta()
        
        theta = self.getNext().getStartTheta()
        if self.getNext().getDirection() == SegmentDirection.REVERSE:
            theta = (theta + math.pi) % (math.pi*2)
        return theta

    def isTurnEnabled(self) -> bool:
        
        # No turning if the start and end theta are close to the same
        startTheta = self.getStartTheta()
        endTheta = self.getStopTheta()

        # if there is no previous or next node, then we can't turn to it
        if startTheta is None or endTheta is None:
            return False
        
        return headingDiff(startTheta, endTheta) > 1e-3
        

    def onHoverOff(self):
        self.constraints.hidePosition()
        self.constraints.hideTheta()

    def onHoverOn(self):
        self.constraints.showPosition()
        self.constraints.showTheta()

    def onStartDrag(self, mouse: tuple):
        self.mouseStartDrag = PointRef(Ref.SCREEN, mouse)
        self.startPosition = self.position.copy()
        self.constraints.showPosition()

    def onStopDrag(self):

        if self.temporary and not self.lastDragPositionValid:
            self.path.removeNode(self)


        self.dragging = False
        self.constraints.hidePosition()
        self.temporary = False # no longer temporary once placed

        # recalculate constraints for nodes, neighbors, and neighbors of neighbors
        # for hovering purposes
        if self.getNext() is not None:
            next = self.getNext().getNext()
            next.constraints.resetPositionConstraints(next.position)
            next.constrainPosition()
            if next.getNext() is not None:
                next = next.getNext().getNext()
                next.constraints.resetPositionConstraints(next.position)
                next.constrainPosition()
        if self.getPrevious() is not None:
            prev = self.getPrevious().getPrevious()
            prev.constraints.resetPositionConstraints(prev.position)
            prev.constrainPosition()
            if prev.getPrevious() is not None:
                prev = prev.getPrevious().getPrevious()
                prev.constraints.resetPositionConstraints(prev.position)
                prev.constrainPosition()
        
        if self.getNext() is not None:
            self.getNext().onNodeStopDrag()
        if self.getPrevious() is not None:
            self.getPrevious().onNodeStopDrag()

    def canDrag(self, mouseTuple: tuple) -> bool:
        mouse = PointRef(Ref.SCREEN, mouseTuple)
        pos: PointRef = self.startPosition + (mouse - self.mouseStartDrag)
        self.lastDragPositionValid = False # See if canDrag() is matched with onDrag() after. If so, valid
        return isInsideBox(*pos.fieldRef, 0, 0, 144, 144) and isInsideBox(*mouseTuple, *self.fieldContainer.RECT)

    def onDrag(self, mouseTuple: PointRef):
        self.lastDragPositionValid = True

        mouse = PointRef(Ref.SCREEN, mouseTuple)
        self.position = self.startPosition + (mouse - self.mouseStartDrag)

        # if the only one being dragged and shift key not pressed, constrain with snapping
        if self.interactor.selected.hasOnly(self) and not self.shiftKeyPressed:
            self.constraints.resetPositionConstraints(self.position)
            self.constrainPosition()
            self.position = self.constraints.getPosition()

        self.onNodeMove()

    def onNodeMove(self):
        if not self.getPrevious() is None:
            self.getPrevious().onNodeMove(self)
        if not self.getNext() is None:
            self.getNext().onNodeMove(self)
        self.updateAdapter()

    def onAngleChange(self):
        self.updateAdapter()

    def getOther(self, segment: PathSegmentEntity):
        if self.getPrevious() is segment:
            return self.getNext()
        elif self.getNext() is segment:
            return self.getPrevious()
        else:
            raise ValueError("Segment is not connected to this node")
        

    def onKeyDown(self, key):
        if key == pygame.K_LSHIFT:
            self.constraints.clear()
            self.shiftKeyPressed = True

        # delete node if temporary
        if (key == pygame.K_ESCAPE or key == pygame.K_BACKSPACE) and self.temporary:
            self.path.removeNode(self)
            self.interactor.removeEntity(self)
            self.interactor.disableUntilMouseUp = False
            self.interactor.leftDragging = False

    def onKeyUp(self, key):
        if key == pygame.K_LSHIFT:
            self.shiftKeyPressed = False

    # "Snaps" to neighbors. Documentation in ConstraintManager
    def constrainPosition(self):

        # snap to previous
        if self.getPrevious() is not None:
            pNode: PathNodeEntity = self.getPrevious().getPrevious()
            if pNode.getPrevious() is not None:
                self.constraints.addPositionConstraint(
                    other = pNode.getPositionRef(),
                    theta = pNode.getPrevious().getEndTheta()
                )
        
        # snap to next
        if self.getNext() is not None:
            nNode: PathNodeEntity = self.getNext().getNext()
            if nNode.getNext() is not None:
                self.constraints.addPositionConstraint(
                    other = nNode.getPositionRef(),
                    theta = nNode.getNext().getStartTheta()
                )
        
        # snap in between
        if self.getPrevious() is not None and self.getNext() is not None:
            pNodePos = self.getPrevious().getPrevious().getPositionRef()
            nNodePos = self.getNext().getNext().getPositionRef()
            self.constraints.addPositionConstraint(
                other = pNodePos,
                theta = (nNodePos - pNodePos).theta()
            )

        # Snap to the four cardinal directions for the current node, as well as previous and next
        self.addCardinalConstraints(self)
        if self.getPrevious() is not None:
            self.addCardinalConstraints(self.getPrevious().getPrevious())
        if self.getNext() is not None:
            self.addCardinalConstraints(self.getNext().getNext())
        
    
    def addCardinalConstraints(self, current: 'PathNodeEntity'):

        if current is None:
            return

        PI = 3.1415
        for theta in [0, PI/2]:
            if current.getPrevious() is not None:
                self.constraints.addPositionConstraint(
                    other = current.getPrevious().getPrevious().getPositionRef(),
                    theta = theta
                )
            if current.getNext() is not None:
                self.constraints.addPositionConstraint(
                    other = current.getNext().getNext().getPositionRef(),
                    theta = theta
                )

    def isFirstNode(self) -> bool:
        return self.getPrevious() is None
    
    def isLastNode(self) -> bool:
        return self.getNext() is None
    
    def isTemporary(self) -> bool:
        return self.temporary