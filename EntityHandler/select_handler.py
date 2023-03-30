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

    def hasOnly(self, entity: Entity) -> bool:
        return len(self.entities) == 1 and entity is self.entities[0]