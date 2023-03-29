from Adapters.adapter import Adapter

class TurnAdapter(Adapter):

    def __init__(self):
        pass
    
    def set(self, startAngle: float, endAngle: float):
        self._startAngle = startAngle
        self._endAngle = endAngle

    def getStartAngle(self) -> float:
        return self._startAngle

    def getEndAngle(self) -> float:
        return self._endAngle

    