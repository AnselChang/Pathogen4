from BaseEntity.entity import Entity
from BaseEntity.EntityFunctions.select_function import SelectLambda

from Adapters.adapter import Adapter

from Commands.command_state import CommandState
from CommandCreation.command_type import COMMAND_INFO

from EntityHandler.interactor import Interactor

from linked_list import LinkedListNode

from draw_order import DrawOrder
from dimensions import Dimensions
from reference_frame import PointRef, Ref
from pygame_functions import shade
from math_functions import isInsideBox2
import pygame



class CommandBlockEntity(Entity, LinkedListNode['CommandBlockEntity']):

    expanded: 'CommandBlockEntity' = None
    
    def __init__(self, state: CommandState, interactor: Interactor, dimensions: Dimensions):
        super().__init__(
            select = SelectLambda(self,
                id = "command",
                enableToggle = True,
                FgetHitbox = lambda: pygame.Rect(*self.getRect()),
                FonSelect = self.onSelect,
                FonDeselect = self.onDeselect
            ),
            drawOrder = DrawOrder.COMMANND_BLOCK
        )

        LinkedListNode.__init__(self)
        self.setState(state)
        
        self.interactor = interactor
        self.dimensions = dimensions

        self.START_Y = 43
        self.Y_BETWEEN_COMMANDS_MIN = 40
        self.Y_BETWEEN_COMMANDS_MAX = 100
        self.Y_MARGIN = 4
        self.CORNER_RADIUS = 3
        self.X_MARGIN = 6

        # the height of the command. set to min or max based on whether it is selected
        self.thisHeight = self.Y_BETWEEN_COMMANDS_MIN
        self.recomputePosition()

    def recomputePosition(self):

        prev = self.getPrevious()
        next = self.getNext()

        # calculate the upper border of the command (still a margin between mouse and command)
        if prev is None:
            self.currentY = self.START_Y 
        else:
            self.currentY = prev.currentY + prev.thisHeight
        
        # Recursively update commands below this one
        if next is not None:
            next.recomputePosition()

    def onSelect(self):

        # only expand if it's the only thing selected
        if not self.interactor.selected.hasOnly(self):

            if CommandBlockEntity.expanded is not None:
                CommandBlockEntity.expanded.onDeselect()

            return

        self.thisHeight = self.Y_BETWEEN_COMMANDS_MAX
        CommandBlockEntity.expanded = self

        if self.getNext() is not None:
            self.getNext().recomputePosition()

    def onDeselect(self):
        self.thisHeight = self.Y_BETWEEN_COMMANDS_MIN

        if self.getNext() is not None:
            self.getNext().recomputePosition()

    def setState(self, state: CommandState):
        self.state = state

    def isVisible(self) -> bool:
        return True
    
    def getRect(self) -> tuple:
        x = self.dimensions.FIELD_WIDTH + self.X_MARGIN
        width = self.dimensions.PANEL_WIDTH - 2 * self.X_MARGIN
        y = self.currentY + self.Y_MARGIN
        height = self.thisHeight - 2 * self.Y_MARGIN
        return x, y, width, height

    def isTouching(self, position: PointRef) -> bool:
        return isInsideBox2(*position.screenRef, *self.getRect())

    def getPosition(self) -> PointRef:
        x = self.dimensions.FIELD_WIDTH + self.dimensions.PANEL_WIDTH / 2
        y = self.currentY + self.thisHeight / 2
        return PointRef(Ref.SCREEN, (x,y))

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        x, y, width, height = self.getRect()

        color = COMMAND_INFO[self.state.type].color
        if isHovered:
            color = shade(color, 1.2)
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius = self.CORNER_RADIUS)

        if isActive:
            pygame.draw.rect(screen, (0,0,0), (x, y, width, height), border_radius = self.CORNER_RADIUS, width = 1)


    def toString(self) -> str:
        pass
