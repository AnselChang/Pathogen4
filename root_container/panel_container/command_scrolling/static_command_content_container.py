from entity_base.container_entity import Container
from entity_base.entity import Entity

class StaticCommandContentContainer(Container):

    def __init__(self, parent: Entity):
        super().__init__(parent)
        self.recomputePosition()

    def defineCenterX(self) -> float:
        return self._px(0.5)
    
    def defineTopY(self) -> float:
        return self._ay(30)
    
    def defineBottomY(self) -> float:
        return self._ay(50)
    
    def defineWidth(self) -> float:
        return self._pwidth(0.9)