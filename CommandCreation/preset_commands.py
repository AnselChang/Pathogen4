from CommandCreation.command_definition import CommandDefinition
from CommandCreation.command_definition_builder import CommandDefinitionBuilder
from CommandCreation.command_type import CommandType
from Widgets.checkbox_widget import CheckboxWidget

"""
The default set of command definitions at the start of the program
"""

class CommandDefinitionPresets:

    def getPresets(self) -> list[CommandDefinition]:
        return self.presets

    def __init__(self):

        self.presets: list[CommandDefinition] = [
            self.getStraightPreset(),
            self.getTurnPreset(),
            self.getCodePreset()
        ]

    def getStraightPreset(self) -> CommandDefinition:
        from Adapters.straight_adapter import StraightAttributeID
        builder = CommandDefinitionBuilder(CommandType.STRAIGHT)
        builder.setName("goForward")
        builder.addReadout(StraightAttributeID.DISTANCE, 0.5, 0.5)
        builder.addWidget(CheckboxWidget(), "checkbox", 0.5, 0.75)
        return builder.build()

    def getTurnPreset(self) -> CommandDefinition:
        from Adapters.turn_adapter import TurnAttributeID
        builder = CommandDefinitionBuilder(CommandType.TURN)
        builder.setName("goTurn")
        builder.addReadout(TurnAttributeID.THETA2, 0.5, 0.5)
        return builder.build()

    def getCodePreset(self) -> CommandDefinition:
        builder = CommandDefinitionBuilder(CommandType.CUSTOM)
        builder.setName("code")
        return builder.build()
    

