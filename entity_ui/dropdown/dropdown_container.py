from common.draw_order import DrawOrder
from common.font_manager import DynamicFont, FontID
from common.image_manager import ImageID
from data_structures.observer import Observable
from entity_base.container_entity import Container
from entity_base.entity import Entity
from entity_base.image.image_entity import ImageEntity
from entity_base.image.image_state import ImageState
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType
from entity_base.listeners.tick_listener import TickLambda
from entity_base.text_entity import TextAlign, TextEntity
from entity_ui.dropdown.dropdown_icon_container import DropdownIconContainer
from entity_ui.dropdown.dropdown_option_entity import DropdownOptionEntity
from entity_ui.group.linear_container import LinearContainer
from entity_ui.group.radio_group_container import RadioGroupContainer
from utility.motion_profile import MotionProfile
import pygame
from utility.pygame_functions import drawTransparentRect

"""
A dropdown is a dynamic group that stores
each option, as well as a ImageEntity that displays
the dropdown arrow icon.
A dropdown is either expanded or collapsed. The DynamicGroupContainer
expands and collapses when the dropdown is expanded/collapsed.
It takes in a list of string options at initialization.
Whenever the option is changed, it sends a notification to all subscribers.
"""

class DropdownContainer(Container, Observable):

    # In addition to setting option text, update the other options
    # to include the old selected option but exclude the new selected option
    def setSelectedText(self, selectedText: str):
        self.selectedOptionText = selectedText
        self.otherOptions = [text for text in self.optionTexts if text != selectedText]
        self.recomputePosition()
        self.notify()

    def getOptionText(self, i: int) -> str:
        if i == -1:
            return self.selectedOptionText
        else:
            return self.otherOptions[i]

    def __init__(self, parent: Entity, options: list[str], fontID: FontID, fontSize: int,
                 colorSelectedHovered, colorSelected, colorHovered, colorOff,
                 dynamicWidth: bool = False, dynamicBorderOpacity: bool = False, centered: bool = True,
                 iconScale = 0.8, verticalTextPadding = 0, textLeftOffset = 14, textRightOffset = 5, cornerRadius = 5):
        
        self.CORNER_RADIUS = cornerRadius
        self.VERTICAL_TEXT_PADDING = verticalTextPadding
        self.TEXT_LEFT_OFFSET = textLeftOffset
        self.ICON_LEFT_OFFSET = self.TEXT_LEFT_OFFSET // 2
        self.TEXT_RIGHT_OFFSET = textRightOffset
        self.ICON_SCALE = iconScale

        # width collapses to selected option width when dropdown collapsed
        self.dynamicWidth = dynamicWidth
        
        # if false, align to left
        self.centered = centered
        
        super().__init__(parent,
                         tick = TickLambda(self, FonTick = self.onTick),
                         click = ClickLambda(self, FOnMouseDownAny = self.onMouseDown),
                         drawOrder = DrawOrder.DROPDOWN
                         )
                         
        self.expanded = False
        self.dynamicBorderOpacity = dynamicBorderOpacity

        self.font = self.fonts.getDynamicFont(fontID, fontSize)

        self.options = []

        self.widthProfile = None
        self.heightProfile = None
        self.borderProfile = None

        self.optionTexts = options
        self.setSelectedText(options[0]) # recomputes position from this call

        self.currentOption = DropdownOptionEntity(self, -1, self.font, 
                                                  colorSelectedHovered, colorSelected, colorHovered, colorOff,
                                                  dynamicText = self.getSelectedOptionText)

        self.options: list[DropdownOptionEntity] = [self.currentOption]
        for i in range(len(self.otherOptions)):
            o = DropdownOptionEntity(self, i, self.font,
                                 colorSelectedHovered, colorSelected, colorHovered, colorOff,
                                 dynamicText = lambda i=i: self.getOptionText(i),
                                 visible = lambda: not self.isFullyCollapsed(),
                                 isLast = (i == len(self.otherOptions)-1)
                                 )
            self.options.append(o)
        self.recomputePosition()

        DropdownIconContainer(self.currentOption, self)

        self.heightProfile = MotionProfile(self.optionHeight, 0.4, 1)
        self.widthProfile = MotionProfile(self.getFullWidth(), 0.4)
        self.borderProfile = MotionProfile(0 if dynamicBorderOpacity else 1, 0.4)


    def onOptionClick(self, i, optionText: str):
        self.setSelectedText(optionText)

        # if it's the selected option that's clicked, toggle visibility
        # otherwise, collapse the dropdown
        if i == -1:
            self.collapse() if self.expanded else self.expand()
        else:
            self.collapse()

    def getSelectedOptionText(self) -> str:
        return self.selectedOptionText
    
    def getFullWidth(self):

        if len(self.options) == 0:
            return 0
        elif self.dynamicWidth and not self.expanded:
            textWidth = self.getOptionWithText(self.selectedOptionText).getTextWidth()
        else:
            textWidth = self.maxOptionWidth
        
        return textWidth + self._awidth(self.TEXT_LEFT_OFFSET + self.TEXT_RIGHT_OFFSET)
    
    def getFullHeight(self):
        if self.expanded:
            height = self.optionHeight * (len(self.optionTexts))
        else:
            height = self.optionHeight
        return height
        

    def updateProfiles(self, force: bool = False):
        if self.widthProfile is None:
            return
    
        self.widthProfile.setEndValue(self.getFullWidth())
        self.heightProfile.setEndValue(self.getFullHeight())
        self.borderProfile.setEndValue(1 if self.expanded else 0)

        if force:
            self.widthProfile.forceToEndValue()
            self.heightProfile.forceToEndValue()
            self.borderProfile.forceToEndValue()
        

    def expand(self):
        self.expanded = True
        self.updateProfiles()
        
    def collapse(self):
        self.expanded = False
        self.updateProfiles()
    
    def isFullyCollapsed(self) -> bool:
        return self.heightProfile.isDone() and not self.expanded

    def onTick(self):

        recompute = (not self.heightProfile.isDone() and not self.widthProfile.isDone())
        
        self.heightProfile.tick()
        self.widthProfile.tick()
        self.borderProfile.tick()

        if recompute:
            self.recomputePosition()

        width = self.widthProfile.get()
        height = self.heightProfile.get()
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

    
    # recompute option text surfaces before computing own
    def defineBefore(self):

        if len(self.options) == 0:
            self.maxOptionWidth = 0
            self.optionHeight = 0
            return

        for option in self.options:
            option.recomputePosition()

        self.maxOptionWidth = max([option.getTextWidth() for option in self.options])
        
        self.optionHeight = max([option.getTextHeight() for option in self.options])
        self.optionHeight += 2 * self._awidth(self.VERTICAL_TEXT_PADDING)

        if self.dimensions.RESIZED_THIS_FRAME:
            self.updateProfiles(True)

    def defineWidth(self):

        if self.widthProfile is None:
            return 0
        return self.widthProfile.get()
    
    def defineHeight(self):
        if self.heightProfile is None:
            return 0
        
        return self.heightProfile.get()
    
    def defineCenterX(self):
        if self.centered:
            return self._px(0.5)
        return None
    
    def defineLeftX(self):
        if not self.centered:
            return self._px(0)
        return None
    
    def defineTopY(self) -> float:
        return self._py(0.5) - self.optionHeight / 2
    
    def defineOther(self):
        self.updateProfiles()
    
    
    def draw(self, screen, a, b):
        #pygame.draw.rect(screen, (0, 0, 0), self.RECT, width = 1)
        screen.blit(self.surface, (self.LEFT_X, self.TOP_Y))

        rect = (self.LEFT_X-1, self.TOP_Y-1, self.surface.get_width()+2, self.surface.get_height()+3)
        
        borderProfileOpacity = self.borderProfile.get() if self.dynamicBorderOpacity else 1
        opacity = min(borderProfileOpacity, self.getOpacity())
        if opacity < 1:
            alpha = int(round(opacity * 255))
            drawTransparentRect(screen, *rect, (0,0,0), alpha, width = 2, radius = self.CORNER_RADIUS)
        else:
            pygame.draw.rect(screen, (0,0,0), rect, width = 2, border_radius = self.CORNER_RADIUS)

    # Higher number is drawn in the front.
    # We want to draw the lowest y coordinate in the front
    def drawOrderTiebreaker(self) -> float:
        return -self.TOP_Y
