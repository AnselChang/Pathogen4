from Adapters.path_adapter import PathAdapter
from CommandCreation.command_type import CommandType

class StraightAdapter(PathAdapter):

    def __init__(self):

        dict = {
                "x1" : -1,
                "y1" : -1,
                "x2" : -1,
                "y2" : -1,
                "distance" : -1
            }

        super().__init__(CommandType.STRAIGHT, dict)
    
    def set(self, startPosition: tuple = None, endPosition: tuple = None, distance: float = None):

        if startPosition is not None:
            self._dict["x1"], self._dict["y1"] = startPosition
        if endPosition is not None:
            self._dict["x2"], self._dict["y2"] = endPosition
        if distance is not None:
            self._dict["distance"] = distance