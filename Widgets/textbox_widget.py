from BaseEntity.EntityListeners.click_listener import ClickLambda
from BaseEntity.EntityListeners.key_listener import KeyLambda
from BaseEntity.EntityListeners.select_listener import SelectLambda, SelectorType

from Widgets.widget_entity import WidgetEntity
from Widgets.widget_definition import WidgetDefinition

from TextEditor.text_editor import TextEditor, TextEditorMode

from Observers.observer import Observer

from image_manager import ImageID
from draw_order import DrawOrder
from reference_frame import PointRef, Ref
from pygame_functions import drawSurface
import pygame


class TextboxWidgetEntity(WidgetEntity):

    def __init__(self, parentCommand, definition: 'TextboxWidgetDefinition'):

        READ_COLOR = (239, 226, 174)
        WRITE_COLOR = (174, 198, 239)

        width = lambda: parentCommand.dimensions.PANEL_WIDTH * definition.pwidth

        self.textEditor = TextEditor(
            self.getX, self.getY, width, definition.rows,
            READ_COLOR, WRITE_COLOR,
            isDynamic = definition.isDynamic,
            isNumOnly = definition.isNumOnly,
            isCentered = definition.isCentered
        )

        # Sends notification when text height changes
        commandStretchObserver = Observer(onNotify = self.onCommandStretch)
        self.textEditor.addObserver(commandStretchObserver)

        super().__init__(parentCommand, definition,
            key = KeyLambda(self,
                            FonKeyDown = self.textEditor.onKeyDown,
                            FonKeyUp = self.textEditor.onKeyUp
                            ),
            select = SelectLambda(self, "text editor", type = SelectorType.SOLO, greedy = True,
                                  FonSelect = self.textEditor.onSelect,
                                  FonDeselect = self.textEditor.onDeselect
                            )
        )

        self.onModifyDefinition()


    def onModifyDefinition(self):
        # width is a lambda so is automatically updated
        self.textEditor.setRows(self.definition.rows)
        # isDynamic is immutable once set

    # top left corner, screen ref
    def getX(self) -> float:
        return self.getPosition().screenRef[0] - self.textEditor.getWidth() / 2
    
    # top left corner, screen ref
    def getY(self) -> float:
        return self.getPosition().screenRef[1] - self.textEditor.originalHeight / 2
    
    # for dynamic widgets. how much to stretch command height by
    def getCommandStretch(self) -> int:
        return max(0, self.textEditor.getHeight() - self.textEditor.originalHeight)
    
    def onCommandStretch(self):
        #print("widget stretch")
        self.notify()
    
    def getValue(self) -> bool:
        return self.textEditor.getText()

    def isTouchingWidget(self, position: PointRef) -> bool:
        return self.textEditor.isTouching(position)
    
    def drawWidget(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        self.textEditor.draw(screen, isActive, isHovered, self.getOpacity())


class TextboxWidgetDefinition(WidgetDefinition):

    def __init__(self, name: str, px: int, py: int, pwidth: float, rows: int, isDynamic: bool, isNumOnly: bool, isCentered: bool):
        super().__init__(name, px, py)

        self.pwidth = pwidth
        self.rows = rows
        self.isDynamic = isDynamic
        self.isNumOnly = isNumOnly
        self.isCentered = isCentered

    def make(self, parentCommand) -> TextboxWidgetEntity:
        return TextboxWidgetEntity(parentCommand, self)
    
# dynamic, no text restrictions
class CodeTextboxWidgetDefinition(TextboxWidgetDefinition):
    def __init__(self, name: str, px: int, py: int, pwidth: float):
        super().__init__(name, px, py, pwidth, 1, isDynamic = True, isNumOnly = False, isCentered = False)

# numbers only, static
class ValueTextboxWidgetDefinition(TextboxWidgetDefinition):

    def __init__(self, name: str, px: int, py: int, pwidth: float):
        super().__init__(name, px, py, pwidth, 1, isDynamic = False, isNumOnly = True, isCentered = True)