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

    def __init__(self, commandBlockEntity: Entity | LinkedListNode, commandExpansion: CommandExpansion, dimensions: Dimensions, defaultExpand: bool):
        self.command = commandBlockEntity
        self.commandExpansion = commandExpansion
        self.dimensions = dimensions

        # whenever a global expansion flag is changed, recompute each individual command expansion
        self.commandExpansion.addObserver(Observer(onNotify = self.recomputeExpansion))

        self.Y_BETWEEN_COMMANDS_MIN = 30
        self.X_MARGIN_LEFT = 6
        self.X_MARGIN_RIGHT = 18

        # the height of the command is updated through a motion profile animation based on goal height (minimized/maximized)
        self._isExpanded = defaultExpand
        self.expandMotion = MotionProfile(self.Y_BETWEEN_COMMANDS_MIN, self.Y_BETWEEN_COMMANDS_MIN,
                                          speed = 0.4)
        
        self.widgetStretch = 0

        self.animatedDragPosition = MotionProfile(0,0, speed = 0.3)
        self.initialPositionNotSet = True
        self.setY(0)
        self.initialPositionNotSet = True

    def getDefinedHeight(self) -> int:
        return self.command.getDefinition().fullHeight
        

    def isFullyCollapsed(self) -> bool:
        return self.expandMotion.isDone() and not self.isExpanded()


    def getX(self) -> float:
        return self.dimensions.FIELD_WIDTH + self.X_MARGIN_LEFT
    
    def getY(self) -> float:

        if self.command.isDragging():
            return self.command.startDragY + self.command.dragOffset        

        return self.animatedDragPosition.get()
    
    def setY(self, y: float):
        self.currentY = y
        self.animatedDragPosition.setEndValue(y)
        if self.initialPositionNotSet:
            self.initialPositionNotSet = False
            self.animatedDragPosition.forceToEndValue()
    
    def getWidth(self) -> float:
        return self.dimensions.PANEL_WIDTH - self.X_MARGIN_LEFT - self.X_MARGIN_RIGHT
    
    # get height of the command
    def getHeight(self) -> float:
        if not self.command.isVisible():
            return 0
        return self.expandMotion.get() * self.dimensions.RESOLUTION_RATIO
    
    def getCenterPosition(self) -> tuple:
        x = self.dimensions.FIELD_WIDTH + self.dimensions.PANEL_WIDTH / 2
        y = self.getY() + self.getHeight() / 2
        return x,y
    
    # the center y position of the title header on the top of the command
    def getCenterHeadingY(self) -> float:
        return self.getY() + self.Y_BETWEEN_COMMANDS_MIN / 2
    
    # return 1 if expanded, 0 if not, and in between
    def getExpandedRatio(self) -> float:
        return (self.getHeight() - self.Y_BETWEEN_COMMANDS_MIN) / (self.getDefinedHeight() - self.Y_BETWEEN_COMMANDS_MIN)
    
    def getAddonPosition(self, px: float, py: float) -> tuple:
        x = self.getX() + px * self.getWidth()
        y = self.Y_BETWEEN_COMMANDS_MIN
        y += self.getY() + py * (self.getHeight() - self.Y_BETWEEN_COMMANDS_MIN - self.widgetStretch)
        return x,y

    # every tick, update animation if exists
    def onTick(self):
        if not self.expandMotion.isDone() or not self.animatedDragPosition.isDone():
            self.expandMotion.tick()
            self.animatedDragPosition.tick()
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

        self.widgetStretch = self.command.getStretchFromWidgets()
        
        expanded = self.isExpanded()

        if expanded:
            x = self.getDefinedHeight() + self.widgetStretch
        else:
            x = self.Y_BETWEEN_COMMANDS_MIN

        # If there is a change, then send callbacks to widgets
        if self.expandMotion.get() != x:
            if expanded:
                self.command.onExpand()
            else:
                self.command.onCollapse()
        
        self.expandMotion.setEndValue(x)

    