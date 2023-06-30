from models.command_models.full_model import FullModel
from serialization.serializable import Serializable


class ProjectModel(Serializable):

    def __init__(self):

        self.projectName = "New Project"

        # stores model for all the commands
        self.commandsModel = FullModel()