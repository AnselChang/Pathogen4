from BaseEntity.EntityListeners.click_listener import ClickListener, ClickLambda
from BaseEntity.EntityListeners.drag_listener import DragListener, DragLambda
from BaseEntity.EntityListeners.select_listener import SelectListener, SelectLambda
from BaseEntity.EntityListeners.tick_listener import TickListener, TickLambda
from BaseEntity.EntityListeners.hover_listener import HoverListener, HoverLambda
from BaseEntity.EntityListeners.key_listener import KeyListener

from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.hover_listener import HoverLambda


from Tooltips.tooltip import TooltipOwner, Tooltip

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

class WidgetEntity(Entity):

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

    @abstractmethod
    def onModifyDefinition(self):
        pass

    @abstractmethod
    def getValue(self) -> str | float:
        pass

    @abstractmethod
    def isTouchingWidget(self, position: PointRef) -> bool:
        pass

    # override this
    def onCommandExpand(self):
        pass

    # override this
    def onCommandCollapse(self):
        pass

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        if not self.parentCommand.isFullyCollapsed():
            self.drawWidget(screen, isActive, isHovered)

    @abstractmethod
    def drawWidget(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pass

    def getPosition(self) -> PointRef:
        px, py = self.definition.getPositionRatio()
        x,y = self.parentCommand.getAddonPosition(px, py)
        return PointRef(Ref.SCREEN, (x, y))
    
    def getOpacity(self) -> float:
        return self.parentCommand.getAddonsOpacity()

    def getName(self) -> str:
        return self.definition.getName()
    
    def isVisible(self) -> bool:
        return self.parentCommand.isVisible()

    def isTouching(self, position: PointRef) -> bool:
        return self.parentCommand.isExpanded() and self.isTouchingWidget(position)

    def toString(self) -> str:
        return "widget"