from enum import Enum, auto

"""
A mixin to specify the location of the entity relative to some
vertical and horizontal alignment of parent rect
"""


# how entity is aligned horizontally within parent rect
class HorizontalAlign(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()
    NONE = auto()

# how text is aligned vertically within parent rect
class VerticalAlign(Enum):
    TOP = auto()
    CENTER = auto()
    BOTTOM = auto()
    NONE = auto()

class AlignedEntityMixin:

    def __init__(self, horizontalAlign: HorizontalAlign, verticalAlign: VerticalAlign):
        self.hAlign  = horizontalAlign
        self.vAlign = verticalAlign
    
    # align entity horizontally based on parent rect
    def defineLeftX(self) -> float:
        if self.hAlign == HorizontalAlign.LEFT:
            return self._px(0)
        else:
            return None
    def defineCenterX(self) -> float:
        if self.hAlign == HorizontalAlign.CENTER:
            return self._px(0.5)   
    def defineRightX(self) -> float:
        if self.hAlign == HorizontalAlign.RIGHT:
            return self._px(1)
        
    # align entity vertically based on parent rect
    def defineTopY(self) -> float:
        if self.vAlign == VerticalAlign.TOP:
            return self._py(0)
        else:
            return None
    def defineCenterY(self) -> float:
        if self.vAlign == VerticalAlign.CENTER:
            return self._py(0.5)
        else:
            return None    
    def defineBottomY(self) -> float:
        if self.vAlign == VerticalAlign.BOTTOM:
            return self._py(1)
        else:
            return None