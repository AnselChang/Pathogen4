#from pygame_functions import FONT15
from common.font_manager import DynamicFont
from common.dimensions import Dimensions
import pygame
from abc import ABC, abstractmethod

_tooltipFont: DynamicFont = None
def setTooltipFont(tooltipFont: DynamicFont):
    global _tooltipFont
    _tooltipFont = tooltipFont

"""
Classes that have a self.tooltip instance variable storing a Tooltip object will have a tooltip displayed
when the mouse is hovering over the object
"""

BACKGROUND_COLOR = [220, 220, 200]
TEXT_COLOR = [0,0,0]

class Tooltip:

    def __init__(self, messages: str | list[str]):

        self.font = _tooltipFont
        self.font.subscribe(onNotify = self.recalculateTooltipSurface)
        
        if type(messages) == str:
            messages = [messages]

        self.messages = messages
        self.recalculateTooltipSurface()

    # Return a tooltip surface based on message parameter(s). Each parameter is a new line
    def recalculateTooltipSurface(self):

        # generate temporary text surfaces for each line to figure out width and height of text
        texts = [self.font.get().render(message, True, TEXT_COLOR) for message in self.messages]

        OUTSIDE_MARGIN_VERTICAL = 3 # margin between text and tooltip surface
        OUTSIDE_MARGIN_HORIZONTAL = 6
        INSIDE_MARGIN = 1 # margin between lines of text
        BORDER_RADIUS = 6

        textWidth = max([text.get_width() for text in texts])
        textHeight = texts[0].get_height()

        # Calculate tooltip dimensions based on # of lines of text, text width/height, and margins
        tooltipWidth = textWidth + 2 * OUTSIDE_MARGIN_HORIZONTAL
        tooltipHeight = len(texts) * textHeight + (len(texts)-1) * INSIDE_MARGIN + 2 * OUTSIDE_MARGIN_VERTICAL

        # Create the background surfaces based on the calculated tooltip dimensions
        tooltipSurface = pygame.Surface([tooltipWidth, tooltipHeight], pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(tooltipSurface, BACKGROUND_COLOR, [0, 0, tooltipWidth, tooltipHeight], border_radius = BORDER_RADIUS)
        
        # draw black border
        pygame.draw.rect(tooltipSurface, (0,0,0), [0, 0, tooltipWidth, tooltipHeight], width = 2, border_radius = BORDER_RADIUS)
        
        # Draw the text line by line onto the surface
        y = OUTSIDE_MARGIN_VERTICAL
        for text in texts:
            tooltipSurface.blit(text, [OUTSIDE_MARGIN_HORIZONTAL, y])
            y += INSIDE_MARGIN + textHeight

        self.tooltip = tooltipSurface

    # Draw the tooltip approximately where the mouse position is
    def draw(self, screen: pygame.Surface, mousePosition: tuple, dimensions: Dimensions):

        Y_SEPARATION_FROM_MOUSE: int = -45
        
        # Calculate tooltip position, preventing tooltip from going above or left of screen
        x = max(0, int(mousePosition[0] - self.tooltip.get_width()/2))
        y = max(0, int(mousePosition[1] - self.tooltip.get_height() - Y_SEPARATION_FROM_MOUSE))

        # prevent tooltip from spilling over right edge of screen
        x = min(x, dimensions.FIELD_WIDTH + dimensions.PANEL_WIDTH - self.tooltip.get_width())

        # if y is spilling in the bottom, make tooltip above mouse instead
        if y + self.tooltip.get_height() > dimensions.SCREEN_HEIGHT:
            y = int(mousePosition[1] - self.tooltip.get_height() - 10)

        screen.blit(self.tooltip, (x,y))

# Entities that have tooltips should implement this
class TooltipOwner(ABC):

    @abstractmethod
    def getTooltip(self) -> Tooltip | None:
        pass

    def drawTooltip(self, screen: pygame.Surface, mousePosition: tuple, dimensions: Dimensions):
        tooltip = self.getTooltip()
        if tooltip is not None:
            tooltip.draw(screen, mousePosition, dimensions)