from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.select_listener import SelectLambda
from BaseEntity.EntityListeners.tick_listener import TickLambda

from Adapters.adapter import Adapter

from Commands.command_state import CommandState
from CommandCreation.command_type import COMMAND_INFO

from EntityHandler.interactor import Interactor

from Animation.motion_profile import MotionProfile

from linked_list import LinkedListNode

from draw_order import DrawOrder
from dimensions import Dimensions
from reference_frame import PointRef, Ref
from pygame_functions import shade
from math_functions import isInsideBox2
import pygame



class CommandBlockEntity(Entity, LinkedListNode['CommandBlockEntity']):

    expandedEntity: 'CommandBlockEntity' = None

    def setState(self, state: CommandState):
        self.state = state
    
    def __init__(self, state: CommandState, interactor: Interactor, dimensions: Dimensions):
        super().__init__(
            select = SelectLambda(self,
                id = "command",
                enableToggle = True,
                FgetHitbox = lambda: pygame.Rect(*self.getRect()),
                FonSelect = self.onSelect,
                FonDeselect = self.onDeselect
            ),
            tick = TickLambda(self, FonTick = self.onTick),
            drawOrder = DrawOrder.COMMANND_BLOCK
        )

        LinkedListNode.__init__(self)
        self.setState(state)
        
        self.interactor = interactor
        self.dimensions = dimensions

        self.Y_BETWEEN_COMMANDS_MIN = 30
        self.Y_BETWEEN_COMMANDS_MAX = 100
        self.CORNER_RADIUS = 3
        self.X_MARGIN = 6

    # commands are sandwiched by CommandInserters
    def getPreviousCommand(self) -> 'CommandBlockEntity':
        return self.getPrevious().getPrevious()
    
    def getNextCommand(self) -> 'CommandBlockEntity':
        return self.getNext().getNext()

    # MUST call this after being added to the linked list
    def initPosition(self):

        # the height of the command is updated through a motion profile animation based on goal height (minimized/maximized)
        self.isExpanded = False
        self.expandMotion = MotionProfile(self.Y_BETWEEN_COMMANDS_MIN, self.Y_BETWEEN_COMMANDS_MIN,
                                          speed = 0.25)

        prev = self.getPrevious()
        self.currentY = prev.currentY + prev.getHeight()
        self.updateNextY()

    # get height of the command
    def getHeight(self) -> float:
        if not self.isVisible():
            return 0
        return self.expandMotion.get()

    # based on this command's height, find next command's y
    def updateNextY(self):

        nextInsert = self.getNext()

        if nextInsert is None:
            return
        
        nextInsert.currentY = self.currentY + self.getHeight()
        nextInsert.updateNextY()
                

    # Update animation every tick
    def onTick(self):
        if not self.expandMotion.isDone():
            self.expandMotion.tick()
            self.updateNextY()

    # expand command
    def setExpanded(self):
        self.isExpanded = True
        CommandBlockEntity.expandedEntity = self
        self.expandMotion.setEndValue(self.Y_BETWEEN_COMMANDS_MAX)

    # minimize command
    def setContracted(self):
        self.isExpanded = False
        CommandBlockEntity.expandedEntity = None
        self.expandMotion.setEndValue(self.Y_BETWEEN_COMMANDS_MIN)

    # try to expand command when selected, but only when it's the only thing selected
    def onSelect(self):

        # only expand if it's the only thing selected
        if self.interactor.selected.hasOnly(self):
            self.setExpanded()
        else:
            if CommandBlockEntity.expandedEntity is not None:
                CommandBlockEntity.expandedEntity.setContracted()

    # minimize command when not selected
    def onDeselect(self):
        self.setContracted()

    def isVisible(self) -> bool:
        return True
    
    # the dimensions of the command rectangle, calculated on-the-fly
    def getRect(self) -> tuple:
        x = self.dimensions.FIELD_WIDTH + self.X_MARGIN
        width = self.dimensions.PANEL_WIDTH - 2 * self.X_MARGIN
        y = self.currentY
        height = self.getHeight()
        return x, y, width, height

    def isTouching(self, position: PointRef) -> bool:
        return isInsideBox2(*position.screenRef, *self.getRect())

    def getPosition(self) -> PointRef:
        x = self.dimensions.FIELD_WIDTH + self.dimensions.PANEL_WIDTH / 2
        y = self.currentY + self.getHeight() / 2
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
