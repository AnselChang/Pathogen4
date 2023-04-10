from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from root_container.panel_container.element.widget.widget_entity import WidgetContainer
from root_container.panel_container.element.widget.widget_definition import WidgetDefinition

from entity_ui.text.text_editor_entity import TextEditorEntity, TextEditorMode

from common.font_manager import FontID
from common.image_manager import ImageID
from common.draw_order import DrawOrder
from common.reference_frame import PointRef, Ref



class TextboxWidgetContainer(WidgetContainer['TextboxWidgetDefinition']):

    def __init__(self, parent, parentCommand: CommandBlockEntity, definition: 'TextboxWidgetDefinition'):

        super().__init__(parent, parentCommand, definition)

        self.textEditor = None
        self.recomputePosition()

        fontID = definition.fontID
        fontSize = definition.fontSize

        if fontID is None:
            fontID = definition.LABEL_FONT
        if fontSize is None:
            fontSize = definition.LABEL_SIZE

        self.textEditor = TextEditorEntity(
            self,
            fontID, fontSize,
            isDynamic = definition.isDynamic,
            isNumOnly = definition.isNumOnly,
            defaultText = definition.defaultText
        )

    # for dynamic widgets. how much to stretch command height by
    def getCommandStretch(self) -> int:
        return self.textEditor.getHeightOffset()
    
    def getValue(self) -> bool:
        return self.textEditor.getText()
    
    def defineWidth(self) -> float:
        if self.textEditor is None:
            return 0
        return self.textEditor.defineWidth()
    
    def defineHeight(self) -> float:
        if self.textEditor is None:
            return 0
        return self.textEditor.defineHeight()

class TextboxWidgetDefinition(WidgetDefinition):

    # set fontID and fontSize to None to use defaults
    def __init__(self, variableName: str, fontID: FontID, fontSize: float, defaultText: str, isDynamic: bool, isNumOnly: bool):
        super().__init__(variableName)

        self.fontID = fontID
        self.fontSize = fontSize
        self.defaultText = defaultText
        self.isDynamic = isDynamic
        self.isNumOnly = isNumOnly

    def makeElement(self, parent, parentCommand, pathAdapter) -> TextboxWidgetContainer:
        return TextboxWidgetContainer(parent, parentCommand, self)
    
# dynamic, no text restrictions
class CodeTextboxWidgetDefinition(TextboxWidgetDefinition):
    def __init__(self):
        super().__init__("code", fontID = FontID.FONT_CODE, fontSize = 10, defaultText = "", isDynamic = True, isNumOnly = False)

# numbers only, static
class ValueTextboxWidgetDefinition(TextboxWidgetDefinition):

    def __init__(self, name: str, defaultValue: float):
        defaultText = str(round(defaultValue, 3))
        super().__init__(name, fontID = None, fontSize = None, defaultText = defaultText, isDynamic = False, isNumOnly = True)