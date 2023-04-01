from Animation.motion_profile import MotionProfile

from BaseEntity.entity import Entity

from Commands.command_expansion import CommandExpansion
from Observers.observer import Observer

from linked_list import LinkedListNode
from dimensions import Dimensions

"""
Owned by CommandBlockEntity
Handles the sole resonsibility of managing the position of the CommandBlockEntity
This includes setting y position to be previous y + previous height
This also handles the expand/shrink animation
"""

class CommandBlockPosition:

    def __init__(self, commandBlockEntity: Entity | LinkedListNode, commandExpansion: CommandExpansion, dimensions: Dimensions):
        self.command = commandBlockEntity
        self.commandExpansion = commandExpansion
        self.dimensions = dimensions

        # whenever a global expansion flag is changed, recompute each individual command expansion
        self.commandExpansion.addObserver(Observer(onNotify = self.recomputeExpansion))

        self.Y_BETWEEN_COMMANDS_MIN = 30
        self.Y_BETWEEN_COMMANDS_MAX = 120
        self.X_MARGIN_LEFT = 6
        self.X_MARGIN_RIGHT = 18

        # the height of the command is updated through a motion profile animation based on goal height (minimized/maximized)
        self._isExpanded = False
        self.expandMotion = MotionProfile(self.Y_BETWEEN_COMMANDS_MIN, self.Y_BETWEEN_COMMANDS_MIN,
                                          speed = 0.25)
        
        self.setY(0)
        self.recomputeExpansion()


    def getX(self) -> float:
        return self.dimensions.FIELD_WIDTH + self.X_MARGIN_LEFT
    
    def getY(self) -> float:
        return self.currentY
    
    def setY(self, y: float):
        self.currentY = y
    
    def getWidth(self) -> float:
        return self.dimensions.PANEL_WIDTH - self.X_MARGIN_LEFT - self.X_MARGIN_RIGHT
    
    # get height of the command
    def getHeight(self) -> float:
        if not self.command.isVisible():
            return 0
        return self.expandMotion.get()
    
    def getCenterPosition(self) -> tuple:
        x = self.dimensions.FIELD_WIDTH + self.dimensions.PANEL_WIDTH / 2
        y = self.getY() + self.getHeight() / 2
        return x,y
    
    # the center y position of the title header on the top of the command
    def getCenterHeadingY(self) -> float:
        return self.getY() + self.Y_BETWEEN_COMMANDS_MIN / 2
    
    # return 1 if expanded, 0 if not, and in between
    def getExpandedRatio(self) -> float:
        return (self.getHeight() - self.Y_BETWEEN_COMMANDS_MIN) / (self.Y_BETWEEN_COMMANDS_MAX - self.Y_BETWEEN_COMMANDS_MIN)
    
    def getAddonPosition(self, px: float, py: float) -> tuple:
        x = self.getX() + px * self.getWidth()
        y = self.Y_BETWEEN_COMMANDS_MIN
        y += self.getY() + py * (self.getHeight() - self.Y_BETWEEN_COMMANDS_MIN)
        return x,y

    # every tick, update animation if exists
    def onTick(self):
        if not self.expandMotion.isDone():
            self.expandMotion.tick()
            self.command.path.recomputeY()

    # based on this command's height, find next command's y
    def updateNextY(self):

        nextInsert = self.command.getNext()

        if nextInsert is None:
            return
        
        nextInsert.setY(self.currentY + self.getHeight())
        nextInsert.updateNextY()

    # expand command
    def setExpanded(self):
        
        # If all are being forced to contract right now, disable forceContract, but 
        # all other commands should retain being contracted except this one
        if self.commandExpansion.getForceCollapse():
            self.command.path.setAllLocalExpansion(False)
            self.commandExpansion.setForceCollapse(False)

        self._isExpanded = True
        self.recomputeExpansion()

    # minimize command
    def setCollapsed(self):

         # If all are being forced to expand right now, disable forceExpand, but 
        # all other commands should retain being expanded except this one
        if self.commandExpansion.getForceExpand():
            self.command.path.setAllLocalExpansion(True)
            self.commandExpansion.setForceExpand(False)

        self._isExpanded = False
        self.recomputeExpansion()

    def isExpanded(self) -> bool:
        if self.commandExpansion.getForceCollapse():
            return False
        elif self.commandExpansion.getForceExpand():
            return True
        return self._isExpanded

    def recomputeExpansion(self):

        if self.isExpanded():
            x = self.Y_BETWEEN_COMMANDS_MAX
        else:
            x = self.Y_BETWEEN_COMMANDS_MIN
        
        self.expandMotion.setEndValue(x)

    