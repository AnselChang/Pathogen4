from enum import Enum

from common.font_manager import FontID

"""
Specify the configuration for the dropdown view here, like colors.
"""
class DropdownConfig:

    def __init__(self,
                fontID: FontID,
                fontSize: int,
                leftMargin: float = 0,
                rightMargin: float = 0,
                verticalMargin: float = 0,
                border: float = 1,
                colorOff: tuple = (255,255,255),
                colorHovered: tuple = (245,245,245),
                colorOn: tuple = (180,180,180),
            ):

        # font used for option text
        self.fontID = fontID
        self.fontSize = fontSize

        # distance from left edge to left edge of text. dropdown icon will be centered in this margin
        self.leftMargin = leftMargin

        # distance from right edge to right edge of text
        self.rightMargin = rightMargin

        # vertical padding below and above the text for each option
        self.verticalMargin = verticalMargin

        # border thickness. will be hidden if wrap == FIT and collapsed
        self.border = border

        # color of the a dropdown option if not active and not hovered
        self.colorOff = colorOff

        # color of the a dropdown option if hovered
        self.colorHovered = colorHovered

        # color of the a dropdown option if active
        self.colorOn = colorOn



