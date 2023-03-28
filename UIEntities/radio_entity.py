from BaseEntity.entity import Entity
from reference_frame import PointRef
from BaseEntity.EntityFunctions.click_function import ClickLambda

# Subclasses implement: isVisible, isTouching, distanceTo, draw
class RadioEntity(Entity):

    # id is used to distinguish between radio entities
    def __init__(self, id):
        super().__init__(click = ClickLambda(
            FonLeftClick = lambda : self.onClick()
        ))

        self.group = None
        self.id = id

    def setRadioGroup(self, radioGroup):
        self.group = radioGroup

    def onClick(self):
        self.group.onClick(self)

    def toString(self) -> str:
        return self.id