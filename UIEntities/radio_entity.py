from BaseEntity.entity import Entity
from reference_frame import PointRef
from BaseEntity.EntityListeners.click_listener import ClickLambda

"""
A single option object for a RadioGroup
"""
class RadioEntity(Entity):

    # id is used to distinguish between radio entities
    def __init__(self, id, drawOrder: int = 0, onUpdate = lambda isOn: None):
        super().__init__(click = ClickLambda(
            self,
            FonLeftClick = lambda : self.onClick(),
        ),
        drawOrder = drawOrder
        )

        self.group = None
        self.id = id

        self.onUpdate = onUpdate

    def setRadioGroup(self, radioGroup):
        self.group = radioGroup

    def onClick(self):
        old = self.isActive()
        self.group.onClick(self)
        
        if self.isActive() is not old: # if there's been a change
            self.onUpdate(self.isActive)


    def toString(self) -> str:
        return self.id
    
    def isActive(self) -> bool:
        return self is self.group.getActiveEntity()