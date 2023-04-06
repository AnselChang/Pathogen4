from BaseEntity.entity import Entity

"""
Means that the entity itself is not interactable or drawable.
Simply, it is a container used for positioning child entities

However, it is useful to set isVisible() for classes subclassing ContainerEntity,
as that will affect child entities without affecting itself
"""

class ContainerEntity(Entity):

    def isTouching(self, position: tuple) -> bool:
        return False