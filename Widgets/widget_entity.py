from BaseEntity.EntityListeners.click_listener import ClickListener, ClickLambda
from BaseEntity.EntityListeners.drag_listener import DragListener, DragLambda
from BaseEntity.EntityListeners.select_listener import SelectListener, SelectLambda
from BaseEntity.EntityListeners.tick_listener import TickListener, TickLambda
from BaseEntity.EntityListeners.hover_listener import HoverListener, HoverLambda

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

    def __init__(self, parentCommand: Entity, definedWidget,
                 click: ClickListener = None,
                 drag: DragListener = None,
                 hover: HoverListener = None,
                 tick: TickListener = None
                 ):
        
        if hover is None:
            hover = HoverLambda(self)
            
        super().__init__(click = click, drag = drag, hover = hover, tick = tick, drawOrder = DrawOrder.WIDGET)

        self.parentCommand = parentCommand
        self.definedWidget = definedWidget
        self.images = parentCommand.images

        # Holds the widget state for the specific CommandBlockEntity that owns this
        self.value = self.getDefaultValue()

    @abstractmethod
    def getDefaultValue(self) -> float:
        pass

    @abstractmethod
    def isTouchingWidget(self, position: PointRef) -> bool:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pass

    def getPosition(self) -> PointRef:
        px, py = self.definedWidget.getPositionRatio()
        x,y = self.parentCommand.getAddonPosition(px, py)
        return PointRef(Ref.SCREEN, (x, y))
    
    def getOpacity(self) -> float:
        return self.parentCommand.getAddonsOpacity()
    
    def getValue(self) -> float:
        return self.value
    
    def setValue(self, value: float):
        self.value = value

    def getName(self) -> str:
        return self.definedWidget.getName()
    
    def isVisible(self) -> bool:
        return self.parentCommand.isVisible()

    def isTouching(self, position: PointRef) -> bool:
        return self.parentCommand.isExpanded() and self.isTouchingWidget(position)

    def toString(self) -> str:
        return "widget"