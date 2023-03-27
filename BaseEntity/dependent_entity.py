from BaseEntity.entity import Entity
from reference_frame import PointRef, VectorRef
from BaseEntity.EntityFunctions.drag_function import Drag
from BaseEntity.EntityFunctions.click_function import Click
from BaseEntity.EntityFunctions.select_function import Select

class DependentEntity(Entity):

    # initialOffset is the offset relative to the parent entity
    def __init__(self, parent: Entity, initialOffset: VectorRef, drag: Drag = None, click: Click = None, select: Select = None):
        Entity.__init__(self, drag = drag, click = click, select = select)
        self.vector = initialOffset
        self.parent = parent

    def getPosition(self) -> PointRef:
        print(self.parent.getPosition().screenRef, self.vector.screenRef, (self.parent.getPosition() + self.vector).screenRef)
        print(self.parent.getPosition().fieldRef, self.vector.fieldRef, (self.parent.getPosition() + self.vector).fieldRef)
        print()
        return self.parent.getPosition() + self.vector