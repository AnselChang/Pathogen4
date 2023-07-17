"""
Handles drawing the text and editor box onto a surface
"""
from data_structures.observer import Observer
from views.text_view.text_content import TextContent
from views.text_view.text_view_config import VisualConfig


class TextSurface(Observer):

    def __init__(self, visualConfig: VisualConfig, content: TextContent):

        super().__init__()

        self.visualConfig = visualConfig
        self.content = content

        self.content.subscribe(self, onNotify = self.updateSurface)
        self.updateSurface()

    # based on the content, update the surface
    def updateSurface(self):
        
        content = self.content.getDisplayableContent()
        cursorX, cursorY = self.content.getCursorPosition()
