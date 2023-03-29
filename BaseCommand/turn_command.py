from Adapters.turn_adapter import TurnAdapter

class TurnCommand:
    
    def __init__(self, adapter: TurnAdapter):
        self.adapter = adapter