from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.key_listener import KeyLambda
from BaseEntity.EntityListeners.select_listener import SelectLambda, SelectorType

from TextEditor.text_handler import TextHandler
from TextEditor.text_editor import TextEditor

from reference_frame import PointRef, Ref
from math_functions import isInsideBox2
from draw_order import DrawOrder
from dimensions import Dimensions

from enum import Enum, auto
from abc import abstractmethod
import pygame

"""
Wraps the TextEditor class into an entity
"""

class TextEditorEntity(Entity):

    def __init__(self, dimensions: Dimensions, xFunc, yFunc, width: float, height: float, readColor: tuple, writeColor: tuple, isDynamic: bool = False):

        self.textEditor = TextEditor(dimensions, xFunc, yFunc, width, height, readColor, writeColor, isDynamic)
        
        Entity.__init__(self,
            key = KeyLambda(self, FonKeyDown = self.textEditor.onKeyDown, FonKeyUp = self.textEditor.onKeyUp),
            select = SelectLambda(self, "text editor", type = SelectorType.SOLO, greedy = True, FonSelect = self.textEditor.onSelect, FonDeselect = self.textEditor.onDeselect),
            drawOrder = DrawOrder.FRONT
        )


    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        self.textEditor.isTouching(position)


    def getCenter(self) -> PointRef:
        return self.textEditor.getCenter()

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        self.textEditor.draw(screen, isActive, isHovered)