from enum import Enum

from common.font_manager import FontID
from entity_base.aligned_entity_mixin import HorizontalAlign, VerticalAlign

"""
Specify the configuration for the dropdown view here, like colors.
"""
class DropdownConfig:

    def __init__(self,
                horizontalAlign: HorizontalAlign,
                fontID: FontID,
                fontSize: int,
                leftMargin: float = 1.0,
                rightMargin: float = .3,
                verticalMargin: float = .2,
                border: float = 1,
                radius = 5,
                textColor: tuple = (0, 0, 0),
                colorOff: tuple = (255,255,255),
                colorHovered: tuple = (200,200,200),
                colorOn: tuple = (180,180,180),
                colorOnHovered: tuple = (160, 160, 160)
            ):
        
        # alignment to parent rect
        self.horizontalAlign = horizontalAlign

        # font used for option text
        self.fontID = fontID
        self.fontSize = fontSize

        # distance from left edge to left edge of text. dropdown icon will be centered in this margin
        self.leftMargin = leftMargin * fontSize

        # distance from right edge to right edge of text
        self.rightMargin = rightMargin * fontSize

        # vertical padding below and above the text for each option
        self.verticalMargin = verticalMargin * fontSize

        # border thickness. will be hidden if wrap == FIT and collapsed
        self.border = border

        # border radius
        self.radius = radius

        # color of text
        self.textColor = textColor

        # color of the a dropdown option if not active and not hovered
        self.colorOff = colorOff

        # color of the a dropdown option if hovered
        self.colorHovered = colorHovered

        # color of the a dropdown option if active
        self.colorOn = colorOn

        # color of a dropdown if both hovered and active
        self.colorOnHovered = colorOnHovered

