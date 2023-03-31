from Animation.motion_profile import MotionProfile
from Commands.command_inserter import CommandInserter

from BaseEntity.entity import Entity

from linked_list import LinkedListNode
from dimensions import Dimensions

"""
Owned by CommandBlockEntity
Handles the sole resonsibility of managing the position of the CommandBlockEntity
This includes setting y position to be previous y + previous height
This also handles the expand/shrink animation
"""

class CommandBlockPosition:

    def __init__(self, commandBlockEntity: Entity | LinkedListNode[CommandInserter], dimensions: Dimensions):
        self.command = commandBlockEntity
        self.dimensions = dimensions

        self.Y_BETWEEN_COMMANDS_MIN = 30
        self.Y_BETWEEN_COMMANDS_MAX = 100
        self.X_MARGIN = 6

        # the height of the command is updated through a motion profile animation based on goal height (minimized/maximized)
        self.isExpanded = False
        self.expandMotion = MotionProfile(self.Y_BETWEEN_COMMANDS_MIN, self.Y_BETWEEN_COMMANDS_MIN,
                                          speed = 0.25)

        prev = self.getPrevious()
        self.currentY = prev.currentY + prev.getHeight()
        self.updateNextY()

    def getX(self) -> float:
        return self.dimensions.FIELD_WIDTH + self.X_MARGIN
    
    def getY(self) -> float:
        return self.currentY
    
    # get height of the command
    def getHeight(self) -> float:
        if not self.command.isVisible():
            return 0
        return self.expandMotion.get()
    
    # the dimensions of the command rectangle, calculated on-the-fly
    def getRect(self) -> tuple:
        x = self.getX()
        width = self.dimensions.PANEL_WIDTH - 2 * self.X_MARGIN
        y = self.getY()
        height = self.getHeight()
        return x, y, width, height
    
    def getCenterPosition(self) -> tuple:
        x = self.dimensions.FIELD_WIDTH + self.dimensions.PANEL_WIDTH / 2
        y = self.currentY + self.getHeight() / 2
        return x,y
    
    # every tick, update animation if exists
    def onTick(self):
        if not self.expandMotion.isDone():
            self.expandMotion.tick()
            self.updateNextY()

    # based on this command's height, find next command's y
    def updateNextY(self):

        nextInsert = self.command.getNext()

        if nextInsert is None:
            return
        
        nextInsert.setY(self.currentY + self.getHeight())

    # expand command
    def setExpanded(self):
        self.isExpanded = True
        self.expandMotion.setEndValue(self.Y_BETWEEN_COMMANDS_MAX)

    # minimize command
    def setContracted(self):
        self.isExpanded = False
        self.expandMotion.setEndValue(self.Y_BETWEEN_COMMANDS_MIN)