from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from root_container.panel_container.element.widget.widget_entity import WidgetEntity
from root_container.panel_container.element.widget.widget_definition import WidgetDefinition

from entity_ui.text.text_editor_entity import TextEditorEntity, TextEditorMode

from common.font_manager import FontID, DynamicFont
from common.image_manager import ImageID
from common.draw_order import DrawOrder
from common.reference_frame import PointRef, Ref



class TextboxWidgetEntity(WidgetEntity['TextboxWidgetDefinition']):

    def __init__(self, parent, parentCommand: CommandBlockEntity, definition: 'TextboxWidgetDefinition'):


        font: DynamicFont = parentCommand.fonts.getDynamicFont(definition.fontID, definition.fontSize)

        super().__init__(parent, parentCommand, definition)
        self.recomputePosition()

        self.textEditor = TextEditorEntity(
            self,
            font,
            getOpacity = self.getOpacity,
            isDynamic = definition.isDynamic,
            isNumOnly = definition.isNumOnly,
            defaultText = definition.defaultText
        )

        # Sends notification when text height changes
        self.textEditor.subscribe(onNotify = parentCommand.updateTargetHeight)


    def onModifyDefinition(self):
        # width is a lambda so is automatically updated
        self.textEditor.setRows(self.definition.rows)
        # isDynamic is immutable once set

    # top left corner, screen ref
    def getX(self) -> float:
        return self.getPosition().screenRef[0] - self.textEditor.defineWidth() / 2
    
    # top left corner, screen ref
    def getY(self) -> float:
        return self.getPosition().screenRef[1] - self.textEditor.originalHeight / 2
    
    # for dynamic widgets. how much to stretch command height by
    def getCommandStretch(self) -> int:
        return self.textEditor.getHeightOffset()
    
    
    def getValue(self) -> bool:
        return self.textEditor.getText()

    def isTouchingWidget(self, position: PointRef) -> bool:
        return self.textEditor.isTouching(position)



class TextboxWidgetDefinition(WidgetDefinition):

    def __init__(self, name: str, px: int, py: int, pwidth: float, rows: int, fontID: FontID, fontSize: float, defaultText: str, isDynamic: bool, isNumOnly: bool):
        super().__init__(name, px, py)

        self.pwidth = pwidth
        self.rows = rows
        self.fontID = fontID
        self.fontSize = fontSize
        self.defaultText = defaultText
        self.isDynamic = isDynamic
        self.isNumOnly = isNumOnly

    def makeElement(self, parent, parentCommand, pathAdapter) -> TextboxWidgetEntity:
        return TextboxWidgetEntity(parent, parentCommand, self)
    
# dynamic, no text restrictions
class CodeTextboxWidgetDefinition(TextboxWidgetDefinition):
    def __init__(self, name: str, px: int, py: int, pwidth: float):
        super().__init__(name, px, py, pwidth, 1, fontID = FontID.FONT_CODE, fontSize = 10, defaultText = "", isDynamic = True, isNumOnly = False)

# numbers only, static
class ValueTextboxWidgetDefinition(TextboxWidgetDefinition):

    def __init__(self, name: str, px: int, py: int, defaultValue: float):
        defaultText = str(round(defaultValue, 3))
        super().__init__(name, px, py, None, 1, fontID = FontID.FONT_NORMAL, fontSize = 15, defaultText = defaultText, isDynamic = False, isNumOnly = True)