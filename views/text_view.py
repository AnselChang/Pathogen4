from enum import Enum, auto

# how text is aligned within text editor box
class TextAlignment(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()

"""
Data struct that represents the configuration/constraints of the text
"""
class TextConfig:
    def __init__(self,
        align: TextAlignment, # how text is aligned within text editor box
        validDisplay: str = ".", # re specifying valid text content while editing.
        #,every keystroke is validated with this, so invalid keystrokes are discarded
        validSubmit: str = ".", # re specifying what valid strings can be submitted to update
        # model. cannot exit text editor whild invalid, and supports a visual 
        # indicator like a red box to tell the user this
        charWidth: int = 0, # the starting width of the text editor.
        expandWidth: bool = True, # if true, charWidth represents the max width
        # the user can type in a line, and the textbox dynamically reshapes to
        # the width of the text. if false, charWidth represents the static
        # width of the textbox, and the textbox is always set to this width
        charHeight: int = 1,
        expandHeight: int = 1, # same logic as charWidth and expandWidth 
        )
        
        self.align = align,
        self.validDisplay = validDisplay,
        self.validSubmit = validSubmit,
        self.charWidth = charWidth,
        self.expandWidth = expandWidth,
        self.charHeight = charHeight,
        self.expandHeight = expandHeight 


"""
Visual characteristics of the text editor for one specific mode"""
class VisualConfigState:

    def __init__(self,
        backgroundColor: tuple,
        borderThickness: int = 0, # 0 if no border
        borderColor: tuple = (0,0,0)
        )
        
        self.backgroundColor = backgroundColor
        self.borderThickness = borderThickness
        self.borderColor = borderColor

"""
Data struct that specifes visual characteristics of the text editor,
like color and border radius. Stores four VisualConfigStates based on the mode: INACTIVE, HOVERED, ACTIVE (invalid/valid)
"""

class VisualConfig:

    def __init__(self,
        inactiveState: VisualConfigState,
        hoveredState: VisualConfigState,
        activeValidState: VisualConfigState,
        activeInvalidState: VisualConfigState,
        font,
        fontSize: int,
        radius: int = 0, # border radius of text editor
        hInnerMargin: int = 1,
        hOuterMargin: int = 2,
        vInnerMargin: int = 1,
        vOuterMargin: int = 2
        )
        
        self.inactiveState = inactiveState
        self.hoveredState = hoveredState
        self.activeValidState = activeHoveredState,
        self.activeInvalidState = activeInvalidState
        

 """
Describes a view that draws and interacts with arbitrary text. Can be constrained in text length, number of lines, content validation (through regular expressions), text alignment.

This also handles the logic for the position of the keyboard input cursor.
"""

class TextView(View):

    def __init__(self, variable: Variable,
    textConfig: TextConfig, # describes text formatting configuration
    visualConfig: VisualConfig, # describes how text editor looks
    ):

        super().__init__(variable)
        self.textConfig = textConfig
        self.visualConfig = visualConfig
        
        # the displayed text. This is usually synced
        # with the variable. However, while editing,
        # the displayed text updates while the variable
        # stays the same. Only when the user submits
        # the text by exiting out of the text box does
        # variable update. This reduces the frequency
        # the model must be updated.
        self.displayedText = variable.getValue()
        
        
    # called when the variable is changed externally
    def onExternalValueChange(self):
        pass