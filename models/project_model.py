from __future__ import annotations
from typing import TYPE_CHECKING

from models.project_data_model import ProjectDataModel
import copy

if TYPE_CHECKING:
    from entities.root_container.field_container.field_entity import FieldEntity

from models.path_models.path_model import PathModel, SerializedPathState
from models.command_models.full_model import FullCommandsModel, SerializedCommandsState

from data_structures.variable import Variable

from serialization.serializable import Serializable, SerializedState

"""
A serializable object containing all the data for the project.
This can be stored in an ordered list for undo/redo, and can
be exported or imported to save or load.
"""
class SerializedProjectState(SerializedState):
    def __init__(self,
                 data: ProjectDataModel,
                 commands: SerializedCommandsState,
                 path: SerializedPathState,
                 ):
        self.data = data
        self.commands = commands
        self.path = path

"""
Stores all the state pertaining to a .pgpath file,
which contains project meta-data, path, and commands.

Should be easy to serialize, and UI should be synced with model.
"""
class ProjectModel:

    _INSTANCE = None

    def getInstance() -> 'ProjectModel':
        if ProjectModel._INSTANCE is None:
            ProjectModel._INSTANCE = ProjectModel()

        return ProjectModel._INSTANCE

    def __init__(self):

        # stores all the project attributes
        self.projectData = ProjectDataModel()

        # stores model for all the commands
        self.commandsModel = FullCommandsModel()

        # stores model for the path
        self.pathModel = PathModel()
        self.pathModel.initCommandsModel(self.commandsModel)

    # link the path model to the field entity
    def initFieldEntity(self, fieldEntity: FieldEntity):
        self.fieldEntity = fieldEntity

        self.pathModel.initFieldEntity(fieldEntity)
        fieldEntity.initPathModel(self.pathModel)

    # Serialize and return the entire project model.
    # Make a deepcopy, so that the original model is not modified.
    def serialize(self) -> SerializedProjectState:

        commands = self.commandsModel.serialize()
        path = self.pathModel.serialize()

        state = SerializedProjectState(self.projectData, commands, path)
        stateCopy = copy.deepcopy(state)

        return stateCopy

    # given a serialized state, update the project model and ui
    def loadSerializedState(self, state: SerializedProjectState):

        # load the project data
        self.projectData = state.data

        # load the path and link with field entity
        self.pathModel = PathModel.deserialize(state.path)
        self.initFieldEntity(self.fieldEntity)

        # load the commands and rebuild the command tree
        self.commandsModel = FullCommandsModel.deserialize(state.commands)
        self.commandsModel.rebuildAll()

        # update the UI
        self.fieldEntity.recomputeEntity()
        self.commandsModel.recomputeUI()