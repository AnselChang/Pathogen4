from BaseEntity.entity import Entity
from BaseEntity.EntityFunctions.select_function import Select
from reference_frame import PointRef
from math_functions import isInsideBox

# handle what can be selected with other entities and what cannot
class SelectHandler:

    def __init__(self):

        self.entities: list[Entity] = []

    # return true if successful add
    def add(self, entity: Entity) -> bool:
        self.entities.append(entity)
        return True

    def remove(self, entity: Entity) -> None:
        self.entities.remove(entity)

    def removeAll(self):
        self.entities.clear()