from command_creation.command_definition import CommandDefinition
from command_creation.command_definition_builder import CommandDefinitionBuilder
from command_creation.command_type import CommandType
from root_container.panel_container.element.widget.checkbox_widget import CheckboxWidgetDefinition
from root_container.panel_container.element.widget.dropdown_widget import DropdownWidgetDefinition
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
        builder.addReadout("Distance", StraightAttributeID.DISTANCE)
        builder.addWidget(DropdownWidgetDefinition("Mode", ["Odometry", "IMU+Encoder", "Encoder"]))
        builder.addWidget(DropdownWidgetDefinition("Motion Profile", ["Fast", "Slow", "None"]))
        builder.addWidget(ValueTextboxWidgetDefinition("Speed", 0.75))
        return builder.build()

    def getTurnPreset(self) -> CommandDefinition:
        from adapter.turn_adapter import TurnAttributeID
        builder = CommandDefinitionBuilder(CommandType.TURN)
        builder.setName("goTurn")
        builder.addReadout("Initial angle", TurnAttributeID.THETA1)
        builder.addReadout("Final angle", TurnAttributeID.THETA2)
        builder.addWidget(ValueTextboxWidgetDefinition("Speed", 0.85))
        builder.addWidget(CheckboxWidgetDefinition("Invert direction?", False))
        return builder.build()

    def getCodePreset(self) -> CommandDefinition:
        builder = CommandDefinitionBuilder(None)
        return builder.build()
    

