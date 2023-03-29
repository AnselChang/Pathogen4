from Adapters.adapter import SegmentAdapter

class StraightAdapter(SegmentAdapter):

    def __init__(self):
        super().__init__(SegmentAdapter.ID.STRAIGHT)
    
    def set(self, startPosition: tuple, endPosition: tuple, distance: float):
        self._startPosition = startPosition
        self._endPosition = endPosition
        self._distance = distance

    def getStartPosition(self) -> tuple:
        return self._startPosition

    def getEndPosition(self) -> tuple:
        return self._endPosition

    def getDistance(self) -> float:
        return self._distance
