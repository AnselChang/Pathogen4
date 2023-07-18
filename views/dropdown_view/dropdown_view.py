from enum import Enum
import math
from common.font_manager import DynamicFont
from common.image_manager import ImageID
from data_structures.variable import Variable
from entity_base.aligned_entity_mixin import AlignedEntityMixin, VerticalAlign
from entity_base.entity import Entity
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.hover_listener import HoverLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType
from entity_base.listeners.tick_listener import TickLambda
from utility.math_functions import isInsideBox2
from utility.motion_profile import MotionProfile
from utility.pygame_functions import scaleImageToRect
from views.dropdown_view.dropdown_view_config import DropdownConfig
import pygame
from views.view import View

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

class DropdownView(AlignedEntityMixin, Entity, View):

    def __init__(self, parent: Entity,
                 activeOption: Variable[str],
                 allOptions: Variable[list[str]],
                 config: DropdownConfig
                ):
        
        # make sure active option is in list of all options
        assert(activeOption.get() in allOptions.get())

        # on external variable changes, recompute
        self.activeOption = activeOption
        self.activeOption.subscribe(self, onNotify = self.recomputeEntity)

        self.allOptions = allOptions
        self.allOptions.subscribe(self, onNotify = self.onOptionListChange)

        self.config = config

        
        self.mode: DropdownMode = DropdownMode.COLLAPSED
        self.hoveredOption = None

        # in charge of collapse/expand height animation
        self.mp = MotionProfile(0, 0.5)

        Entity.__init__(self, parent,
            hover = HoverLambda(self,
                FonHoverOn = self.onHover,
                FonHoverMouseMove = self.onHover,
                FonHoverOff = self.onHoverOff
            ),
            click = ClickLambda(self, FonLeftClick = self.onClick),
            select = SelectLambda(self, "dropdown", type = SelectorType.SOLO, greedy = True,
                #FonSelect = self.onClick,
                FonDeselect = lambda interactor: self.collapseDropdown(),
            ),
            tick = TickLambda(self, FonTickStart = self.onTick),
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
    
    # when the variable for all the options changes
    # if active option is not valid anymore, set to first option
    def onOptionListChange(self):
        if self.getActiveOption() not in self.getAllOptions():
            self.activeOption.set(self.getAllOptions()[0])
        
        self.recomputeEntity()

    # update height animation, and redraw if change
    def onTick(self):

        self.mp.tick()

        if self.mp.wasChange():
            self.recomputeEntity()

    # update visually which is being hovered
    # find which option is the closest to the mouse
    def onHover(self, mouse: tuple):

        # if mouse is not inside dropdown,it is not hovering over any option
        if not isInsideBox2(*mouse, *self.RECT):
            self.hoveredOption = None

        # if collapsed, then the only thing that can be hovered is the active option
        elif self.mode == DropdownMode.COLLAPSED:
            self.hoveredOption = self.getActiveOption()
        
        else:
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

        self.recomputeEntity()

    # no more hovered option, redraw
    def onHoverOff(self):
        self.hoveredOption = None
        self.recomputeEntity()

    # If collapsed, expand
    # If expanded, update active option to clicked option and collapse
    def onClick(self, mouse: tuple):
        if self.mode == DropdownMode.COLLAPSED:
            self.expandDropdown()
        else:
            if self.hoveredOption is not None:
                self.setOption(self.hoveredOption)
                # release greedy focus
                self.interactor.releaseGreedyEntity()
            self.collapseDropdown()

    # Set the motion profile to expand dropdown, and redraw
    def expandDropdown(self):
        self.mp.setEndValue(1)
        self.mode = DropdownMode.EXPANDED
        self.recomputeEntity()

    # Set the motion profile to collapse dropdown, and redraw
    def collapseDropdown(self):
        self.mp.setEndValue(0)
        self.mode = DropdownMode.COLLAPSED
        self.recomputeEntity()

    # first, calculate the size of the dropdown based on text content
    # need to define this before to calculate width and height first
    # cache all these computations for defining and drawing
    def defineBefore(self) -> None:

        # convert to current resolution
        self.VERTICAL_MARGIN = self._aheight(self.config.verticalMargin)
        self.LEFT_MARGIN = self._awidth(self.config.leftMargin)
        self.RIGHT_MARGIN = self._aheight(self.config.rightMargin)

        # font for this current screen resolution 
        self.currentFont = self.font.get()

        # get height of text
        heightTestText = "gP"
        heightTestSurface = self.currentFont.render(heightTestText, True, (0,0,0))
        charHeight = heightTestSurface.get_height()
        self.optionHeight = charHeight + self.VERTICAL_MARGIN * 2

        # find longest option and determine option width
        longestOption = ""
        for option in self.getAllOptions():
            if len(option) > len(longestOption):
                longestOption = option
        textWidthSurface = self.currentFont.render(longestOption, True, (0,0,0))
        textWidth = textWidthSurface.get_width()
        self.optionWidth = self.LEFT_MARGIN + textWidth + self.RIGHT_MARGIN

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
    
    def defineAfter(self) -> None:
        self.defineSurface()
    
    # cache the dropdown surface to be blit onto the screen
    def defineSurface(self):

        # height is somewhere between collapsed and expanded height, based on animation
        surfaceHeight = self.optionHeight + self.optionHeight * (len(self.getAllOptions())-1) * self.mp.get()
        self.surface = pygame.Surface([self.WIDTH, surfaceHeight]).convert_alpha()

        activeOption = self.getActiveOption()

        # border radius
        r = self.config.radius

        # draw the options in that order
        y = 0
        order = self.getDisplayOptionOrder()
        for option in order:

            # determine rect for this option
            optionRect = [0, y, self.optionWidth, self.optionHeight+1]

            # determine color for this option based on config state
            isHovered = option == self.hoveredOption
            if option == activeOption:
                color = self.config.colorOnHovered if isHovered else self.config.colorOn
            elif isHovered:
                color = self.config.colorHovered
            else:
                color = self.config.colorOff

            # draw the background rect for the option, with corresponding border radius if top or bottom
            if len(order) == 1:
                pygame.draw.rect(self.surface, color, optionRect, border_radius = r)
            elif option == order[0]:
               pygame.draw.rect(self.surface, color, optionRect, border_top_left_radius = r, border_top_right_radius = r)
            elif option == order[-1]:
                pygame.draw.rect(self.surface, color, optionRect, border_bottom_left_radius = r, border_bottom_right_radius = r)
            else:
                pygame.draw.rect(self.surface, color, optionRect)

            # draw the text centered in the option rect
            textY = y + self.VERTICAL_MARGIN
            textSurface = self.currentFont.render(option, True, self.config.textColor)
            self.surface.blit(textSurface, (self.LEFT_MARGIN, textY))

            # increment y to next option position
            y += self.optionHeight

        # draw dropdown ui icon
        PERCENT = 1
        size = self.LEFT_MARGIN * PERCENT
        icon = scaleImageToRect(self.images.get(ImageID.DROPDOWN_ICON), size, size)
        x = (self.LEFT_MARGIN - size) / 2 + 1
        y = (self.optionHeight - size) / 2
        self.surface.blit(icon, [x,y])

        # draw overall dropdown border
        pygame.draw.rect(self.surface, (0,0,0), [0, 0, self.WIDTH, surfaceHeight], self.config.border, border_radius = r)

        
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        screen.blit(self.surface, [self.LEFT_X, self.TOP_Y])