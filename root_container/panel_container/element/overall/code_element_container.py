from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from root_container.panel_container.element.overall.abstract_elements_container import AbstractElementsContainer

from adapter.path_adapter import PathAdapter
from command_creation.command_definition import CommandDefinition
from entity_ui.text.text_editor_entity import TextEditorEntity
from common.font_manager import FontID
"""
For the special case of code command block, where, instead of a list of rows
of elements, we have a single code element that is a text box
"""

class CodeElementContainer(AbstractElementsContainer):
    
    def __init__(self, parentCommand: CommandBlockEntity, commandDefinition: CommandDefinition, pathAdapter: PathAdapter):

        super().__init__(parentCommand, commandDefinition, pathAdapter)

        self.textEditor = None
        self.recomputePosition()

        self.textEditor = TextEditorEntity(self,
            fontID = FontID.FONT_CODE,
            fontSize = 12,
            isDynamic = True,
            isNumOnly = False,
            isCentered = False,
            isFixedWidth = True,
            defaultText = "// [Enter code here]"
        )

        self.textEditor.subscribe(onNotify = self._notify)

    def _notify(self):
        print("code element container notified")
        self.notify()


    # This container is dynamically fit to DynamicGroupContainer
    def defineHeight(self) -> float:
        if self.textEditor is None:
            return 0
        return self.textEditor.defineHeight()
    
    # Element and label define their own x positions along width of command block
    def defineWidth(self) -> float:
        return self._pwidth(0.9)

    def defineLeftX(self) -> float:
        return self._px(0.05)