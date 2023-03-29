from Adapters.turn_adapter import TurnAdapter

class TurnCommand:
    
    def __init__(self, adapter: TurnAdapter):
        self.adapter = adapter

    def __str__(self) -> str:
        return f"Turn -> Angle: {self.adapter.getEndAngle() * 180 / 3.1415}"