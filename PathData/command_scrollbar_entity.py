from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.select_listener import SelectLambda, SelectorType
from BaseEntity.EntityListeners.drag_listener import DragLambda

from reference_frame import PointRef, Ref
from dimensions import Dimensions
from draw_order import DrawOrder

from Observers.observer import Observer, Observable
from math_functions import isInsideBox2

import pygame

class CommandScrollbarEntity(Entity, Observable):

    def __init__(self, dimensions: Dimensions):

        super().__init__(
            select = SelectLambda(self, "scroll", type = SelectorType.SOLO),
            drag = DragLambda(self,
                              FonStartDrag = self.onStartDrag,
                              FonDrag = self.onDrag),
            drawOrder = DrawOrder.SCROLLBAR
        )

        self.dimensions = dimensions
        self.dimensions.subscribe(Observer(onNotify = self.update))

        self.UPPER_MARGIN = 35
        self.LOWER_MARGIN = 3
        self.RIGHT_MARGIN = 2


        self.y = self.UPPER_MARGIN
        self.width = 10

        self.barYOffset = 0

    def getOffset(self):
        return self.barYOffset / self.getHeight() * (self.contentHeight)

    def getHeight(self):
        return self.dimensions.SCREEN_HEIGHT - self.UPPER_MARGIN - self.LOWER_MARGIN
    
    def getX(self):
        return self.dimensions.FIELD_WIDTH + self.dimensions.PANEL_WIDTH - self.width - self.RIGHT_MARGIN

    def setContentHeight(self, height):
        BOTTOM_MARGIN = 70
        self.contentHeight = height + BOTTOM_MARGIN
        self.update()

    def update(self):
    
        height = self.getHeight()

        if self.contentHeight == 0:
            ratio = 1
        else:
            ratio = min(1, height / self.contentHeight)
        self.barHeight = height * ratio

        self.barYOffset = max(0, min(self.barYOffset, height - self.barHeight))

    def onStartDrag(self, mouse: PointRef):
        self.mouseStartY = mouse.screenRef[1]
        self.startBarYOffset = self.barYOffset

    def onDrag(self, mouse: PointRef):
        self.barYOffset = self.startBarYOffset + mouse.screenRef[1] - self.mouseStartY
        self.notify() # this will indrectly call update() as well

    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        return isInsideBox2(*position.screenRef, self.getX(), self.y + self.barYOffset, self.width, self.barHeight)

    def getPosition(self) -> PointRef:
        x = self.getX() + self.width / 2
        y = self.y + self.barYOffset + self.barHeight / 2
        return PointRef(Ref.SCREEN, (x,y))

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pygame.draw.rect(screen, (0,0,0), [self.getX(), self.y, self.width, self.getHeight()], 1)

        INNER_MARGIN = 1
        color = [150,150,150] if isHovered else [170,170,170]
        x = self.getX() + INNER_MARGIN
        y = self.y + self.barYOffset + INNER_MARGIN
        width = self.width - INNER_MARGIN * 2
        height = self.barHeight - INNER_MARGIN * 2
        pygame.draw.rect(screen, color, [x, y, width, height])