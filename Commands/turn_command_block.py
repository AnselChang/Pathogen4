from BaseCommand.command_state import CommandState
from Adapters.turn_adapter import TurnAdapter

class TurnCommandState(CommandState):
    
    def __init__(self, adapter: TurnAdapter):
        self.adapter = adapter

    def __str__(self) -> str:
        return f"Turn -> Angle: {self.adapter.getEndAngle() * 180 / 3.1415}"