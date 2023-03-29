from Adapters.adapter import Adapter
from Commands.command_type import CommandType

class TurnAdapter(Adapter):

    def __init__(self):
        super().__init__(CommandType.TURN)
        self.set(-1, -1)

    def set(self, startAngle: float, endAngle: float):

        super().setDict(
            {
                "theta1" : startAngle,
                "theta2" : endAngle
            }
        )