from BaseEntity.entity import Entity

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