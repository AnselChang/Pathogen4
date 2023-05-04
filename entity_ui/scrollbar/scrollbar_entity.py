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
        self.contentHeight = 0

    # How much the scrollbar offsets the scrolling container in negative y direction
    def getScrollOffset(self) -> float:
        return 0 - self.percent * (self.contentHeight - self._pheight(1))

    def defineTopY(self) -> tuple:
        return self._py(0) + (self._pheight(1) - self.HEIGHT) * self.percent
    
    def defineCenterX(self) -> float:
        return self._px(0.5)

    def defineWidth(self) -> float:
        return self._pwidth(0.7)
    
    def defineHeight(self) -> float:
        if self.contentHeight == 0:
            ratio = 1
        else:
            ratio = min(1, self._pheight(1) / self.contentHeight)
        return self._pheight(1) * ratio


    def setContentHeight(self, height):
        BOTTOM_MARGIN = 70

        # do nothing if no change in height
        if (height + BOTTOM_MARGIN) == self.contentHeight:
            return
        
        self.contentHeight = height + BOTTOM_MARGIN

        moveableDistance = (self._pheight(1) - self.defineHeight())
        if moveableDistance == 0:
            self.percent = 0
        else:
            self.percent = (self.TOP_Y - self._py(0)) / moveableDistance
            self.percent = clamp(self.percent, 0, 1)

        self.recomputeEntity()
        self.notify()

    def setManualOffset(self, y):
        self.percent = (y - self._py(0)) / (self.contentHeight - self._pheight(1))
        self.percent = clamp(self.percent, 0, 1)
        self.recomputeEntity()
        self.notify()

    def onStartDrag(self, mouse: tuple):
        self.mouseStartY = mouse[1]
        self.startDragY = self.TOP_Y

    def onDrag(self, mouse: tuple):
        absoluteDragY = self.startDragY + mouse[1] - self.mouseStartY

        moveableDistance = (self._pheight(1) - self.HEIGHT)
        if moveableDistance == 0:
            self.percent = 0
        else:
            self.percent = (absoluteDragY - self._py(0)) / moveableDistance
            self.percent = clamp(self.percent, 0, 1)
        self.recomputeEntity()
        self.notify()

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:

        color = [140,140,140] if isHovered else [160,160,160]
        pygame.draw.rect(screen, color, self.RECT)