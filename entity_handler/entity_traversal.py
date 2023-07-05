from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity_handler.entity_manager import EntityManager

from enum import Enum
from typing import Iterator
import entity_base.entity as entity

"""
Handles postfix or prefix traversal of entities
Useful for determining mouse interaction or drawing order
"""

class TraversalOrder(Enum):
    DRAW = 0
    MOUSE = 1

def _traverseEntities(current: entity.Entity, order: TraversalOrder, ignoreOutside: bool = False) -> Iterator[entity.Entity]:

    if ignoreOutside and not current.drawOrderRecursive:
        return

    if order == TraversalOrder.DRAW:
        yield current

    sortedChildren = sorted(
        current._children,
        key = lambda entity: (entity.drawOrder, 0 if entity.drawOrderTiebreaker() is None else (-entity.drawOrderTiebreaker())),
        reverse = (order == TraversalOrder.DRAW)
    )

    for child in sortedChildren:
        yield from _traverseEntities(child, order, ignoreOutside)

    if order == TraversalOrder.MOUSE:
        yield current

# A generator for all entities in the tree
# Either postfix or prefix
def traverseEntities(manager: EntityManager, order: TraversalOrder) -> Iterator[entity.Entity]:

    yield from _traverseEntities(entity.ROOT_CONTAINER, order, ignoreOutside = (order == TraversalOrder.DRAW))

    if order == TraversalOrder.DRAW:
        for e in manager.outsideEntites:
            yield from _traverseEntities(e, order, ignoreOutside = False)