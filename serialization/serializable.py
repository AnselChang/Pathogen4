# all classes that implement this must store only serializable data
from typing import Generic, TypeVar


class SerializedState:
    pass

T = TypeVar('T')
class Serializable(Generic[T]):

    def serialize(self) -> SerializedState | T:
        raise NotImplementedError("Must implement this method")

    @staticmethod
    def deserialize(state: SerializedState | T) -> 'Serializable':
        raise NotImplementedError("Must implement this method")