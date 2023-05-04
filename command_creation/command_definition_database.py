from command_creation.command_definition import CommandType, CommandDefinition
from command_creation.preset_commands import CommandDefinitionPresets
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.custom_command_block_entity import CustomCommandBlockEntity

from entity_handler.interactor import Interactor
from entity_handler.entity_manager import EntityManager

from adapter.path_adapter import PathAdapter, NullPathAdapter, PathAttributeID
from common.image_manager import ImageManager
from common.dimensions import Dimensions
from root_container.panel_container.element.readout.readout_definition import ReadoutDefinition
from root_container.panel_container.element.row.element_definition import ElementDefinition, ElementType
import json

"""
Stores all the different CommandDefinitions
"""

class CommandDefinitionDatabase:

    def __init__(self):

        # initialize empty list for each command type
        self.definitions : dict[CommandType, dict[str, CommandDefinition]] = {}
        for type in CommandType:
            self.definitions[type] = {}

        # initially populate with preset commands. make sure there's one command per type at least
        presets = CommandDefinitionPresets()
        for preset in presets.getPresets():
            self.registerDefinition(preset)

    # add a (id, command) pair to definitions
    def registerDefinition(self, command: CommandDefinition):
        self.definitions[command.type][command.id] = command

    def getDefinitionNames(self, type: CommandType, isInTask: bool = False) -> list[str]:
        return [definition.name for definition in self.definitions[type].values()
                if (not isInTask or definition.allowedInTask)]
    
    def getNumDefitions(self, type: CommandType) -> int:
        return len(self.definitions[type])
    
    def getDefinitionByIndex(self, type: CommandType, index: int = 0) -> CommandDefinition:
        return list(self.definitions[type].values())[index]
    
    def getDefinitionByID(self, type: CommandType, id: str) -> CommandDefinition:
        return self.definitions[type][id]
    
    def getDefinitionIDByName(self, type: CommandType, name: str) -> int:
        definitions = self.definitions[type]
        for id in definitions:
            if definitions[id].name == name:
                return id
        raise Exception("No definition with name " + name + " found")

    # generate a dictionary of all the command definitions, and convert to json
    def exportToJson(self) -> dict:

        dictionary = {}
        for type in self.definitions:
            definitions = self.definitions[type]

            commandDict = {}
            for commandID in definitions:
                commandDefinition = definitions[commandID]
                commandDict[commandID] = self.encodeCommandDefinition(commandDefinition)
            dictionary[type.name] = commandDict

        return dictionary
    
    def encodeCommandElements(self, elements: list[ElementDefinition]) -> list:
        elementList = []
        for elementDefinition in elements:

            elementID: int = elementDefinition.id # numeric id of element
            elementType: ElementType = elementDefinition.elementType # readout/textbox/checkbox/etc
            variableName: str = elementDefinition.variableName # label name
            pathAttributeID: PathAttributeID = elementDefinition.pathAttributeID

            elementList.append({
                "id": elementID,
                "type": elementType.name,
                "name": variableName,
                "pathAttributeID": pathAttributeID.name
            })
        return elementList
    
    def encodeCommandDefinition(self, commandDefinition: CommandDefinition):

        elementList = self.encodeCommandElements(commandDefinition.elements)

        return {
            "name": commandDefinition.name,
            "elements": elementList,
            "templateText": commandDefinition.templateText,
            "isCode": commandDefinition.isCode,
            "isTask": commandDefinition.isTask,
            "nonblockingEnabled": commandDefinition.nonblockingEnabled,
            "allowedInTask": commandDefinition.allowedInTask
        }