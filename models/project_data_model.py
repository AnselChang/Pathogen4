# everything is already serialized, no need to designate a serialized state
from data_structures.variable import Variable
from serialization.serializable import Serializable


class ProjectDataModel(Serializable):

    def __init__(self):
        self.projectName = Variable("New Project")

    def serialize(self) -> 'ProjectDataModel':
        return self

    @staticmethod
    def deserialize(state: 'ProjectDataModel') -> 'Serializable':
        return state