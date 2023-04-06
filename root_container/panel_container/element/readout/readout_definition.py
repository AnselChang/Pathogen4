from enum import Enum
from root_container.panel_container.element.readout.readout_entity import ReadoutEntity

"""
A CommandDefinition holds a list of DefinedReadouts.
A defined readout holds information for position relative to command
"""

class ReadoutDefinition:

    def __init__(self, attribute: Enum, px: int, py: int):
        self._attribute = attribute

        # px and py are numbers (0-1) representing 0 (top/left) and 1 (top/right) for relative position
        self.px, self.py = px, py

    def make(self, parentCommand, pathAdapter) -> ReadoutEntity:
        return ReadoutEntity(parentCommand, pathAdapter, self)

    def getPositionRatio(self) -> tuple:
        return self.px, self.py
    
    def getAttribute(self) -> Enum:
        return self._attribute
