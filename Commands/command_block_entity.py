from BaseEntity.entity import Entity
from BaseEntity.EntityFunctions.select_function import SelectLambda

from Adapters.adapter import Adapter

from Commands.command_state import CommandState
from CommandCreation.command_type import COMMAND_INFO

from linked_list import LinkedListNode

from draw_order import DrawOrder
from dimensions import Dimensions
from reference_frame import PointRef, Ref
from pygame_functions import shade
from math_functions import isInsideBox2
import pygame



class CommandBlockEntity(Entity, LinkedListNode['CommandBlockEntity']):
    
    def __init__(self, state: CommandState, dimensions: Dimensions):
        super().__init__(
            select = SelectLambda(self, "command"),
            drawOrder = DrawOrder.COMMANND_BLOCK)
        LinkedListNode.__init__(self)
        self.setState(state)
        
        self.dimensions = dimensions

        self.START_Y = 35
        self.Y_BETWEEN_COMMANDS = 40
        self.Y_MARGIN = 3
        self.CORNER_RADIUS = 3
        self.X_MARGIN = 5

        self.recomputePosition()

    def recomputePosition(self):

        # calculate the upper border of the command (still a margin between mouse and command)
        if self.getPrevious() is None:
            self.currentY = self.START_Y 
        else:
            self.currentY = self.getPrevious().currentY + self.Y_BETWEEN_COMMANDS
        
        # Recursively update commands below this one
        if self.getNext() is not None:
            self.getNext().recomputePosition()

    def setState(self, state: CommandState):
        self.state = state

    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        x = self.dimensions.FIELD_WIDTH
        width = self.dimensions.PANEL_WIDTH
        y = self.currentY
        height = self.Y_BETWEEN_COMMANDS
        return isInsideBox2(*position.screenRef, x, y, width, height)

    def getPosition(self) -> PointRef:
        x = self.dimensions.FIELD_WIDTH + self.dimensions.PANEL_WIDTH / 2
        y = self.currentY + self.Y_BETWEEN_COMMANDS / 2
        return PointRef(Ref.SCREEN, (x,y))

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        x = self.dimensions.FIELD_WIDTH + self.X_MARGIN
        width = self.dimensions.PANEL_WIDTH - 2 * self.X_MARGIN
        y = self.currentY + self.Y_MARGIN
        height = self.Y_BETWEEN_COMMANDS - 2 * self.Y_MARGIN

        color = COMMAND_INFO[self.state.type].color
        if isHovered:
            color = shade(color, 1.2)
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius = self.CORNER_RADIUS)

        if isActive:
            pygame.draw.rect(screen, (0,0,0), (x, y, width, height), border_radius = self.CORNER_RADIUS, width = 1)


    def toString(self) -> str:
        pass
