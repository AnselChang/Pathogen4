from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.hover_listener import HoverLambda
from BaseEntity.EntityListeners.click_listener import ClickLambda

from Commands.command_block_entity import CommandBlockEntity

from EntityHandler.interactor import Interactor

from dimensions import Dimensions
from linked_list import LinkedListNode
from reference_frame import PointRef, Ref
from draw_order import DrawOrder

from math_functions import isInsideBox2

import pygame

"""
Appears between each command
A "plus" button that, when clicked, inserts a custom command there
"""

class CommandInserter(Entity, LinkedListNode[CommandBlockEntity]):

    def __init__(self, interactor: Interactor, dimensions: Dimensions, onInsert = lambda: None):

        super().__init__(
            hover = HoverLambda(self, FonHoverOn = self.onHoverOn, FonHoverOff = self.onHoverOff),
            click = ClickLambda(self, FonLeftClick = lambda: onInsert(self)),
            drawOrder = DrawOrder.COMMAND_INSERTER)
        LinkedListNode.__init__(self)

        self.interactor = interactor
        self.dimensions = dimensions

        self.START_Y = 43
        self.Y_MIN = 6
        self.Y_MAX = 15

        # shaded area specs
        self.X_MARGIN = 6
        self.Y_MARGIN = 3
        self.CORNER_RADIUS = 3
        self.MOUSE_MARGIN = 0

        # cross specs
        self.RADIUS = 6
        self.HOVER_RADIUS = 8
        self.THICK = 3 # cross thick radius
        self.THIN = 1 # cross thin radius


        self.isHovered = False

    # MUST CALL THIS AFTER ADDING TO LINKED LIST
    def initPosition(self):
        prev = self.getPrevious()
        if prev is None:
            self.currentY = self.START_Y
        else:
            self.currentY = prev.currentY + prev.getHeight()
        self.updateNextY()

    def onHoverOn(self):

        if len(self.interactor.selected.entities) > 1:
            return

        self.isHovered = True
        self.updateNextY()

    def onHoverOff(self):
        self.isHovered = False
        self.updateNextY()

    def getHeight(self):
        if not self.isVisible():
            return 0
        return self.Y_MAX if self.isHovered else self.Y_MIN

    # based on this command's height, find next command's y
    def updateNextY(self):

        nextCommand = self.getNext()

        if nextCommand is None:
            return
        
        nextCommand.currentY = self.currentY + self.getHeight() 
        
        nextCommand.updateNextY()
        
         
    def isVisible(self) -> bool:
        return True
    
    def getRect(self, big: bool = False) -> tuple:
        x = self.dimensions.FIELD_WIDTH + self.X_MARGIN
        width = self.dimensions.PANEL_WIDTH - self.X_MARGIN*2
        y = self.currentY
        height = self.getHeight()
        
        margin = (-self.MOUSE_MARGIN) if big else self.Y_MARGIN

        y += margin
        height -= margin*2
        
        return x, y, width, height

    def isTouching(self, position: PointRef) -> bool:
        return isInsideBox2(*position.screenRef, *self.getRect(True))

    def getPosition(self) -> PointRef:
        x = self.dimensions.FIELD_WIDTH + self.dimensions.PANEL_WIDTH / 2
        y = self.currentY + self.getHeight() / 2
        return PointRef(Ref.SCREEN, (x, y))

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        

        if isHovered:
            # draw shaded area
            pygame.draw.rect(screen, [160, 160, 160], self.getRect(), border_radius = self.CORNER_RADIUS)

            # draw cross
            x,y = self.getPosition().screenRef
            pygame.draw.rect(screen, [255,255,255], [x - self.THICK, y - self.THIN, self.THICK*2, self.THIN*2])
            pygame.draw.rect(screen, [255,255,255], [x - self.THIN, y - self.THICK, self.THIN*2, self.THICK*2])

    def toString(self) -> str:
        return "command inserter"