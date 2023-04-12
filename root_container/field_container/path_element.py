"""
A PathNodeEntity or PathSegment entity
"""

from typing import Generic, TypeVar
from data_structures.linked_list import LinkedListNode

T = TypeVar('T')
class PathElement(LinkedListNode, Generic[T]):
    pass