from NodeEntities.circle_mixin import CircleMixin
from BaseEntity.entity import Entity
from reference_frame import PointRef, VectorRef
from BaseEntity.EntityListeners.drag_listener import DragLambda
from BaseEntity.EntityListeners.click_listener import ClickLambda
from BaseEntity.EntityListeners.select_listener import SelectListener, SelectLambda
from SegmentEntities.path_segment_entity import PathSegmentEntity
from draw_order import DrawOrder

from Adapters.path_adapter import AdapterInterface
from Adapters.turn_adapter import TurnAdapter, TurnAttributeID

from image_manager import ImageID
from linked_list import LinkedListNode

from math_functions import isInsideBox
from pygame_functions import shade
from angle_functions import deltaInHeading
from format_functions import formatDegrees

"""
Interactable path nodes
Neighbors PathSegmentEntities
Referenced in PathSection
"""

class PathNodeEntity(CircleMixin, Entity, AdapterInterface, LinkedListNode[PathSegmentEntity]):

    BLUE_COLOR = (102, 153, 255)
    FIRST_BLUE_COLOR = (40, 40, 255)

    def __init__(self, position: PointRef):
        Entity.__init__(self,
            drag = DragLambda(
                self,
                FcanDragOffset = lambda offset: isInsideBox(*(self.getPosition()+offset).fieldRef, 0, 0, 144, 144),
                FdragOffset = lambda offset: self.move(offset)
            ),
            select = SelectLambda(self, "path node", FgetHitbox = self.getHitbox),
            click = ClickLambda(self, FonLeftClick = lambda : print("left click"), FonRightClick = lambda : print("right click")),
            drawOrder = DrawOrder.NODE
            )
        
        LinkedListNode.__init__(self)
                
        super().__init__(10, 12)

        self.position = position
        self.adapter: TurnAdapter = TurnAdapter()

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

    def move(self, offset: VectorRef):
        self.position += offset
        self.onNodeMove()

    def onNodeMove(self):
        if not self.getPrevious() is None:
            self.getPrevious().onNodeMove(self)
        if not self.getNext() is None:
            self.getNext().onNodeMove(self)
        self.updateAdapter()

    def onAngleChange(self):
        self.updateAdapter()