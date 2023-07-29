from __future__ import annotations
from typing import TYPE_CHECKING
import typing
from entity_base.entity import Entity
from models.command_models.abstract_model import SerializedRecursiveState

from models.project_data_model import ProjectDataModel, SerializedProjectDataState
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
                 data: SerializedProjectDataState,
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
        self._projectData = ProjectDataModel()

        # stores model for all the commands
        self._commandsModel = FullCommandsModel()

        # stores model for the path
        self._pathModel = PathModel()
        self._pathModel.initCommandsModel(self._commandsModel)

    def getData(self) -> ProjectDataModel:
        return self._projectData
    
    def getCommands(self) -> FullCommandsModel:
        return self._commandsModel
    
    def getPath(self) -> PathModel:
        return self._pathModel

    # link the path model to the field entity
    def initFieldEntity(self, fieldEntity: FieldEntity):
        self.fieldEntity = fieldEntity
        self._pathModel.initFieldEntity(fieldEntity)
        fieldEntity.initPathModel(self._pathModel)

    def initCommandParentEntity(self, parentCommandEntity: Entity):
        self.parentCommandEntity = parentCommandEntity

    # Serialize and return the entire project model.
    # Make a deepcopy, so that the original model is not modified.
    def serialize(self) -> SerializedProjectState:

        # convert all the adapters to serialized states first
        self._commandsModel.makeNullAdapterSerialized()
        for element in self._pathModel.pathList:
            element.makeAdapterSerialized()

        commands = self._commandsModel.serialize()
        path = self._pathModel.serialize()

        state = SerializedProjectState(self._projectData.serialize(), commands, path)
        print(state)
        stateCopy = copy.deepcopy(state)

        return stateCopy

    # given a serialized state, update the project model and ui
    def loadSerializedState(self, state: SerializedProjectState):

        # delete all the path ui
        for element in self._pathModel.pathList:
            element.ui.deleteEntity()

        # delete all the commands ui
        self._commandsModel.ui.deleteEntity()

        # convert all adapters back to deserialized states
        state.commands.makeNullAdapterDeserialized()
        for element in state.path.pathList:
            element.makeAdapterDeserialized()

        # load the project data
        self._projectData.deserialize(state.data)

        # load the commands and rebuild the command tree
        self._commandsModel = typing.cast(FullCommandsModel, FullCommandsModel.deserialize(state.commands))
        self._commandsModel.fullModelParentUI = self.parentCommandEntity
        self._commandsModel.rebuildAll()

        # load the path and link with field entity
        self._pathModel = PathModel.deserialize(state.path, self.fieldEntity)
        self.initFieldEntity(self.fieldEntity)

        self._pathModel.initCommandsModel(self._commandsModel)

        # recalculate path cached data
        self._pathModel.recalculateAll()

        # update the UI
        self.fieldEntity.recomputeEntity()
        self._commandsModel.recomputeUI()

        # select the selected entities at this state
        self.fieldEntity.interactor.removeAllEntities()
        for selectedNodeOrSegmentSerialized in state.path.selected:
            selectedNodeOrSegment = selectedNodeOrSegmentSerialized.deserialize()
            self.fieldEntity.interactor.addEntity(selectedNodeOrSegment.ui)

        

        #self.commandsModel.tree()
        #print(self.pathModel.pathList)