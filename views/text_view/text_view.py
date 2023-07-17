from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.listeners.select_listener import SelectLambda, SelectorType

if TYPE_CHECKING:
    from common.font_manager import DynamicFont

from data_structures.variable import Variable
from entity_base.entity import Entity
from entity_base.listeners.hover_listener import HoverLambda
from entity_base.listeners.key_listener import KeyLambda
from views.text_view.text_content import TextContent
from views.text_view.text_view_config import HorizontalAlign, TextConfig, VerticalAlign, VisualConfig
from views.single_variable_view import SingleVariableView
import pygame

"""
Describes a view that draws and interacts with arbitrary text. Can be constrained in text length, number of lines, content validation (through regular expressions), text alignment.

This also handles the logic for the position of the keyboard input cursor.
"""

class TextView(Entity, SingleVariableView):

    def __init__(self,
            parent: Entity,
            variable: Variable,
            textConfig: TextConfig, # describes text formatting configuration
            visualConfig: VisualConfig, # describes how text editor looks
        ):

        SingleVariableView.__init__(self, variable)
        self.textConfig = textConfig
        self.visualConfig = visualConfig
        
        self.content = TextContent(textConfig, variable.get())

        # on changes to content, recompute
        self.content.subscribe(self, onNotify = self.recomputeEntity)

        super().__init__(parent,
            hover = HoverLambda(self),
            select = SelectLambda(self, "text editor", type = SelectorType.SOLO, greedy = True,
                FonSelect = self.onSelect,
                FonDeselect = self.onDeselect
            ),
            key = KeyLambda(self,
                FonKeyDown = lambda key: self.onKeyDown(key)
            )
        )

        self.font: DynamicFont = self.fonts.getDynamicFont(self.visualConfig.fontID, self.visualConfig.fontSize)

    
    # called when the variable is changed externally
    def onExternalValueChange(self):
        pass

    def onSelect(self, interactor):
        print("selected text editor")

    def onDeselect(self, interactor):
        print("deselected text editor")

    # if editing text view, process keystroke
    def onKeyDown(self, key):
        if self.select.isSelected:
            self.content.onKeystroke(key)

    # first, calculate the size of the text box based on text content
    # need to define this before to calculate width and height first
    # cache all these computations for defining and drawing
    def defineBefore(self) -> None:

        # font for this current screen resolution 
        self.currentFont = self.font.get()

        # get width of text
        widthTestText = "-" * self.content.getDisplayMaxCharWidth()
        widthTestSurface = self.currentFont.render(widthTestText, True, (0,0,0))
        textWidth = widthTestSurface.get_width()
        self.fullWidth = textWidth + self.visualConfig.hOuterMargin * 2

        self.charWidth = self.currentFont.render("g", True, (0,0,0)).get_width()

        # get height of text
        heightTestText = "gP"
        heightTestSurface = self.currentFont.render(heightTestText, True, (0,0,0))
        self.charHeight = heightTestSurface.get_height()

        numLines = self.content.getDisplayCharHeight()
        self.fullHeight = self.visualConfig.vOuterMargin * 2
        self.fullHeight += numLines * self.charHeight
        self.fullHeight += (numLines - 1) * self.visualConfig.vInnerMargin

    # return cached width computed in defineBefore
    def defineWidth(self) -> float:
        return self.fullWidth
    
    # return cached height computed in defineBefore
    def defineHeight(self) -> float:
        return self.fullHeight
    
    # align text editor horizontally based on config
    def defineLeftX(self) -> float:
        if self.textConfig.hAlign == HorizontalAlign.LEFT:
            return self._px(0)
        else:
            return None
    def defineCenterX(self) -> float:
        if self.textConfig.hAlign == HorizontalAlign.CENTER:
            return self._px(0.5)   
    def defineRightX(self) -> float:
        if self.textConfig.hAlign == HorizontalAlign.RIGHT:
            return self._px(1)
        
    # align text editor vertically based on config
    def defineTopY(self) -> float:
        if self.textConfig.vAlign == VerticalAlign.TOP:
            return self._py(0)
        else:
            return None
    def defineCenterY(self) -> float:
        if self.textConfig.vAlign == VerticalAlign.CENTER:
            return self._py(0.5)
        else:
            return None    
    def defineBottomY(self) -> float:
        if self.textConfig.vAlign == VerticalAlign.BOTTOM:
            return self._py(1)
        else:
            return None
        
    # draw the text editor
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        # determine which visual state to draw
        if isActive:
            if self.content.isSubmitValid():
                state = self.visualConfig.activeValidState
            else:
                state = self.visualConfig.activeInvalidState
        elif self.hover.isHovering:
            state = self.visualConfig.hoveredState
        else:
            state = self.visualConfig.inactiveState

        # draw background
        r = self.visualConfig.radius
        pygame.draw.rect(screen, state.backgroundColor, self.RECT, border_radius = r)

        # draw border if exists
        if state.borderThickness > 0:
            pygame.draw.rect(screen, state.borderColor, self.RECT, width = state.borderThickness, border_radius = r)

        # draw text
        x = self.LEFT_X + self.visualConfig.hOuterMargin
        y = self.TOP_Y + self.visualConfig.vOuterMargin
        for line in self.content.getDisplayableContent():
            textSurface = self.currentFont.render(line, True, state.textColor)
            screen.blit(textSurface, (x,y))
            y += self.charHeight + self.visualConfig.vInnerMargin

        # draw cursor if active
        if isActive:
            cursorX = self.LEFT_X + self.visualConfig.hOuterMargin + self.charWidth * self.content.getDisplayCursorX()
            cursorY = self.TOP_Y + self.visualConfig.vOuterMargin - self.visualConfig.vInnerMargin
            cursorY +=  self.content.getDisplayCursorY() * (self.charHeight + self.visualConfig.vInnerMargin)
            pygame.draw.line(screen, (0,0,0), (cursorX, cursorY), (cursorX, cursorY + self.charHeight), width = 1)