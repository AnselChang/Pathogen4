from __future__ import annotations
from typing import TYPE_CHECKING
from entity_base.aligned_entity_mixin import AlignedEntityMixin

from entity_base.listeners.select_listener import SelectLambda, SelectorType
from views.view import View

if TYPE_CHECKING:
    from common.font_manager import DynamicFont

from data_structures.variable import Variable
from entity_base.entity import Entity
from entity_base.listeners.hover_listener import HoverLambda
from entity_base.listeners.key_listener import KeyLambda
from views.text_view.text_content import TextContent
from views.text_view.text_view_config import HorizontalAlign, TextConfig, VerticalAlign, VisualConfig
import pygame

"""
Describes a view that draws and interacts with arbitrary text. Can be constrained in text length, number of lines, content validation (through regular expressions), text alignment.

This also handles the logic for the position of the keyboard input cursor.
"""

class TextView(AlignedEntityMixin, Entity, View):

    def __init__(self,
            parent: Entity,
            variable: Variable,
            textConfig: TextConfig, # describes text formatting configuration
            visualConfig: VisualConfig, # describes how text editor looks
        ):

        super().__init__(textConfig.hAlign, textConfig.vAlign)

        self.textVariable = variable
        self.textVariable.subscribe(self, onNotify = self.onExternalVariableChange)

        self.textConfig = textConfig
        self.visualConfig = visualConfig
        
        self.content = TextContent(textConfig, variable.get())

        # on changes to content, recompute
        self.content.subscribe(self, onNotify = self.recomputeEntity)

        Entity.__init__(self, parent,
            hover = HoverLambda(self),
            select = SelectLambda(self, "text editor", type = SelectorType.SOLO, greedy = True,
                FonSelect = self.onSelect,
                FonDeselect = self.onDeselect,
                FdisableGreedySelect = lambda: not self.content.isSubmitValid() # do not release focus if not valid value
            ),
            key = KeyLambda(self,
                FonKeyDown = lambda key: self.onKeyDown(key)
            )
        )

        self.font: DynamicFont = self.fonts.getDynamicFont(self.visualConfig.fontID, self.visualConfig.fontSize)

    
    # get the value the text editor is derived from
    def getValue(self) -> str:
        return self.textVariable.get()
    
    # set a new value for the variable
    def setValue(self, value: str):
        self.textVariable.set(value)

    # when something else changes the variable, update content
    def onExternalVariableChange(self):
        self.content.setContentFromString(self.getValue())

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

        # convert to current resolution
        self.H_OUTER = self._awidth(self.visualConfig.hOuterMargin)
        self.V_INNER = self._aheight(self.visualConfig.vInnerMargin)
        self.V_OUTER = self._aheight(self.visualConfig.vOuterMargin)

        # font for this current screen resolution 
        self.currentFont = self.font.get()

        # get width of text
        widthTestText = "-" * self.content.getDisplayMaxCharWidth()
        widthTestSurface = self.currentFont.render(widthTestText, True, (0,0,0))
        textWidth = widthTestSurface.get_width()
        self.fullWidth = textWidth + self.H_OUTER * 2

        self.charWidth = self.currentFont.render("g", True, (0,0,0)).get_width()

        # get height of text
        heightTestText = "gP"
        heightTestSurface = self.currentFont.render(heightTestText, True, (0,0,0))
        self.charHeight = heightTestSurface.get_height()

        numLines = self.content.getDisplayCharHeight()
        self.fullHeight = self.V_OUTER * 2
        self.fullHeight += numLines * self.charHeight
        self.fullHeight += (numLines - 1) * self.V_INNER

    # return cached width computed in defineBefore
    def defineWidth(self) -> float:
        return self.fullWidth
    
    # return cached height computed in defineBefore
    def defineHeight(self) -> float:
        return self.fullHeight
        
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
        x = self.LEFT_X + self.H_OUTER
        y = self.TOP_Y + self.V_OUTER
        for line in self.content.getDisplayableContent():
            textSurface = self.currentFont.render(line, True, state.textColor)
            screen.blit(textSurface, (x,y))
            y += self.charHeight + self.V_INNER

        # draw cursor if active
        if isActive:
            cursorX = self.LEFT_X + self.H_OUTER + self.charWidth * self.content.getDisplayCursorX()
            cursorY = self.TOP_Y + self.V_OUTER - self.V_INNER
            cursorY += self.content.getDisplayCursorY() * (self.charHeight + self.V_INNER)
            pygame.draw.line(screen, (0,0,0), (cursorX, cursorY), (cursorX, cursorY + self.charHeight), width = 1)