from enum import Enum
import math
from common.font_manager import DynamicFont
from data_structures.variable import Variable
from entity_base.aligned_entity_mixin import AlignedEntityMixin, VerticalAlign
from entity_base.entity import Entity
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.hover_listener import HoverLambda
from views.dropdown_view.dropdown_view_config import DropdownConfig
import pygame

"""
A view for a dropdown, where one active option out of many
is selected, and clicking on the dropdown reveals the other options
to select from.

This view works with two variables:
    - a string for the active option
    - a list of strings for all the options, including the active one

Horizontal alignment can be specified, but dropdown will always be
vertically centered on active option
"""


class DropdownMode(Enum):
    EXPANDED = 0
    COLLAPSED = 1

class DropdownView(AlignedEntityMixin, Entity):

    def __init__(self, parent: Entity,
                 activeOption: Variable[str],
                 allOptions: Variable[list[str]],
                 config: DropdownConfig
                ):
        
        # make sure active option is in list of all options
        assert(activeOption.get() in allOptions.get())

        self.activeOption = activeOption
        self.allOptions = allOptions

        self.config = config

        
        self.mode: DropdownMode = DropdownMode.COLLAPSED
        self.hoveredOption = None

        Entity.__init__(self, parent,
            hover = HoverLambda(self,
                FonHoverOn = self.onHover,
                FonHoverMouseMove = self.onHover,
                FonHoverOff = self.onHoverOff
            ),
            click = ClickLambda(self, FonLeftClick = self.onClick)
        )
        super().__init__(config.horizontalAlign, VerticalAlign.NONE)
        self.font: DynamicFont = self.fonts.getDynamicFont(config.fontID, config.fontSize)

    def getActiveOption(self) -> str:
        return self.activeOption.get()
    
    def getAllOptions(self) -> list[str]:
        return self.allOptions.get()
    
    def setOption(self, optionStr: str):
        assert optionStr in self.getAllOptions()
        self.activeOption.set(optionStr)

    # determine the draw order of options to be displayed
    # active option always goes first, rest follow sequentially
    # no duplicate of active option
    def getDisplayOptionOrder(self) -> list[str]:
        activeOption = self.getActiveOption()

        order = [activeOption]
        if self.mode == DropdownMode.EXPANDED:
            # if expanded, the rest of the options follow
            order.extend([o for o in self.getAllOptions() if o != activeOption])

        return order


    # update visually which is being hovered
    # find which option is the closest to the mouse
    def onHover(self, mouse: tuple):

        # if collapsed, then the only thing that can be hovered is the active option
        if self.mode == DropdownMode.COLLAPSED:
            return self.getActiveOption()
        
        # need to find closest option when expanded
        closestOption = None
        closestDistance = math.inf

        mx, my = mouse
        optionY = self.TOP_Y + self.optionHeight / 2
        for option in self.getDisplayOptionOrder():
            distance = abs(optionY - my)
            if distance < closestDistance:
                closestDistance = distance
                closestOption = option
            optionY += self.optionHeight

        # update hovered option and redraw
        self.hoveredOption = closestOption
        print(self.hoveredOption)
        self.recomputeEntity()

    # no more hovered option, redraw
    def onHoverOff(self):
        self.hoveredOption = None
        self.recomputeEntity()

    # If collapsed, expand
    # If expanded, update active option to clicked option and collapse
    def onClick(self, mouse: tuple):
        if self.mode == DropdownMode.COLLAPSED:
            self.mode = DropdownMode.EXPANDED
        else:
            self.setOption(self.hoveredOption)
            self.mode = DropdownMode.COLLAPSED

        # recalculate view
        self.recomputeEntity()

    # first, calculate the size of the dropdown based on text content
    # need to define this before to calculate width and height first
    # cache all these computations for defining and drawing
    def defineBefore(self) -> None:

        # font for this current screen resolution 
        self.currentFont = self.font.get()

        # get height of text
        heightTestText = "gP"
        heightTestSurface = self.currentFont.render(heightTestText, True, (0,0,0))
        charHeight = heightTestSurface.get_height()
        self.optionHeight = charHeight + self.config.verticalMargin * 2

        # find longest option and determine option width
        longestOption = ""
        for option in self.getAllOptions():
            if len(option) > len(longestOption):
                longestOption = option
        textWidthSurface = self.currentFont.render(longestOption, True, (0,0,0))
        textWidth = textWidthSurface.get_width()
        self.optionWidth = self.config.leftMargin + textWidth + self.config.rightMargin

    def defineWidth(self) -> float:
        return self.optionWidth
    
    def defineHeight(self) -> float:

        # if collapsed, only active option is shown
        if self.mode == DropdownMode.COLLAPSED:
            return self.optionHeight
        else: # if expanded, all the options are showns
            return self.optionHeight * len(self.getAllOptions())
        
    # defined to be centered on the active option
    def defineTopY(self) -> float:
        return self._py(0.5) - self.optionHeight / 2
        
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        activeOption = self.getActiveOption()

        # draw the options in that order
        y = self.TOP_Y
        for option in self.getDisplayOptionOrder():

            # determine rect for this option
            optionRect = [self.LEFT_X, y, self.optionWidth, self.optionHeight]

            # determine color for this option based on config state
            if option == activeOption:
                color = self.config.colorOn
            elif option == self.hoveredOption:
                color = self.config.colorHovered
            else:
                color = self.config.colorOff

            # draw the background rect for the option
            pygame.draw.rect(screen, color, optionRect)

            # draw the text centered in the option rect
            textY = y + self.optionHeight / 2
            textSurface = self.currentFont.render(option, True, self.config.textColor)
            screen.blit(textSurface, (self.LEFT_X + self.config.leftMargin, y))

            # increment y to next option position
            y += self.optionHeight

        # draw overall dropdown border
        pygame.draw.rect(screen, (0,0,0), self.RECT, self.config.border)