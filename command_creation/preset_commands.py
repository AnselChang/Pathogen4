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
        from adapter.straight_adapter import StraightAttributeID
        builder = CommandDefinitionBuilder(CommandType.STRAIGHT)
        builder.setName("goForward")
        builder.addReadout("distance", StraightAttributeID.DISTANCE)
        builder.addWidget(CheckboxWidgetDefinition("checkbox1", False, "enabled a", "disabled a"))
        builder.addWidget(CheckboxWidgetDefinition("checkbox2", True, "enabled b", "disabled b"))
        return builder.build()

    def getTurnPreset(self) -> CommandDefinition:
        from adapter.turn_adapter import TurnAttributeID
        builder = CommandDefinitionBuilder(CommandType.TURN)
        builder.setName("goTurn")
        builder.addReadout("Initial angle", TurnAttributeID.THETA1)
        builder.addReadout("Final angle", TurnAttributeID.THETA2)
        #builder.addWidget(ValueTextboxWidgetDefinition("textbox", 0.5, 0.6, 3.14))
        return builder.build()

    def getCodePreset(self) -> CommandDefinition:
        builder = CommandDefinitionBuilder(CommandType.CUSTOM)
        builder.setName("code")
        #builder.setHeight(80)
        #builder.addWidget(CodeTextboxWidgetDefinition("textbox", 0.5, 0.4, 0.83))
        return builder.build()
    

