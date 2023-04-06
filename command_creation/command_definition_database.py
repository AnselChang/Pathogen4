from command_creation.command_definition import CommandType, CommandDefinition
from command_creation.preset_commands import CommandDefinitionPresets
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.custom_command_block_entity import CustomCommandBlockEntity

from entity_handler.interactor import Interactor
from entity_handler.entity_manager import EntityManager

from adapter.path_adapter import PathAdapter, NullPathAdapter
from common.image_manager import ImageManager
from common.dimensions import Dimensions

"""
Stores all the different CommandDefinitions
"""

class CommandDefinitionDatabase:

    def __init__(self):

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