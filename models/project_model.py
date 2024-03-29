from __future__ import annotations
from typing import TYPE_CHECKING
import typing
from entity_base.entity import Entity
from models.command_models.abstract_model import SerializedRecursiveState

from models.project_data_model import ProjectDataModel
import copy

if TYPE_CHECKING:
    from entities.root_container.field_container.field_entity import FieldEntity

from models.path_models.path_model import PathModel, SerializedPathState
from models.command_models.full_model import FullCommandsModel

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
                 commands: SerializedRecursiveState,
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

    def initCommandParentEntity(self, parentCommandEntity: Entity):
        self.parentCommandEntity = parentCommandEntity

    # Serialize and return the entire project model.
    # Make a deepcopy, so that the original model is not modified.
    def serialize(self) -> SerializedProjectState:

        # convert all the adapters to serialized states first
        self.commandsModel.makeNullAdapterSerialized()
        for element in self.pathModel.pathList:
            element.makeAdapterSerialized()

        commands = self.commandsModel.serialize()
        path = self.pathModel.serialize()

        state = SerializedProjectState(self.projectData, commands, path)
        stateCopy = copy.deepcopy(state)

        return stateCopy

    # given a serialized state, update the project model and ui
    def loadSerializedState(self, state: SerializedProjectState):

        # delete all the path ui
        for element in self.pathModel.pathList:
            element.ui.deleteEntity()

        # delete all the commands ui
        self.commandsModel.ui.deleteEntity()

        # convert all adapters back to deserialized states
        state.commands.makeNullAdapterDeserialized()
        for element in state.path.pathList:
            element.makeAdapterDeserialized()

        # load the project data
        self.projectData = state.data

        # load the commands and rebuild the command tree
        self.commandsModel = typing.cast(FullCommandsModel, FullCommandsModel.deserialize(state.commands))
        self.commandsModel.fullModelParentUI = self.parentCommandEntity
        self.commandsModel.rebuildAll()

        # load the path and link with field entity
        self.pathModel = PathModel.deserialize(state.path, self.fieldEntity)
        self.initFieldEntity(self.fieldEntity)

        self.pathModel.initCommandsModel(self.commandsModel)

        # recalculate path cached data
        self.pathModel.recalculateAll()

        # update the UI
        self.fieldEntity.recomputeEntity()
        self.commandsModel.recomputeUI()

        # select the selected entities at this state
        self.fieldEntity.interactor.removeAllEntities()
        for selectedNodeOrSegmentSerialized in state.path.selected:
            selectedNodeOrSegment = selectedNodeOrSegmentSerialized.deserialize()
            self.fieldEntity.interactor.addEntity(selectedNodeOrSegment.ui)

        

        #self.commandsModel.tree()
        #print(self.pathModel.pathList)