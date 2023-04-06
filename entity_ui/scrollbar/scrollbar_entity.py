from entity_base.entity import Entity
from entity_base.listeners.select_listener import SelectLambda, SelectorType
from entity_base.listeners.drag_listener import DragLambda

from common.reference_frame import PointRef, Ref
from common.dimensions import Dimensions
from common.draw_order import DrawOrder

from data_structures.observer import Observable
from utility.math_functions import isInsideBox2, clamp

import pygame

class ScrollbarEntity(Entity, Observable):

    # parent should be of ScrollbarContainerEntity type
    def __init__(self, parent):

        super().__init__(
            parent = parent,
            select = SelectLambda(self, "scroll", type = SelectorType.SOLO),
            drag = DragLambda(self,
                              FonStartDrag = self.onStartDrag,
                              FonDrag = self.onDrag),
            drawOrder = DrawOrder.SCROLLBAR
        )

        self.percent = 0
        self.setContentHeight(0)
        self.recomputePosition()

    # How much the scrollbar offsets the scrolling container in negative y direction
    def getScrollOffset(self) -> float:
        return 0 - self.percent * (self.contentHeight - self._pheight(1))

    def defineTopY(self) -> tuple:
        return self._py(0) + (self._pheight(1) - self.HEIGHT) * self.percent
    
    def defineCenterX(self) -> float:
        return self._px(0.5)

    def defineWidth(self) -> float:
        return self._mwidth(1)
    
    def defineHeight(self) -> float:
        if self.contentHeight == 0:
            ratio = 1
        else:
            ratio = min(1, self._pheight(1) / self.contentHeight)
        return self._pheight(1) * ratio


    def setContentHeight(self, height):
        BOTTOM_MARGIN = 70
        self.contentHeight = height + BOTTOM_MARGIN
        self.recomputePosition()


    def onStartDrag(self, mouse: PointRef):
        self.mouseStartY = mouse.screenRef[1]
        self.startDragY = self.TOP_Y

    def onDrag(self, mouse: PointRef):
        absoluteDragY = self.startDragY + mouse.screenRef[1] - self.mouseStartY
        self.percent = (absoluteDragY - self._py(0)) / (self._pheight(1) - self.HEIGHT)
        self.percent = clamp(self.percent, 0, 1)
        self.recomputePosition()
        self.notify()

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        color = [150,150,150] if isHovered else [170,170,170]
        pygame.draw.rect(screen, color, self.RECT, 1)