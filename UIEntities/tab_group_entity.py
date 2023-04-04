from UIEntities.radio_group_entity import RadioGroupEntity
from dimensions import Dimensions

"""a group of radio_entities, where only one is selected at a time
If allowNoSelect is True, then no option being selected is allowed
Child of Panel Entity
"""
class TabGroupEntity(RadioGroupEntity):

    def __init__(self, entityManager, dimensions: Dimensions):

        super().__init__(entityManager)
        self.dimensions = dimensions

    def getTopLeft(self) -> tuple:
        return self._parent.LEFT_X, self._parent.TOP_Y

    def getWidth(self) -> float:
        return self._parent.WIDTH
    def getHeight(self) -> float:
        return 30