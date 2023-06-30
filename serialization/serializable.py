# all classes that implement this must store only serializable data
class SerializedState:
    pass

class Serializable:

    def serialize(self) -> SerializedState:
        raise NotImplementedError("Must implement this method")

    @staticmethod
    def deserialize(state: SerializedState) -> 'Serializable':
        raise NotImplementedError("Must implement this method")