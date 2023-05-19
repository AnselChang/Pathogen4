from typing import TYPE_CHECKING
from models.command_models.abstract_model import AbstractModel
if TYPE_CHECKING:
    from command_creation.command_definition_database import CommandDefinitionDatabase
    from command_creation.command_definition import CommandDefinition
    from adapter.path_adapter import PathAdapter
    from models.command_models.section_model import SectionModel

from root_container.panel_container.command_block.parameter_state import ParameterState

"""
Stores the data of a single command block
Model part of MVC design pattern for command block
"""

class CommandModel(AbstractModel['CommandModel' | SectionModel, 'CommandModel' | None]):

    def __init__(self,pathAdapter: PathAdapter):

        self.database = CommandDefinitionDatabase.getInstance()
        self.type = pathAdapter.type

        super().__init__()

        # initialize default command definition to be the first one
        self._definitionID = self.database.getDefinitionByIndex(self.type).id
        self.parameters = ParameterState(self)

        # if None, use template text in definition.
        # If not none, means there's a text editor in command and templateText is editable
        self.templateText = None 

    def createChild(self) -> 'CommandModel':
        return self.createCustomCommandModel()


    def getDefinition(self) -> CommandDefinition:
        return self.database.getDefinitionByID(self.type, self._definitionID)
    
    # whether command can contain children. Ie tasks, loops, etc
    def canHaveChildren(self) -> bool:
        return self.getDefinition().isTask
    
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