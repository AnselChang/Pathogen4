from enum import Enum
from root_container.panel_container.element.readout.readout_entity import ReadoutEntity
from root_container.panel_container.element.row.element_definition import ElementDefinition

"""
A CommandDefinition holds a list of DefinedReadouts.
A defined readout holds information for position relative to command
"""

class ReadoutDefinition(ElementDefinition):

    def __init__(self, attributeID: Enum, variableName: str, px: int, py: int):
        self._attribute = attributeID

        super().__init__(variableName)

    # overriding
    def makeElement(self, parent, parentCommand, pathAdapter) -> ReadoutEntity:
        return ReadoutEntity(parent, parentCommand, pathAdapter, self)

    def getAttribute(self) -> Enum:
        return self._attribute
