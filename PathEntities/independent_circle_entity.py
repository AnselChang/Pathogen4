from PathEntities.circle_mixin import CircleMixin
from BaseEntity.independent_entity import IndependentEntity
from reference_frame import PointRef, VectorRef
from BaseEntity.EntityFunctions.drag_function import DragLambda
from BaseEntity.EntityFunctions.click_function import ClickLambda
from BaseEntity.EntityFunctions.select_function import Select

class IndependentCircleEntity(IndependentEntity, CircleMixin):

    def __init__(self, position: PointRef, radius: int, color: tuple, id: str):
        super().__init__(
            position = position,
            drag = DragLambda(FdragOffset = lambda offset: self.move(offset)),
            select = Select(id),
            click = ClickLambda(FonLeftClick = lambda : print("left click"), FonRightClick = lambda : print("right click"))
            )
        
        CircleMixin.__init__(self, radius, color)


    def move(self, offset: VectorRef):
        self.position += offset