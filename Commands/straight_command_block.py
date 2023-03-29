from BaseCommand.segment_command_state import SegmentCommandState
from Adapters.straight_adapter import StraightAdapter

class StraightCommandState(SegmentCommandState):
    
    def __init__(self, adapter: StraightAdapter):
        self.adapter = adapter

    def __str__(self) -> str:
        return f"Straight -> distance: {self.adapter.getDistance()}"