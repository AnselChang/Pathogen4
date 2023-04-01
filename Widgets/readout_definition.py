from enum import Enum

"""
A CommandDefinition holds a list of DefinedReadouts.
A defined readout holds information for position relative to command
"""

class ReadoutDefinition:

    def __init__(self, attribute: Enum, px: int, py: int):
        self._attribute = attribute

        # px and py are numbers (0-1) representing 0 (top/left) and 1 (top/right) for relative position
        self._px, self._py = px, py

    def getPositionRatio(self) -> tuple:
        return self._px, self._py
    
    def getAttribute(self) -> Enum:
        return self._attribute