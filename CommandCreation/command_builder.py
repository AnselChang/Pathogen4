from CommandCreation.command_definition import CommandType, CommandDefinition
from Commands.command_state import CommandState
from Adapters.adapter import Adapter

"""
Stores all the different CommandDefinitions. Creates CommandStates based on CommandDefintions
"""

class CommandBuilder:

    def __init__(self):

        self.commandDefinitions : dict[CommandType, list[CommandDefinition]] = {}

    def registerCommand(self, command: CommandDefinition):
        self.commandDefinitions[command.type].append(command)

    def getCommandNames(self, type: CommandType) -> list[str]:
        return [definition.name for definition in self.commandDefinitions[type]]
    
    def getNumCommands(self, type: CommandType) -> int:
        return len(self.commandDefinitions[type])
    
    def buildCommand(self, adapter: Adapter, index: int = 0) -> CommandState:
        definition = self.commandDefinitions[adapter.type][index]
        return CommandState(definition, adapter)