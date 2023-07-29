# everything is already serialized, no need to designate a serialized state
from data_structures.variable import Variable
from serialization.serializable import Serializable

class SerializedProjectDataState(Serializable):
    def __init__(self, projectName: str):
        self.projectName = projectName

class ProjectDataModel(Serializable):

    def __init__(self):
        self.projectName = Variable("New Project")

    def serialize(self) -> 'SerializedProjectDataState':
        return SerializedProjectDataState(self.projectName.get())

    def deserialize(self, state: 'SerializedProjectDataState'):
        self.projectName.set(state.projectName)
