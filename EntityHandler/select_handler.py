from BaseEntity.entity import Entity
from BaseEntity.EntityFunctions.select_function import Select
from reference_frame import PointRef
from math_functions import isInsideBox

class SelectHandler:

    def startSelection(self, mouseStartPosition: PointRef):
        self.x1, self.y1 = mouseStartPosition.screenRef
        self.selectionID = None

    # Whether at least one of the hitbox points fall inside the multiselect rectangle
    def isSelecting(self, entity: Entity, x2, y2):
        for point in entity.select.getHitboxPoints():
            if isInsideBox(*point.screenRef, self.x1, self.y1, x2, y2):
                return True
        return False

    # return if adding entity is successful
    def updateSelection(self, mousePosition: PointRef, entities: list[Entity]) -> list[Entity]:

        x2, y2 = mousePosition.screenRef
        self.selected: list[Entity] = []
        for entity in entities:

            # not a multi-selectable entitity
            if entity.select is None:
                continue

            if self.isSelecting(entity, x2, y2):
 
                # Define what other entities are selectable after the first entity is selected
                if self.selectionID is None:
                    self.selectionID = entity.select.id

                # assert this entity is the same type as the other selected ones
                if self.selectionID == entity.select.id:
                    self.selected.append(entity)

        return self.selected