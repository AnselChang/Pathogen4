from command_creation.command_definition import CommandDefinition
from command_creation.command_definition_builder import CommandDefinitionBuilder
from command_creation.command_type import CommandType
from root_container.panel_container.element.widget.checkbox_widget import CheckboxWidgetDefinition
from root_container.panel_container.element.widget.textbox_widget import CodeTextboxWidgetDefinition, ValueTextboxWidgetDefinition

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
        builder.addReadout(StraightAttributeID.DISTANCE, 0.5, 0.25)
        builder.addWidget(CheckboxWidgetDefinition("checkbox", 0.35, 0.75, False, "enabled a", "disabled a"))
        builder.addWidget(CheckboxWidgetDefinition("checkbox", 0.65, 0.75, True, "enabled b", "disabled b"))
        return builder.build()

    def getTurnPreset(self) -> CommandDefinition:
        from Adapters.turn_adapter import TurnAttributeID
        builder = CommandDefinitionBuilder(CommandType.TURN)
        builder.setName("goTurn")
        builder.addReadout(TurnAttributeID.THETA2, 0.5, 0.3)
        builder.addWidget(ValueTextboxWidgetDefinition("textbox", 0.5, 0.6, 3.14))
        return builder.build()

    def getCodePreset(self) -> CommandDefinition:
        builder = CommandDefinitionBuilder(CommandType.CUSTOM)
        builder.setName("code")
        builder.setHeight(80)
        builder.addWidget(CodeTextboxWidgetDefinition("textbox", 0.5, 0.4, 0.83))
        return builder.build()
    

