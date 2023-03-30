from CommandCreation.command_definition import CommandDefinition
from CommandCreation.command_type import CommandType

class CommandDefinitionPresets:

    def __init__(self):

        self.presets: list[CommandDefinition] = [
            CommandDefinition(CommandType.STRAIGHT, "goForward"),
            CommandDefinition(CommandType.TURN, "goTurn")
        ]

    def getPresets(self) -> list[CommandDefinition]:
        return self.presets

