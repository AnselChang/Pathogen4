from BaseEntity.entity import Entity
from reference_frame import PointRef
from BaseEntity.EntityListeners.click_listener import ClickLambda

"""
A single option object for a RadioGroup
"""
class RadioEntity(Entity):

    # id is used to distinguish between radio entities
    def __init__(self, drawOrder: int = 0, onUpdate = lambda isOn: None):
        super().__init__(click = ClickLambda(
            self,
            FonLeftClick = lambda : self.onClick(),
        ),
        drawOrder = drawOrder
        )

        self.group = None

        self.onUpdate = onUpdate

    # i is zero-indexed relative position in radio group
    def setRadioGroup(self, radioGroup, i):
        self.group = radioGroup
        self.i = i

    def onClick(self):
        old = self.isActive()
        self.group.onClick(self)
        
        if self.isActive() is not old: # if there's been a change
            self.onUpdate(self.isActive)
    
    def isActive(self) -> bool:
        return self is self.group.getActiveEntity()