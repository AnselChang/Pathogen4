from BaseEntity.entity import Entity
from reference_frame import PointRef
from BaseEntity.EntityListeners.drag_listener import Drag
from BaseEntity.EntityListeners.click_listener import Click
from BaseEntity.EntityListeners.select_listener import Select

class IndependentEntity(Entity):

    # initialOffset is the offset relative to the parent entity
    def __init__(self, position: PointRef, drag: Drag = None, click: Click = None, select: Select = None, drawOrder: int = 0):
        Entity.__init__(self, drag = drag, click = click, select = select, drawOrder = drawOrder)
        self.position = position

    def getPosition(self) -> PointRef:
        return self.position