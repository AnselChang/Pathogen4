from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from root_container.panel_container.element.widget.widget_entity import WidgetContainer
from root_container.panel_container.element.widget.widget_definition import WidgetDefinition

from entity_ui.text.text_editor_entity import TextEditorEntity, TextEditorMode

from common.font_manager import FontID, DynamicFont
from common.image_manager import ImageID
from common.draw_order import DrawOrder
from common.reference_frame import PointRef, Ref



class TextboxWidgetContainer(WidgetContainer['TextboxWidgetDefinition']):

    def __init__(self, parent, parentCommand: CommandBlockEntity, definition: 'TextboxWidgetDefinition'):


        font: DynamicFont = parentCommand.fonts.getDynamicFont(definition.fontID, definition.fontSize)

        super().__init__(parent, parentCommand, definition)
        self.recomputePosition()

        self.textEditor = TextEditorEntity(
            self,
            font,
            isDynamic = definition.isDynamic,
            isNumOnly = definition.isNumOnly,
            defaultText = definition.defaultText
        )

        # Sends notification when text height changes
        self.textEditor.subscribe(onNotify = parentCommand.updateTargetHeight)


    # for dynamic widgets. how much to stretch command height by
    def getCommandStretch(self) -> int:
        return self.textEditor.getHeightOffset()
    
    def getValue(self) -> bool:
        return self.textEditor.getText()


class TextboxWidgetDefinition(WidgetDefinition):

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
        super().__init__(name, fontID = FontID.FONT_NORMAL, fontSize = 15, defaultText = defaultText, isDynamic = False, isNumOnly = True)