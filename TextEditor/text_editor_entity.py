from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.key_listener import KeyLambda
from BaseEntity.EntityListeners.select_listener import SelectLambda, SelectorType

from TextEditor.text_handler import TextHandler

from reference_frame import PointRef, Ref
from pygame_functions import drawText, FONTCODE
from math_functions import isInsideBox2
from draw_order import DrawOrder

from enum import Enum, auto
from abc import abstractmethod
import pygame

class TextEditorMode(Enum):
    READ = auto()
    WRITE = auto()


class TextEditorEntity(Entity):

    def __init__(self, width: float, height: float, readColor: tuple, writeColor: tuple):
        
        super().__init__(
            key = KeyLambda(self, FonKeyDown = self.onKeyDown, FonKeyUp = self.onKeyUp),
            select = SelectLambda(self, "text editor", type = SelectorType.SOLO, FonSelect = self.onSelect, FonDeselect = self.onDeselect),
            drawOrder = DrawOrder.FRONT
        )
        
        self.width = width
        self.height = height

        self.OUTER_X_MARGIN = 6
        self.OUTER_Y_MARGIN = 3
        self.INNER_Y_MARGIN = 0

        self.textHeight = FONTCODE.render("TEST", True, (0,0,0)).get_height()

        self.textHandler = TextHandler(self)

        self.mode: TextEditorMode = TextEditorMode.READ

        self.backgroundColor: dict[TextEditorMode, tuple] = {
            TextEditorMode.READ : readColor,
            TextEditorMode.WRITE : writeColor
        }

    @abstractmethod
    # top left corner, screen ref
    def getX(self) -> float:
        pass
    
    @abstractmethod
    # top left corner, screen ref
    def getY(self) -> float:
        pass

    def getWidth(self) -> float:
        return self.width
    
    def getHeight(self) -> float:
        return self.height

    def setWidth(self, width: float):
        self.width = width

    def setHeight(self, height: float):
        self.height = height

    def getMaxTextWidth(self) -> float:
        return self.getWidth() - self.OUTER_X_MARGIN * 2
    
    def getMaxTextLines(self) -> int:
        return (self.getHeight() - 2*self.OUTER_Y_MARGIN + self.INNER_Y_MARGIN) // (self.textHeight + self.INNER_Y_MARGIN)

    def getRect(self) -> tuple:
        return self.getX(), self.getY(), self.getWidth(), self.getHeight()

    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        return isInsideBox2(*position.screenRef, self.getX(), self.getY(), self.getWidth(), self.getHeight())
    

    def getPosition(self) -> PointRef:
        x = self.getX() + self.getWidth() / 2
        y = self.getY() + self.getHeight() / 2
        return PointRef(Ref.SCREEN, (x,y))

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        BORDER_RADIUS = 3
        rect = self.getRect()
        pygame.draw.rect(screen, self.backgroundColor[self.mode], rect, border_radius = BORDER_RADIUS)
        pygame.draw.rect(screen, (0,0,0), rect, width = 2, border_radius = BORDER_RADIUS)

        x = self.getX() + self.OUTER_X_MARGIN
        y = self.getY() + self.OUTER_Y_MARGIN
        for surface in self.textHandler.getSurfaces():
            screen.blit(surface, (x,y))
            y += self.textHeight + self.INNER_Y_MARGIN


    def onKeyDown(self, key):
        if self.mode == TextEditorMode.WRITE:
            self.textHandler.onKeyDown(key)

    def onKeyUp(self, key):
        pass

    def onSelect(self, interactor):
        self.mode = TextEditorMode.WRITE

    def onDeselect(self, interactor):
        self.mode = TextEditorMode.READ

    