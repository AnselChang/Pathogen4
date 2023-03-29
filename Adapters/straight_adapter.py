from Adapters.adapter import Adapter
from Commands.command_type import CommandType

class StraightAdapter(Adapter):

    def __init__(self):
        super().__init__(CommandType.STRAIGHT)
        self.set((-1,-1), (-1,-1), -1)
    
    def set(self, startPosition: tuple, endPosition: tuple, distance: float):

        super().setDict(
            {
                "x1" : startPosition[0],
                "y1" : startPosition[1],
                "x2" : endPosition[0],
                "y2" : endPosition[1],
                "distance" : distance
            }
        )