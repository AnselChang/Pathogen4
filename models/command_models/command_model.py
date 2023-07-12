from typing import TYPE_CHECKING
from command_creation.command_type import CommandType
from data_structures.observer import NotifyType, Observer
from models.command_models.abstract_model import AbstractModel, SerializedRecursiveState
from entities.root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from command_creation.command_definition_database import CommandDefinitionDatabase

    
from entity_base.entity import Entity
from adapter.path_adapter import PathAdapter
from models.command_models.model_based_entity import ModelBasedEntity
from command_creation.command_definition import CommandDefinition
from entities.root_container.panel_container.command_block.custom_command_block_entity import CustomCommandBlockEntity


from entities.root_container.panel_container.command_block.parameter_state import ParameterState
from serialization.serializable import SerializedState

class SerializedCommandState(SerializedRecursiveState):

    def __init__(self, uiState: 'SharedCommandUIState', adapter: PathAdapter, templateText: str):
        super().__init__()
        self.uiState = uiState
        self.adapter = adapter.serialize()
        self.templateText = templateText

    def _deserialize(self) -> 'CommandModel':
        model = CommandModel(self.adapter.deserialize())
        model.uiState = self.uiState
        model.templateText = self.templateText
        return model
    
    def makeNullAdapterDeserialized(self):
        if self.adapter.type == CommandType.CUSTOM:
            self.adapter.makeDeserialized()
        super().makeNullAdapterDeserialized()

# singleton for state shared by all commands, like highlight
class SharedCommandUIState:

    _INSTANCE = None
    def __init__(self):
        if SharedCommandUIState._INSTANCE is not None:
            raise Exception("Singleton cannot be re-instantiated.")
        
        self.highlightedModel: 'CommandModel' = None

    def getInstance() -> 'SharedCommandUIState':
        return SharedCommandUIState._INSTANCE
SharedCommandUIState._INSTANCE = SharedCommandUIState()

# each command has its own CommandUIState
class CommandUIState:

    def __init__(self, expanded = True, highlighted = False):
        self.expanded = expanded

"""
Stores the data of a single command block
Model part of MVC design pattern for command block
"""
class CommandModel(AbstractModel, Observer):

    def makeNullAdapterSerialized(self):
        if self.adapter.type == CommandType.CUSTOM:
            self.adapter.makeSerialized()
        super().makeNullAdapterSerialized()

    def _serialize(self) -> SerializedCommandState:
        return SerializedCommandState(self.uiState, self.adapter, self.templateText)

    def __init__(self, pathAdapter: 'PathAdapter'):

        super().__init__()

        self.uiState: CommandUIState = CommandUIState(expanded = pathAdapter.type == CommandType.CUSTOM)
        self.uiSharedState: SharedCommandUIState = SharedCommandUIState.getInstance()

        self.database = CommandDefinitionDatabase.getInstance()
        # subscribe to changes in the database
        self.database.subscribe(self, onNotify = self.onCommandDefinitionChange)

        self.adapter: PathAdapter = None
        self.setNewAdapter(pathAdapter)

        # if None, use template text in definition.
        # If not none, means there's a text editor in command and templateText is editable
        self.templateText = None


    def setNewAdapter(self, newAdapter: 'PathAdapter'):

        if self.adapter is not None:
            self.adapter.unsubscribeAll()
        
        self.adapter = newAdapter

        # initialize default command definition to be the first one
        self._definitionID = self.database.getDefinitionByIndex(self.adapter.type).id
        self.parameters = ParameterState(self)

        # For turn commands: if turn is enabled/disabled, command is shown/hidden
        if self.adapter.type == CommandType.TURN:
            self.adapter.subscribe(self, id = NotifyType.TURN_ENABLE_TOGGLED, onNotify = self.onTurnEnableToggled)
            self.onTurnEnableToggled(recompute = False)

    def expandUI(self):
        self.uiState.expanded = True
        self.uiSharedState.highlightedModel = None
        self.ui.recomputeEntity()

    def collapseUI(self):
        self.uiState.expanded = False
        self.uiSharedState.highlightedModel = None
        self.ui.recomputeEntity()

    def highlightUI(self):
        self.uiSharedState.highlightedModel = self
        self.uiState.expanded = True
        self.getRootModel().ui.recomputeEntity()

    def wasModified(self):
        return self.show and self.adapter.wasModified()
    
    def resetModified(self):
        self.adapter.resetModified()

    def onCommandDefinitionChange(self):
        print("CommandModel: onCommandDefinitionChange")

    def onTurnEnableToggled(self, recompute: bool = True):
        commandEntity: CommandBlockEntity = self.ui

        if self.adapter.turnEnabled:
            self.showUI()
        else:
            self.hideUI()

        if recompute:
            self.parent.ui.recomputeEntity()

    def isHighlighted(self):
        return self.uiSharedState.highlightedModel is self
    
    def getCommandType(self) -> CommandType:
        return self.adapter.type

    def _createChild(self) -> 'CommandModel':
        return CommandModel(NullPathAdapter())
    
    # whether command can contain children. Ie tasks, loops, etc
    def _canHaveChildren(self) -> bool:
        return self.isTask()
    
    def _generateUIForMyself(self) -> ModelBasedEntity | Entity:
        if self.getCommandType() == CommandType.CUSTOM:
            return CustomCommandBlockEntity(None, self)
        else:
            return CommandBlockEntity(None, self)
        
    def getName(self):
        return f"{self.getCommandType()} {self.getFunctionName()}"

    def getDefinition(self) -> CommandDefinition:
        #print("getdef", self.getCommandType(), self.database.getDefinitionNames(self.getCommandType()))
        return self.database.getDefinitionByID(self.getCommandType(), self._definitionID)
    
    def getParameters(self) -> ParameterState:
        return self.parameters

    def getAdapter(self) -> PathAdapter:
        return self.adapter
    
    def isTask(self) -> bool:
        return self.getDefinition().isTask
    
    
    def setDefinitionID(self, id: str):
        print("setDefinitionID", id)
        self._definitionID = id
    
    def getGeneratedCode(self) -> str:
        
        # get template text from command definition if not set
        if self.templateText is None:
            templateText = self.getDefinition().templateText
        else:
            templateText = self.templateText

        # replace all parameters with their values
        # TODO

        return templateText

    def getFunctionName(self) -> str:
        return self.getDefinition().name
    
    def getFunctionNameOptions(self):
        return self.database.getDefinitionNames(self.getCommandType())