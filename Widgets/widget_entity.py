from BaseEntity.EntityListeners.click_listener import ClickListener, ClickLambda
from BaseEntity.EntityListeners.drag_listener import DragListener, DragLambda
from BaseEntity.EntityListeners.select_listener import SelectListener, SelectLambda
from BaseEntity.EntityListeners.tick_listener import TickListener, TickLambda
from BaseEntity.EntityListeners.hover_listener import HoverListener, HoverLambda
from BaseEntity.EntityListeners.key_listener import KeyListener

from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.hover_listener import HoverLambda


from Tooltips.tooltip import TooltipOwner, Tooltip

from Observers.observer import Observable

from image_manager import ImageID
from draw_order import DrawOrder
from reference_frame import PointRef, Ref
import pygame
from abc import abstractmethod

"""
Belongs to a specific CommandBlockEntity.
Owns a DefinedWidget which stores information about the widget's context for all commands of that type
Stores the actual value of the widget
"""
# notifies observers when getCommandStretch() changes
class WidgetEntity(Entity, Observable):

    def __init__(self, parentCommand: Entity, definition,
                 click: ClickListener = None,
                 drag: DragListener = None,
                 hover: HoverListener = None,
                 tick: TickListener = None,
                 select: SelectListener = None,
                 key: KeyListener = None
                 ):
        
        if hover is None:
            hover = HoverLambda(self)
            
        super().__init__(click = click, drag = drag, hover = hover, tick = tick, select = select, key = key, drawOrder = DrawOrder.WIDGET)

        self.parentCommand = parentCommand
        self.definition = definition
        self.images = parentCommand.images
    

    def getCenter(self) -> tuple:
        return self._px(self.definition.px), self._py(self.definition.py)

    # for dynamic widgets. how much to stretch command height by
    def getCommandStretch(self) -> int:
        return 0

    @abstractmethod
    def onModifyDefinition(self):
        pass

    @abstractmethod
    def getValue(self) -> str | float:
        pass

    @abstractmethod
    def isTouchingWidget(self, position: tuple) -> bool:
        pass

    def getName(self) -> str:
        return self.definition.getName()
    
    def isVisible(self) -> bool:
        return not self.parentCommand.isFullyCollapsed()

    def isTouching(self, position: tuple) -> bool:
        return self.parentCommand.isFullyExpanded() and self.isTouchingWidget(position)

    def getOpacity(self) -> float:
        return self.parentCommand.getAddonsOpacity()