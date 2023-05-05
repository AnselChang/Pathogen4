from command_creation.command_definition import CommandDefinition
from command_creation.command_definition_builder import CommandDefinitionBuilder
from command_creation.command_type import CommandType
from root_container.panel_container.element.widget.checkbox_widget import CheckboxWidgetDefinition
from root_container.panel_container.element.widget.dropdown_widget import DropdownWidgetDefinition
from root_container.panel_container.element.widget.textbox_widget import CodeTextboxWidgetDefinition, ValueTextboxWidgetDefinition
from adapter.path_adapter import PathAttributeID

def goToPoint() -> CommandDefinition:
    builder = CommandDefinitionBuilder(CommandType.STRAIGHT)
    builder.setName("goToPoint()")
    builder.addReadout("X", PathAttributeID.X2)
    builder.addReadout("Y", PathAttributeID.Y2)
    builder.addWidget(ValueTextboxWidgetDefinition("Speed", 0.6))
    return builder.build()