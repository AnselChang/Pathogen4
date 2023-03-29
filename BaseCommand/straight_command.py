from BaseCommand.segment_command import SegmentCommand
from Adapters.straight_adapter import StraightAdapter

class StraightCommand(SegmentCommand):
    
    def __init__(self, adapter: StraightAdapter):
        self.adapter = adapter

    def __str__(self) -> str:
        return f"Straight -> distance: {self.adapter.getDistance()}"