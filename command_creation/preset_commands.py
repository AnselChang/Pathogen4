from command_creation.command_definition import CommandDefinition
from command_creation.command_definition_builder import CommandDefinitionBuilder
from command_creation.command_type import CommandType
from root_container.panel_container.element.widget.checkbox_widget import CheckboxWidgetDefinition
from root_container.panel_container.element.widget.dropdown_widget import DropdownWidgetDefinition
from root_container.panel_container.element.widget.textbox_widget import CodeTextboxWidgetDefinition, ValueTextboxWidgetDefinition
from functools import wraps
import inspect


# A decorator that adds the decorated function to the list of presets
def preset(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if not hasattr(self, 'presets'):
            self.presets = []
        self.presets.append(result)
        return result
    return wrapper


"""
The default set of command definitions at the start of the program.
To add a preset, simply create a function inside the CommandDefinitionPresets
class that returns a CommandDefinition, and decorate it with @preset
"""
class CommandDefinitionPresets:

    def getPresets(self) -> list[CommandDefinition]:
        return self.presets
    
    def __init__(self):
        self.presets: list[CommandDefinition] = []

        # Call all instance methods decorated with @preset
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if getattr(method, '__wrapped__', None) is not None:
                method()

        # add a custom code editor command option to each command type
        for commandType in CommandType:
            builder = CommandDefinitionBuilder(commandType, True)
            builder.setName("[manual set]")
            command = builder.build()

            self.presets.append(command)

    @preset
    def goForward(self) -> CommandDefinition:
        from adapter.straight_adapter import StraightAttributeID
        builder = CommandDefinitionBuilder(CommandType.STRAIGHT)
        builder.setName("goForward()")
        builder.addReadout("Distance", StraightAttributeID.DISTANCE)
        builder.addWidget(DropdownWidgetDefinition("Mode", ["Odometry", "IMU+Encoder", "Encoder"]))
        builder.addWidget(DropdownWidgetDefinition("Motion Profile", ["Fast", "Slow", "None"]))
        builder.addWidget(ValueTextboxWidgetDefinition("Speed", 0.75))
        return builder.build()
    
    @preset
    def goForwardTime(self) -> CommandDefinition:
        from adapter.straight_adapter import StraightAttributeID
        builder = CommandDefinitionBuilder(CommandType.STRAIGHT)
        builder.setName("goForwardTime()")
        builder.addReadout("Distance", StraightAttributeID.DISTANCE)
        builder.addWidget(ValueTextboxWidgetDefinition("Speed", 0.75))
        builder.addWidget(ValueTextboxWidgetDefinition("Time (s)", 1.0))
        return builder.build()

    @preset
    def goTurn(self) -> CommandDefinition:
        from adapter.turn_adapter import TurnAttributeID
        builder = CommandDefinitionBuilder(CommandType.TURN)
        builder.setName("goTurn()")
        builder.addReadout("Initial angle", TurnAttributeID.THETA1)
        builder.addReadout("Final angle", TurnAttributeID.THETA2)
        builder.addWidget(ValueTextboxWidgetDefinition("Speed", 0.85))
        builder.addWidget(CheckboxWidgetDefinition("Invert direction?", False))
        return builder.build()
    
    @preset
    def goArc(self) -> CommandDefinition:
        from adapter.arc_adapter import ArcAttributeID
        builder = CommandDefinitionBuilder(CommandType.ARC)
        builder.setName("goArc()")
        builder.addReadout("Arc length", ArcAttributeID.ARC_LENGTH)
        builder.addReadout("Initial angle", ArcAttributeID.THETA1)
        builder.addReadout("Final angle", ArcAttributeID.THETA2)
        builder.addReadout("Radius", ArcAttributeID.RADIUS)
        builder.addWidget(ValueTextboxWidgetDefinition("Speed", 0.85))
        builder.addWidget(CheckboxWidgetDefinition("IMU correction?", False))
        return builder.build()
    
    @preset
    def goPurePursuit(self) -> CommandDefinition:
        from adapter.bezier_adapter import BezierAttributeID
        builder = CommandDefinitionBuilder(CommandType.BEZIER)
        builder.setName("goPurePursuit()")
        builder.addReadout("Initial angle", BezierAttributeID.THETA1)
        builder.addReadout("Final angle", BezierAttributeID.THETA2)
        builder.addWidget(ValueTextboxWidgetDefinition("Speed", 0.85))
        builder.addWidget(ValueTextboxWidgetDefinition("Lookahead Distance", 10))
        return builder.build()
    
    @preset
    def goStanley(self) -> CommandDefinition:
        from adapter.bezier_adapter import BezierAttributeID
        builder = CommandDefinitionBuilder(CommandType.BEZIER)
        builder.setName("goStanley()")
        builder.addReadout("Initial angle", BezierAttributeID.THETA1)
        builder.addReadout("Final angle", BezierAttributeID.THETA2)
        builder.addWidget(ValueTextboxWidgetDefinition("Speed", 0.85))
        builder.addWidget(ValueTextboxWidgetDefinition("Cross-track gain", 1))
        builder.addWidget(ValueTextboxWidgetDefinition("Heading gain", 5))
        return builder.build()
    
    @preset
    def goRamsete(self) -> CommandDefinition:
        from adapter.bezier_adapter import BezierAttributeID
        builder = CommandDefinitionBuilder(CommandType.BEZIER)
        builder.setName("goRamsete()")
        builder.addReadout("Initial angle", BezierAttributeID.THETA1)
        builder.addReadout("Final angle", BezierAttributeID.THETA2)
        builder.addWidget(ValueTextboxWidgetDefinition("Speed", 0.85))
        builder.addWidget(ValueTextboxWidgetDefinition("B parameter", 2))
        builder.addWidget(ValueTextboxWidgetDefinition("Zeta parameter", 0.7))
        return builder.build()
    
    @preset
    def a_wait(self) -> CommandDefinition:
        builder = CommandDefinitionBuilder(CommandType.CUSTOM)
        builder.setName("wait()")
        builder.setColor((140, 135, 130))
        builder.addWidget(ValueTextboxWidgetDefinition("Time (s)", 0.5))
        builder.disableNonblocking()
        return builder.build()
    
    @preset
    def b_task(self) -> CommandDefinition:
        builder = CommandDefinitionBuilder(CommandType.CUSTOM, isTask = True)
        builder.setName("task()")
        builder.setColor(100)
        builder.disallowInTask() # no recursion
        return builder.build()