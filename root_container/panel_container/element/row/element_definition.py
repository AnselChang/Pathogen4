from enum import Enum
from root_container.panel_container.element.readout.readout_entity import ReadoutEntity
from root_container.panel_container.element.row.label_entity import LabelEntity
from root_container.panel_container.element.widget.widget_entity import WidgetEntity

from common.font_manager import FontID

from abc import ABC, abstractmethod

"""
An element is either a widget or a readout.
A list of element definitions are used to convert into a list of rows
"""

class ElementDefinition(ABC):

    def __init__(self, variableName):
        self.variableName = variableName


        self.LABEL_FONT = FontID.FONT_NORMAL
        self.LABEL_SIZE = 15

    @abstractmethod
    def makeElement(self, parent, parentCommand, pathAdapter) -> ReadoutEntity | WidgetEntity:
        return
    
    def makeLabel(self, parent) -> LabelEntity:
        LabelEntity(parent, self.LABEL_FONT, self.LABEL_SIZE, staticText = self.variableName)

    def getName(self) -> str:
        return self.variableName