from __future__ import annotations
from typing import TYPE_CHECKING

from root_container.panel_container.element.row.element_entity import ElementContainer
if TYPE_CHECKING:
    from root_container.panel_container.element.widget.widget_definition import WidgetDefinition
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity


from entity_base.listeners.click_listener import ClickListener, ClickLambda
from entity_base.listeners.drag_listener import DragListener, DragLambda
from entity_base.listeners.select_listener import SelectListener, SelectLambda
from entity_base.listeners.tick_listener import TickListener, TickLambda
from entity_base.listeners.hover_listener import HoverListener, HoverLambda
from entity_base.listeners.key_listener import KeyListener
from entity_base.listeners.hover_listener import HoverLambda

from entity_base.entity import Entity

from data_structures.observer import Observable

from common.draw_order import DrawOrder
from typing import TypeVar, Generic
from abc import abstractmethod

"""
Belongs to a specific CommandBlockEntity.
Owns a DefinedWidget which stores information about the widget's context for all commands of that type
Stores the actual value of the widget
"""
# notifies observers when getCommandStretch() changes
T = TypeVar('T')
class WidgetContainer(ElementContainer, Observable, Generic[T]):

    def __init__(self, parent, parentCommand: CommandBlockEntity, definition: WidgetDefinition):
        
        super().__init__(parent = parent)

        self.parentCommand = parentCommand
        self.definition: WidgetDefinition | T = definition

    # for dynamic widgets. how much to stretch command height by
    def getCommandStretch(self) -> int:
        return 0

    def onModifyDefinition(self):
        pass

    @abstractmethod
    def getValue(self) -> str | float:
        pass
    
    def isVisible(self) -> bool:
        return self.parentCommand.isVisible() and not self.parentCommand.isFullyCollapsed()

    def getOpacity(self) -> float:
        return self.parentCommand.getAddonsOpacity()