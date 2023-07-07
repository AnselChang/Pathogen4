from models.command_models.full_model import FullModel
from models.path_models.path_model import PathModel
from serialization.serializable import Serializable

"""
Stores all the state pertaining to a .pgpath file,
which contains project meta-data, path, and commands.

Should be easy to serialize, and UI should be synced with model.
"""

class ProjectModel(Serializable):

    _INSTANCE = None

    def getInstance() -> 'ProjectModel':
        if ProjectModel._INSTANCE is None:
            ProjectModel._INSTANCE = ProjectModel()

        return ProjectModel._INSTANCE

    def __init__(self):

        self.projectName = "New Project"

        # stores model for all the commands
        self.commandsModel = FullModel()

        print("commands model after init")
        self.commandsModel.tree()

        # stores model for the path
        self.pathModel = PathModel()
        self.pathModel.initCommandsModel(self.commandsModel)