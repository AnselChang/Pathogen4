
from data_structures.variable import Variable
from entity_base.entity import Entity
from entity_base.listeners.hover_listener import HoverLambda
from views.text_view.text_content import TextContent
from views.text_view.text_surface import TextSurface
from views.text_view.text_view_config import TextConfig, VisualConfig
from views.view import View

"""
Describes a view that draws and interacts with arbitrary text. Can be constrained in text length, number of lines, content validation (through regular expressions), text alignment.

This also handles the logic for the position of the keyboard input cursor.
"""

class TextView(Entity, View):

    def __init__(self,
            parent: Entity,
            variable: Variable,
            textConfig: TextConfig, # describes text formatting configuration
            visualConfig: VisualConfig, # describes how text editor looks
        ):

        View.__init__(self, variable)
        self.textConfig = textConfig
        self.visualConfig = visualConfig
        
        self.content = TextContent(textConfig, variable.get())
        self.surface = TextSurface(visualConfig, self.content)

        super.__init__(parent,
            hover = HoverLambda(self,
                FonHoverOn = self.surface.updateSurface,
                FonHoverOff = self.surface.updateSurface,
            )
        )

       
        
        
    # called when the variable is changed externally
    def onExternalValueChange(self):
        pass