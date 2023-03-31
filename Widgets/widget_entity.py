from BaseEntity.EntityListeners.click_listener import Click, ClickLambda
from BaseEntity.EntityListeners.drag_listener import Drag, DragLambda
from BaseEntity.EntityListeners.select_listener import Select, SelectLambda
from BaseEntity.EntityListeners.tick_listener import Tick, TickLambda
from BaseEntity.EntityListeners.hover_listener import Hover, HoverLambda

from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.hover_listener import HoverLambda

from Widgets.widget_value import WidgetValue
from Widgets.widget_type import WidgetType
from Widgets.defined_widget import DefinedWidget

from draw_order import DrawOrder
from reference_frame import PointRef, Ref
import pygame

"""
Belongs to a specific CommandBlockEntity.
Owns a DefinedWidget which stores information about the widget's context for all commands of that type
Owns a WidgetValue which stores information about the widget's context for this specific CommandBlock
"""

class WidgetEntity(Entity):

    def __init__(self, parentCommand: Entity, definedWidget: DefinedWidget):
            

        super().__init__(
            click = ClickLambda(self, FonLeftClick = self.onLeftClick, FonRightClick = self.onRightClick),
            drag = DragLambda(self, FstartDragging = self.onStartDrag, FdragOffset = self.onDragOffset, FstopDragging = self.onStopDrag),
            hover = HoverLambda(),
            drawOrder = DrawOrder.WIDGET
        )

        self.parentCommand = parentCommand
        self.definedWidget = definedWidget
        self.widgetType = definedWidget.widgetType

        # Holds the widget state for the specific CommandBlockEntity that owns this
        self.value = WidgetValue(value = self.widgetType.getDefaultValue())

    def getPosition(self) -> tuple:
        px, py = self.definedWidget.getPositionRatio()
        x,y = self.parentCommand.getAddonPosition(px, py)
        return PointRef(Ref.SCREEN, (x, y))
    
    def getValue(self) -> float:
        return self.value.getValue()
    
    def setValue(self, value: float):
        self.value.setValue(value)

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