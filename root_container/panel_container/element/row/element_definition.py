from enum import Enum
from root_container.panel_container.element.readout.readout_entity import ReadoutEntity
from root_container.panel_container.element.widget.widget_entity import WidgetEntity
from entity_base.text_entity import TextEntity
from common.font_manager import FontID

from abc import ABC, abstractmethod

"""
An element is either a widget or a readout.
A list of element definitions are used to convert into a list of rows
"""

class ElementDefinition(ABC):

    def __init__(self, variableName: str, px: int, py: int):
        self.variableName = variableName

        # px and py are numbers (0-1) representing 0 (top/left) and 1 (top/right) for relative position
        self.px, self.py = px, py

        self.LABEL_FONT = FontID.FONT_NORMAL
        self.LABEL_SIZE = 15

    @abstractmethod
    def makeElement(self, parent, parentCommand, pathAdapter) -> ReadoutEntity | WidgetEntity:
        return
    
    def makeLabel(self, parent) -> TextEntity:
        TextEntity(parent, self.LABEL_FONT, self.LABEL_SIZE, staticText = self.variableName)

    def getPositionRatio(self) -> tuple:
        return self.px, self.py
    
    def getName(self) -> str:
        return self.variableName