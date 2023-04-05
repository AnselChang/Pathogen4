from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.select_listener import SelectLambda, SelectorType
from BaseEntity.EntityListeners.drag_listener import DragLambda

from reference_frame import PointRef, Ref
from dimensions import Dimensions
from draw_order import DrawOrder

from Observers.observer import Observable
from math_functions import isInsideBox2

import pygame

class ScrollbarEntity(Entity, Observable):

    def __init__(self):

        super().__init__(
            select = SelectLambda(self, "scroll", type = SelectorType.SOLO),
            drag = DragLambda(self,
                              FonStartDrag = self.onStartDrag,
                              FonDrag = self.onDrag),
            drawOrder = DrawOrder.SCROLLBAR
        )

        self.dimensions.subscribe(onNotify = self.update)        

        self.barYOffset = 0
        self.recomputePosition()

    def getTopLeft(self) -> tuple:
        return max(0, min(self.barYOffset, self._parent.HEIGHT - self.HEIGHT))

    # must impl both of these if want to contain other entity
    def getWidth(self) -> float:
        return self._mwidth(1)
    
    def getHeight(self) -> float:
        if self.contentHeight == 0:
            ratio = 1
        else:
            ratio = min(1, self._parent.HEIGHT / self.contentHeight)
        return self._parent.HEIGHT * ratio


    def setContentHeight(self, height):
        BOTTOM_MARGIN = 70
        self.contentHeight = height + BOTTOM_MARGIN
        self.recomputePosition()


    def onStartDrag(self, mouse: PointRef):
        self.mouseStartY = mouse.screenRef[1]
        self.startBarYOffset = self.barYOffset

    def onDrag(self, mouse: PointRef):
        self.barYOffset = self.startBarYOffset + mouse.screenRef[1] - self.mouseStartY
        self.recomputePosition()

    def isTouching(self, position: PointRef) -> bool:
        return isInsideBox2(*position.screenRef, *self.RECT)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        color = [150,150,150] if isHovered else [170,170,170]
        pygame.draw.rect(screen, color, self.RECT, 1)