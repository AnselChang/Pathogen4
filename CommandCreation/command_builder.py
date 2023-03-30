from CommandCreation.command_definition import CommandType, CommandDefinition
from CommandCreation.preset_commands import CommandDefinitionPresets
from Commands.command_state import CommandState
from Commands.command_block_entity import CommandBlockEntity
from Adapters.adapter import Adapter
from dimensions import Dimensions

"""
Stores all the different CommandDefinitions. Creates CommandStates based on CommandDefintions
"""

class CommandBuilder:

    def __init__(self, dimensions: Dimensions):

        self.dimensions = dimensions

        # initialize empty list for each command type
        self.commandDefinitions : dict[CommandType, list[CommandDefinition]] = {}
        for type in CommandType:
            self.commandDefinitions[type] = []

        # initially populate with preset commands. make sure there's one command per type at least
        presets = CommandDefinitionPresets()
        for preset in presets.getPresets():
            self.registerCommand(preset)

    def registerCommand(self, command: CommandDefinition):
        self.commandDefinitions[command.type].append(command)

    def getCommandNames(self, type: CommandType) -> list[str]:
        return [definition.name for definition in self.commandDefinitions[type]]
    
    def getNumCommands(self, type: CommandType) -> int:
        return len(self.commandDefinitions[type])
    
    def buildCommandState(self, adapter: Adapter, index: int = 0) -> CommandState:
        definition = self.commandDefinitions[adapter.type][index]
        return CommandState(definition, adapter)
    
    def buildCommand(self, adapter: Adapter, index: int = 0) -> CommandBlockEntity:
        state = self.buildCommandState(adapter, index)
        return CommandBlockEntity(state, self.dimensions)