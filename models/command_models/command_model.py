from typing import TYPE_CHECKING
from command_creation.command_type import CommandType
from data_structures.observer import NotifyType, Observer
from models.command_models.abstract_model import AbstractModel
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from command_creation.command_definition_database import CommandDefinitionDatabase

    
from models.command_models.section_model import SectionModel
from entity_base.entity import Entity
from adapter.path_adapter import PathAdapter
from models.command_models.model_based_entity import ModelBasedEntity
from command_creation.command_definition import CommandDefinition


from root_container.panel_container.command_block.parameter_state import ParameterState

"""
Stores the data of a single command block
Model part of MVC design pattern for command block
"""

class CommandModel(AbstractModel, Observer):

    def __init__(self, pathAdapter: 'PathAdapter'):

        self.database = CommandDefinitionDatabase.getInstance()
        self.adapter = pathAdapter
        self.type = pathAdapter.type

        super().__init__()

        # initialize default command definition to be the first one
        self._definitionID = self.database.getDefinitionByIndex(self.type).id
        self.parameters = ParameterState(self)

        # if None, use template text in definition.
        # If not none, means there's a text editor in command and templateText is editable
        self.templateText = None 

        # subscribe to changes in the database
        self.database.subscribe(self, onNotify = self.onCommandDefinitionChange)

        # For turn commands: if turn is enabled/disabled, command is shown/hidden
        if self.adapter.type == CommandType.TURN:
            self.adapter.subscribe(self, id = NotifyType.TURN_ENABLE_TOGGLED, onNotify = self.onTurnEnableToggled)

        self.onTurnEnableToggled()

    def onCommandDefinitionChange(self):
        print("CommandModel: onCommandDefinitionChange")

    def onTurnEnableToggled(self):
        print("CommandModel: onTurnEnableToggled")

    def isHighlighted(self):
        return False
    
    def getCommandType(self) -> CommandType:
        return self.type

    def _createChild(self) -> 'CommandModel':
        return self.createCustomCommandModel()
    
    # whether command can contain children. Ie tasks, loops, etc
    def _canHaveChildren(self) -> bool:
        return self.getDefinition().isTask
    
    def _generateUIForMyself(self) -> ModelBasedEntity | Entity:
        return CommandBlockEntity(self.getParentUI(), self)

    def getDefinition(self) -> CommandDefinition:
        return self.database.getDefinitionByID(self.type, self._definitionID)
    
    def getType(self) -> CommandType:
        return self.type

    def getAdapter(self) -> PathAdapter:
        return self.adapter

    
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
        return self.database.getDefinitionNames(self.type)