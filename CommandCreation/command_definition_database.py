from CommandCreation.command_definition import CommandType, CommandDefinition
from CommandCreation.preset_commands import CommandDefinitionPresets
from Commands.command_state import CommandState
from Commands.command_block_entity import CommandBlockEntity
from Commands.custom_command_block_entity import CustomCommandBlockEntity

from EntityHandler.interactor import Interactor
from EntityHandler.entity_manager import EntityManager

from Adapters.path_adapter import PathAdapter, NullPathAdapter
from image_manager import ImageManager
from dimensions import Dimensions

"""
Stores all the different CommandDefinitions. Creates CommandStates based on CommandDefintions
"""

class CommandDefinitionDatabase:

    def __init__(self, entities: EntityManager, interactor: Interactor, images: ImageManager, dimensions: Dimensions):

        self.entities = entities
        self.interactor = interactor
        self.images = images
        self.dimensions = dimensions

        # initialize empty list for each command type
        self.definitions : dict[CommandType, list[CommandDefinition]] = {}
        for type in CommandType:
            self.definitions[type] = []

        # initially populate with preset commands. make sure there's one command per type at least
        presets = CommandDefinitionPresets()
        for preset in presets.getPresets():
            self.registerDefinition(preset)

    def registerDefinition(self, command: CommandDefinition):
        self.definitions[command.type].append(command)

    def getDefinitionNames(self, type: CommandType) -> list[str]:
        return [definition.name for definition in self.definitions[type]]
    
    def getNumDefitions(self, type: CommandType) -> int:
        return len(self.definitions[type])
    
    def getDefinition(self, type: CommandType, index: int = 0) -> CommandDefinition:
        return self.definitions[type][index]
    
    # REST OF THESE DO NOT BELONG HERE
    def buildCommandState(self, adapter: PathAdapter, index: int = 0) -> CommandState:
        definition = self.definitions[adapter.type][index]
        return CommandState(definition, adapter)
    
    def buildCommand(self, adapter: PathAdapter, index: int = 0) -> CommandBlockEntity:
        assert(adapter.type != CommandType.CUSTOM)
        state = self.buildCommandState(adapter, index)
        return CommandBlockEntity(state, self.entities, self.interactor, self.images, self.dimensions)
    
    def buildCustomCommand(self, index: int = 0) -> CommandBlockEntity:
        state = self.buildCommandState(NullPathAdapter(), index)
        return CustomCommandBlockEntity(state, self.entities, self.interactor, self.images, self.dimensions)