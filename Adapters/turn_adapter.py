from Adapters.path_adapter import PathAdapter
from CommandCreation.command_type import CommandType

class TurnAdapter(PathAdapter):

    def __init__(self):

        dict = {
                "theta1" : -1,
                "theta2" : -1,
            }

        super().__init__(CommandType.TURN, dict)
    
    def set(self, startAngle: float = None, endAngle: float = None):

        if startAngle is not None:
            self._dict["theta1"] = startAngle
        if endAngle is not None:
            self._dict["theta2"] = endAngle