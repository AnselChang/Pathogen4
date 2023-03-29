from PathEntities.circle_mixin import CircleMixin
from BaseEntity.independent_entity import IndependentEntity
from reference_frame import PointRef, VectorRef
from BaseEntity.EntityFunctions.drag_function import DragLambda
from BaseEntity.EntityFunctions.click_function import ClickLambda
from BaseEntity.EntityFunctions.select_function import Select, SelectLambda
from draw_order import DrawOrder

from math_functions import isInsideBox

"""
Interactable path nodes
PathSegmentEntities connect two PathNodeEntities
Referenced in PathSection
"""

class PathNodeEntity(IndependentEntity, CircleMixin):

    def __init__(self, position: PointRef):
        super().__init__(
            position = position,
            drag = DragLambda(
                self,
                FcanDragOffset = lambda offset: isInsideBox(*(self.getPosition()+offset).fieldRef, 0, 0, 144, 144),
                FdragOffset = lambda offset: self.move(offset)
            ),
            select = SelectLambda(self, "path node", FgetHitboxPoints = self.getHitboxPoints),
            click = ClickLambda(self, FonLeftClick = lambda : print("left click"), FonRightClick = lambda : print("right click")),
            drawOrder = DrawOrder.NODE
            )
        
        blue = (102, 153, 255)
        CircleMixin.__init__(self, 10, 12, blue)


    def move(self, offset: VectorRef):
        self.position += offset
