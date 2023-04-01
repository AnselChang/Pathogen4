from BaseEntity.EntityListeners.click_listener import ClickListener, ClickLambda
from BaseEntity.EntityListeners.drag_listener import DragListener, DragLambda
from BaseEntity.EntityListeners.select_listener import SelectListener, SelectLambda
from BaseEntity.EntityListeners.tick_listener import TickListener, TickLambda
from BaseEntity.EntityListeners.hover_listener import HoverListener, HoverLambda

from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.hover_listener import HoverLambda

from Widgets.widget_type import WidgetType
from Widgets.defined_widget import DefinedWidget

from image_manager import ImageID
from draw_order import DrawOrder
from reference_frame import PointRef, Ref
import pygame

"""
Belongs to a specific CommandBlockEntity.
Owns a DefinedWidget which stores information about the widget's context for all commands of that type
Stores the actual value of the widget
"""

class WidgetEntity(Entity):

    def __init__(self, parentCommand: Entity, definedWidget: DefinedWidget):
            

        super().__init__(
            click = ClickLambda(self, FonLeftClick = self.onLeftClick, FonRightClick = self.onRightClick),
            drag = DragLambda(self, FstartDragging = self.onStartDrag, FdragOffset = self.onDragOffset, FstopDragging = self.onStopDrag),
            hover = HoverLambda(self),
            drawOrder = DrawOrder.WIDGET
        )

        self.parentCommand = parentCommand
        self.definedWidget = definedWidget
        self.widgetType = definedWidget.widgetType

        # Holds the widget state for the specific CommandBlockEntity that owns this
        self.value = self.widgetType.getDefaultValue()

    def getImage(self, id: ImageID, opacity: float = 1) -> pygame.Surface:
        return self.parentCommand.images.get(id, opacity)

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
        return self.widgetType.isTouching(self, position)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        self.widgetType.draw(self, screen, isActive, isHovered)

    def toString(self) -> str:
        return "widget"
    
    def onLeftClick(self):
        self.widgetType.onLeftClick(self)

    def onRightClick(self):
        self.widgetType.onRightClick(self)

    def onStartDrag(self):
        self.widgetType.onStartDrag(self)

    def onDragOffset(self):
        self.widgetType.onDragOffset(self)

    def onStopDrag(self):
        self.widgetType.onStopDrag(self)