from BaseEntity.entity import Entity
from reference_frame import PointRef
from BaseEntity.EntityFunctions.drag_function import Drag
from BaseEntity.EntityFunctions.click_function import Click
from BaseEntity.EntityFunctions.select_function import Select

class IndependentEntity(Entity):

    # initialOffset is the offset relative to the parent entity
    def __init__(self, position: PointRef, drag: Drag = None, click: Click = None, select: Select = None, drawOrder: int = 0):
        Entity.__init__(self, drag = drag, click = click, select = select, drawOrder = drawOrder)
        self.position = position

    def getPosition(self) -> PointRef:
        return self.position