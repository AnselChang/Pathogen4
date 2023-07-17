from enum import Enum, auto

from common.font_manager import FontID
from data_structures.variable import Variable
from views.view import View

# how text is aligned horizontally within text editor box
class HorizontalAlign(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()

# how text is aligned vertically within text editor box
class VerticalAlign(Enum):
    TOP = auto()
    CENTER = auto()
    BOTTOM = auto()

"""
Data struct that represents the configuration/constraints of the text
"""
class TextConfig:

    # regular expressions for common text types
    RE_ANY = "^.*$"
    RE_INTEGER = "^[-+]?[0-9]+$"
    RE_DECIMAL = "^[+-]?((\d+(\.\d+)?)|(\.\d+))$"
    RE_ALPHANUMERIC = "^[a-zA-Z0-9]*$"
    RE_ALPHANUMERIC_SPACE = "^[a-zA-Z0-9 ]*$"

    def __init__(self,
            horizontalAlign: HorizontalAlign,
            verticalAlign: VerticalAlign,
            validDisplay: str = ".",
            validSubmit: str = ".",
            charWidth: int = 0,
            expandWidth: bool = True,
            charHeight: int = 1,
            expandHeight: int = 1,
        ):
        
        # how text is aligned within text editor box
        self.hAlign: HorizontalAlign = horizontalAlign
        self.vAlign: VerticalAlign = verticalAlign

        # regular expression specifying valid text content while editing.
        # every keystroke is validated with this, so invalid keystrokes are discarded
        self.validDisplay: str = validDisplay

        # regular expression specifying valid text content to update variable with
        # if not valid, the text editor will be set to invalid mode
        # cannot leave text editor until valid, and option to display something
        # like a red border to indicate so
        self.validSubmit: str = validSubmit

        # the width of the text editor, depending on context from expandWidth
        self.charWidth: int = charWidth

        # if true, charWidth represents the max width
        # the user can type in a line, and the textbox dynamically reshapes to
        # the width of the text.
        # if false, charWidth represents the static
        # width of the textbox, and the textbox is always set to this width
        self.expandWidth = expandWidth

        # same logic as charWidth and expandWidth
        self.charHeight = charHeight
        self.expandHeight = expandHeight 


"""
Visual characteristics of the text editor for one specific mode"""
class VisualConfigState:

    def __init__(self,
            textColor: tuple,
            backgroundColor: tuple,
            borderThickness: int = 0, # 0 if no border
            borderColor: tuple = (0,0,0)
        ):
        
        self.textColor = textColor
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
            fontID: FontID,
            fontSize: int,
            radius: int = 0, # border radius of text editor
            hOuterMargin: int = 2,
            vInnerMargin: int = 1,
            vOuterMargin: int = 2
        ):
        
        self.inactiveState = inactiveState
        self.hoveredState = hoveredState
        self.activeValidState = activeValidState
        self.activeInvalidState = activeInvalidState

        self.fontID = fontID
        self.fontSize = fontSize
        self.radius = radius
        self.hOuterMargin = hOuterMargin
        self.vInnerMargin = vInnerMargin
        self.vOuterMargin = vOuterMargin