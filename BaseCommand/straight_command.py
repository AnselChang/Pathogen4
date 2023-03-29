from BaseCommand.segment_command import SegmentCommand
from Adapters.straight_adapter import StraightAdapter

class StraightCommand(SegmentCommand):
    
    def __init__(self, adapter: StraightAdapter):
        self.adapter = adapter