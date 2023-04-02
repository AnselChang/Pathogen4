from BaseEntity.EntityListeners.click_listener import ClickLambda
from BaseEntity.EntityListeners.key_listener import KeyLambda
from BaseEntity.EntityListeners.select_listener import SelectLambda, SelectorType

from Widgets.widget_entity import WidgetEntity
from Widgets.widget_definition import WidgetDefinition

from TextEditor.text_editor import TextEditor, TextEditorMode

from image_manager import ImageID
from draw_order import DrawOrder
from reference_frame import PointRef, Ref
from pygame_functions import drawSurface
import pygame


class TextboxWidgetEntity(WidgetEntity):

    def __init__(self, parentCommand, definition: 'TextboxWidgetDefinition'):

        READ_COLOR = (239, 226, 174)
        WRITE_COLOR = (174, 198, 239)

        super().__init__(parentCommand, definition,
            key = KeyLambda(self,
                            FonKeyDown = lambda key: self.getTextEditor().onKeyDown(key),
                            FonKeyUp = lambda key: self.getTextEditor().onKeyUp(key)
                            ),
            select = SelectLambda(self, "text editor", type = SelectorType.SOLO, greedyDeselect = True,
                                  FonSelect = lambda interactor: self.getTextEditor().onSelect(interactor),
                                  FonDeselect = lambda interactor: self.getTextEditor().onDeselect(interactor)
                            )
        )

        self.textEditor = TextEditor(self.getX, self.getY, definition.width, definition.height, READ_COLOR, WRITE_COLOR, self.getOpacity)

        self.onModifyDefinition()

    def getTextEditor(self):
        return self.textEditor

    def onModifyDefinition(self):
        self.textEditor.setWidth(self.definition.width)
        self.textEditor.setHeight(self.definition.height)


    # top left corner, screen ref
    def getX(self) -> float:
        return self.getPosition().screenRef[0] - self.textEditor.getWidth() / 2
    
    # top left corner, screen ref
    def getY(self) -> float:
        return self.getPosition().screenRef[1] - self.textEditor.getHeight() / 2
    
    def getValue(self) -> bool:
        return self.textEditor.getText()

    def isTouchingWidget(self, position: PointRef) -> bool:
        return self.textEditor.isTouching(position)
    
    def drawWidget(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        self.textEditor.draw(screen, isActive, isHovered, self.getOpacity())
    

class TextboxWidgetDefinition(WidgetDefinition):

    def __init__(self, name: str, px: int, py: int, width: int, height: int):
        super().__init__(name, px, py)

        self.width = width
        self.height = height

    def make(self, parentCommand) -> TextboxWidgetEntity:
        return TextboxWidgetEntity(parentCommand, self)