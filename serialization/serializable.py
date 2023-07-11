# all classes that implement this must store only serializable data
from typing import Generic, TypeVar

from utility.pretty_printer import PrettyPrinter


class SerializedState(PrettyPrinter):
    pass

T = TypeVar('T')
class Serializable(Generic[T]):

    def serialize(self) -> SerializedState | T:
        raise NotImplementedError("Must implement this method")

    @staticmethod
    def deserialize(state: SerializedState | T) -> 'Serializable':
        raise NotImplementedError("Must implement this method")