from enum import Enum
from typing import Iterator
import entity_base.entity as entity

"""
Handles postfix or prefix traversal of entities
Useful for determining mouse interaction or drawing order
"""

class TraversalOrder(Enum):
    PREFIX = 0
    POSTFIX = 1

def _traverseEntities(current: entity.Entity, order: TraversalOrder) -> Iterator[entity.Entity]:

    if order == TraversalOrder.PREFIX:
        yield current

    sortedChildren = sorted(
        current._children,
        key = lambda entity: (entity.drawOrder, 0 if entity.drawOrderTiebreaker() is None else (-entity.drawOrderTiebreaker())),
        reverse = (order == TraversalOrder.PREFIX)
    )

    for child in sortedChildren:
        yield from _traverseEntities(child, order)

    if order == TraversalOrder.POSTFIX:
        yield current

# A generator for all entities in the tree
# Either postfix or prefix
def traverseEntities(order: TraversalOrder) -> Iterator[entity.Entity]:
    yield from _traverseEntities(entity.ROOT_CONTAINER, order)