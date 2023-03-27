from Entities.circle_mixin import CircleMixin
from BaseEntity.entity import Entity
from BaseEntity.dependent_entity import DependentEntity
from reference_frame import PointRef, VectorRef
from BaseEntity.EntityFunctions.drag_function import DragLambda
from BaseEntity.EntityFunctions.click_function import ClickLambda
from BaseEntity.EntityFunctions.select_function import Select

class DependentCircleEntity(DependentEntity, CircleMixin):

    def __init__(self, parent: Entity, initialOffset: VectorRef, radius: int, color: tuple, id: str):
        super().__init__(
            parent = parent,
            initialOffset = initialOffset,
            drag = DragLambda(FdragOffset = lambda offset: self.move(offset)),
            select = Select(id),
            click = ClickLambda(FonLeftClick = lambda : print("left click"), FonRightClick = lambda : print("right click"))
            )
        
        CircleMixin.__init__(self, radius, color)


    def move(self, offset: VectorRef):
        self.vector += offset