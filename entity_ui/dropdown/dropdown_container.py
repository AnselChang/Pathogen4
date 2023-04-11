from common.draw_order import DrawOrder
from common.font_manager import DynamicFont, FontID
from common.image_manager import ImageID
from entity_base.container_entity import Container
from entity_base.entity import Entity
from entity_base.image.image_entity import ImageEntity
from entity_base.image.image_state import ImageState
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType
from entity_base.listeners.tick_listener import TickLambda
from entity_base.text_entity import TextAlign, TextEntity
from entity_ui.dropdown.dropdown_option_entity import DropdownOptionEntity
from entity_ui.group.linear_container import LinearContainer
from entity_ui.group.radio_group_container import RadioGroupContainer
from utility.motion_profile import MotionProfile
import pygame

"""
A dropdown is a radio group that stores
each option, as well as a ImageEntity that displays
the dropdown arrow icon.
A dropdown is either expanded or collapsed. The DynamicGroupContainer
expands and collapses when the dropdown is expanded/collapsed, through
addingg/deleting LinearContainer entities. This class holds a list
of the LinearContainer options seperately.
It takes in a list of string options at initialization.
It also takes in pwidth.
the center of the top option is set to the center of the parent
"""

class DropdownContainer(Container):

    def __init__(self, parent: Entity, options: list[str], fontID: FontID, fontSize: int, dynamicWidth: bool = False):
        
        self.CORNER_RADIUS = 5
        self.TEXT_PADDING_RATIO = 1.1
        self.TEXT_LEFT_OFFSET = 14
        self.ICON_LEFT_OFFSET = self.TEXT_LEFT_OFFSET // 2

        self.TEXT_RIGHT_OFFSET = 5

        # width collapses to selected option width when dropdown collapsed
        self.dynamicWidth = dynamicWidth
        
        super().__init__(parent,
                         tick = TickLambda(self, FonTick = self.onTick),
                         click = ClickLambda(self, FOnMouseDownAny = self.onMouseDown),
                         drawOrder = DrawOrder.DROPDOWN
                         )
                         
        self.dynamicWidth = dynamicWidth
        self.expanded = False

        self.font = self.fonts.getDynamicFont(fontID, fontSize)

        self.optionTexts = options
        self.selectedOptionText = options[0]
        self.options = []

        self.widthProfile = None
        self.recomputePosition()

        self.currentOption = DropdownOptionEntity(self, 0, self.font, dynamicText = self.getSelectedOptionText)

        self.options: list[DropdownOptionEntity] = [self.currentOption]
        for i, optionStr in enumerate(options):
            o = DropdownOptionEntity(self, i+1, self.font,
                                 staticText = optionStr,
                                 visible = lambda: not self.isFullyCollapsed(),
                                 isLast = (i == len(options)-1)
                                 )
            self.options.append(o)
        self.recomputePosition()

        self.heightProfile = MotionProfile(self.getOptionHeight(), 0.4)
        self.widthProfile = MotionProfile(self.getFullWidth(), 0.4)

    def getOptionHeight(self) -> float:
        self.font.get()
        return self.font.getCharHeight() * self.TEXT_PADDING_RATIO
    
    def onOptionClick(self, i, optionText: str):
        self.selectedOptionText = optionText

        # if it's the selected option that's clicked, toggle visibility
        # otherwise, collapse the dropdown
        if i == 0:
            self.collapse() if self.expanded else self.expand()
        else:
            self.collapse()

    def getSelectedOptionText(self) -> str:
        return self.selectedOptionText
    
    def updateHeightProfile(self):
        if self.dynamicWidth:
            self.widthProfile.setEndValue(self.getFullWidth())

    def expand(self):
        self.expanded = True
        self.heightProfile.setEndValue(self.getOptionHeight() * len(self.optionTexts)+1)
        self.updateHeightProfile()
        
    def collapse(self):
        self.expanded = False
        self.heightProfile.setEndValue(self.getOptionHeight())

        self.updateHeightProfile()
    
    def isFullyCollapsed(self) -> bool:
        return self.heightProfile.get() == self.getOptionHeight()

    def onTick(self):

        recompute = (not self.heightProfile.isDone() and not self.widthProfile.isDone())
        
        self.heightProfile.tick()
        self.widthProfile.tick()

        if recompute:
            self.recomputePosition()

        width = self.widthProfile.get()
        height = self._aheight(self.heightProfile.get())
        self.surface = pygame.Surface((width, height-1), pygame.SRCALPHA).convert_alpha()

        for option in self.options:
            option.drawOnSurface(self.surface)

    # if clicking elsewhere on the screen, collapse the dropdown
    def onMouseDown(self, mouse: tuple):
        for option in self.options:
            if option.hover.isHovering:
                return
        self.collapse()

    def getOptionWithText(self, text):
        for option in self.options:
            if option.getText() == text:
                return option

    def getFullWidth(self):

        if len(self.options) == 0:
            return 0
        elif self.dynamicWidth and not self.expanded:
            textWidth = self.getOptionWithText(self.selectedOptionText).getTextWidth()
        else:
            widths = [option.getTextWidth() for option in self.options]
            textWidth = max(widths)
        
        return textWidth + self._awidth(self.TEXT_LEFT_OFFSET + self.TEXT_RIGHT_OFFSET)

    def defineWidth(self):
        fullWidth = self.getFullWidth()

        if self.widthProfile is not None:
            self.widthProfile.setEndValue(fullWidth)
            return self.widthProfile.get()
        return 0
    
    # not used
    def defineHeight(self):
        return self._aheight(self.getOptionHeight() * len(self.optionTexts))
    
    def defineCenterX(self):
        return self._px(0.5)
    
    def defineTopY(self) -> float:
        return self._py(0.5) - self._aheight(self.getOptionHeight() / 2)
    
    def draw(self, screen, a, b):
        #pygame.draw.rect(screen, (0, 0, 0), self.RECT, width = 1)
        screen.blit(self.surface, (self.LEFT_X, self.TOP_Y))

        rect = (self.LEFT_X-1, self.TOP_Y-1, self.surface.get_width()+2, self.surface.get_height()+3)
        pygame.draw.rect(screen, (0,0,0), rect, width = 2, border_radius = self.CORNER_RADIUS)

    # Higher number is drawn in the front.
    # We want to draw the lowest y coordinate in the front
    def drawOrderTiebreaker(self) -> float:
        return -self.CENTER_Y
