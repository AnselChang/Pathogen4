from models.command_models.full_model import FullModel
from models.path_models.path_model import PathModel
from serialization.serializable import Serializable


class ProjectModel(Serializable):

    def __init__(self):

        self.projectName = "New Project"

        # stores model for all the commands
        self.commandsModel = FullModel()

        # stores model for the path
        self.pathModel = PathModel()
        self.pathModel.initCommandsModel(self.commandsModel)