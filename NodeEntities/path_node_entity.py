from NodeEntities.circle_mixin import CircleMixin
from BaseEntity.entity import Entity
from reference_frame import PointRef, VectorRef
from BaseEntity.EntityListeners.drag_listener import DragLambda
from BaseEntity.EntityListeners.click_listener import ClickLambda
from BaseEntity.EntityListeners.select_listener import SelectListener, SelectLambda
from BaseEntity.EntityListeners.key_listener import KeyLambda
from BaseEntity.EntityListeners.hover_listener import HoverLambda
from SegmentEntities.path_segment_entity import PathSegmentEntity
from draw_order import DrawOrder
from EntityHandler.interactor import Interactor
from EntityHandler.entity_manager import EntityManager

from Adapters.path_adapter import AdapterInterface
from Adapters.turn_adapter import TurnAdapter, TurnAttributeID

from NodeEntities.constraints import Constraints
from dimensions import Dimensions

from image_manager import ImageID
from linked_list import LinkedListNode

from math_functions import isInsideBox
from pygame_functions import shade
from angle_functions import deltaInHeading
from format_functions import formatDegrees

import pygame

"""
Interactable path nodes
Neighbors PathSegmentEntities
Referenced in PathSection
"""

class PathNodeEntity(CircleMixin, Entity, AdapterInterface, LinkedListNode[PathSegmentEntity]):

    BLUE_COLOR = (102, 153, 255)
    FIRST_BLUE_COLOR = (40, 40, 255)

    def __init__(self, entities: EntityManager, interactor: Interactor, dimensions: Dimensions, position: PointRef):
        Entity.__init__(self,
            drag = DragLambda(
                self,
                FonStartDrag = self.onStartDrag,
                FcanDrag = self.canDrag,
                FonDrag = self.onDrag,
                FonStopDrag = self.onStopDrag
            ),
            select = SelectLambda(self, "path node", FgetHitbox = self.getHitbox),
            click = ClickLambda(self, FonLeftClick = lambda : print("left click"), FonRightClick = lambda : print("right click")),
            hover = HoverLambda(self, FonHoverOff = self.onHoverOff, FonHoverOn = self.onHoverOn),
            key = KeyLambda(self, FonKeyDown = self.onKeyDown, FonKeyUp = self.onKeyUp),
            drawOrder = DrawOrder.NODE
            )
        
        LinkedListNode.__init__(self)
                
        super().__init__(10, 12)

        self.interactor = interactor
        self.position = position
        self.adapter: TurnAdapter = TurnAdapter()

        self.dragging = True
        SNAPPING_POWER = 5 # in pixels
        self.constraints = Constraints(SNAPPING_POWER, dimensions)
        entities.addEntity(self.constraints, self)

        self.shiftKeyPressed = False

    def getPosition(self) -> PointRef:
        return self.position

    def getColor(self) -> tuple:
        return self.FIRST_BLUE_COLOR if self.getPrevious() is None else self.BLUE_COLOR

    def getAdapter(self) -> TurnAdapter:
        return self.adapter
    
    def updateAdapter(self) -> None:
        if self.getPrevious() is None and self.getNext() is None:
            start, end = 0,0
        elif self.getPrevious() is not None and self.getNext() is None:
            angle = self.getPrevious().getEndTheta()
            start, end = angle, angle
        elif self.getNext() is not None and self.getPrevious() is None:
            angle = self.getNext().getStartTheta()
            start, end = angle, angle
        else:
            start = self.getPrevious().getEndTheta()
            end = self.getNext().getEndTheta()
            
        self.adapter.set(TurnAttributeID.THETA1, start, formatDegrees(start, 1))
        self.adapter.set(TurnAttributeID.THETA2, end, formatDegrees(end, 1))

        direction = deltaInHeading(start, end)
        self.adapter.setIcon(ImageID.TURN_RIGHT if direction >= 0 else ImageID.TURN_LEFT)

    def onHoverOff(self):
        self.constraints.hide()

    def onHoverOn(self):
        self.constraints.show()

    def onStartDrag(self, mouse: PointRef):
        self.mouseStartDrag = mouse.copy()
        self.startPosition = self.getPosition().copy()
        self.constraints.show()

    def onStopDrag(self):
        self.dragging = False
        self.constraints.hide()

    def canDrag(self, mouse: PointRef) -> bool:

        pos = self.startPosition + (mouse - self.mouseStartDrag)
        return isInsideBox(*pos.fieldRef, 0, 0, 144, 144)

    def onDrag(self, mouse: PointRef):

        self.position = self.startPosition + (mouse - self.mouseStartDrag)

        # if the only one being dragged and shift key not pressed, constrain with snapping
        if self.interactor.selected.hasOnly(self) and not self.shiftKeyPressed:
            self.constrainPosition()

        self.onNodeMove()

    def onNodeMove(self):
        if not self.getPrevious() is None:
            self.getPrevious().onNodeMove(self)
        if not self.getNext() is None:
            self.getNext().onNodeMove(self)
        self.updateAdapter()

    def onAngleChange(self):
        self.updateAdapter()

    def onKeyDown(self, key):
        if key == pygame.K_LSHIFT:
            self.constraints.clear()
            self.shiftKeyPressed = True

    def onKeyUp(self, key):
        if key == pygame.K_LSHIFT:
            self.shiftKeyPressed = False

    # "Snaps" to neighbors. Documentation in ConstraintManager
    def constrainPosition(self):

        self.constraints.reset(self.position)

        # snap to previous
        if self.getPrevious() is not None:
            pNode: PathNodeEntity = self.getPrevious().getPrevious()
            if pNode.getPrevious() is not None:
                self.constraints.addConstraint(
                    other = pNode.getPosition(),
                    theta = pNode.getPrevious().getEndTheta()
                )
        
        # snap to next
        if self.getNext() is not None:
            nNode: PathNodeEntity = self.getNext().getNext()
            if nNode.getNext() is not None:
                self.constraints.addConstraint(
                    other = nNode.getPosition(),
                    theta = nNode.getNext().getStartTheta()
                )
        
        # snap in between
        if self.getPrevious() is not None and self.getNext() is not None:
            pNodePos = self.getPrevious().getPrevious().getPosition()
            nNodePos = self.getNext().getNext().getPosition()
            self.constraints.addConstraint(
                other = pNodePos,
                theta = (nNodePos - pNodePos).theta()
            )

        # The four cardinal directions
        PI = 3.1415
        for theta in [0, PI/2]:
            if self.getPrevious() is not None:
                self.constraints.addConstraint(
                    other = self.getPrevious().getPrevious().getPosition(),
                    theta = theta
                )
            if self.getNext() is not None:
                self.constraints.addConstraint(
                    other = self.getNext().getNext().getPosition(),
                    theta = theta
                )

        self.position = self.constraints.get()