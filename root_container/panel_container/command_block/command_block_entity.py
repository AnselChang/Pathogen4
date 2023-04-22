from __future__ import annotations
from typing import TYPE_CHECKING
from adapter.turn_adapter import TurnAdapter
from entity_base.listeners.hover_listener import HoverLambda
from entity_ui.scrollbar.scrolling_content_container import ScrollingContentContainer

if TYPE_CHECKING:
    from command_creation.command_definition_database import CommandDefinitionDatabase
    from root_container.panel_container.command_block.command_block_container import CommandBlockContainer
    from root_container.panel_container.command_block.command_sequence_handler import CommandSequenceHandler

from entity_base.entity import Entity
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.tick_listener import TickLambda
from entity_base.listeners.drag_listener import DragLambda, DragListener
from entity_base.listeners.select_listener import SelectLambda, SelectorType

from adapter.path_adapter import PathAdapter

from command_creation.command_type import CommandType
from command_creation.command_definition import CommandDefinition

from root_container.panel_container.command_block.command_block_header import CommandBlockHeader
from root_container.panel_container.command_expansion.command_expansion_container import CommandExpansionContainer

from root_container.panel_container.element.overall.elements_container_factory import createElementsContainer

from root_container.panel_container.command_block.command_block_constants import CommandBlockConstants as Constants
from common.font_manager import FontID
from common.draw_order import DrawOrder
from data_structures.observer import NotifyType, Observer
from utility.pygame_functions import shade, drawText, drawTransparentRect
from utility.motion_profile import MotionProfile
import pygame, re

"""
A CommandBlockEntity object describes a single instance of a command block
displayed on the right panel.
It references some CommandDefinition at any given point, which specfies the template of the
command. Note the same CommandDefinition may be shared by multiple CommandBlockEntities
The WidgetEntities and pathAdapters hold the informatino for this specific instance.
Position calculation is offloaded to CommandBlockPosition
"""

class CommandBlockEntity(Entity, Observer):

    HIGHLIGHTED = None


    def __init__(self, parent: CommandBlockContainer, handler: CommandSequenceHandler, pathAdapter: PathAdapter, database: CommandDefinitionDatabase, commandExpansion: CommandExpansionContainer, drag: DragListener = None, defaultExpand: bool = False, hasTrashCan: bool = False):
        
        self.container = parent
        
        self.handler = handler

        self.COLLAPSED_HEIGHT = 35
        self.EXPANDED_HEIGHT = 50 

        self.DRAG_OPACITY = 0.7
        self.dragOffset = 0

        self.definitionIndex: int = 0
        self.database = database
        self.pathAdapter = pathAdapter
        self.type = self.pathAdapter.type

        # controls height animatino
        self.animatedExpansion = MotionProfile(0, speed = 0.4)
        # whether to expand by default, ignoring global flags
        self.localExpansion = False

        r,g,b = self.getDefinition().color
        self.colorR = MotionProfile(r, speed = 0.2)
        self.colorG = MotionProfile(g, speed = 0.2)
        self.colorB = MotionProfile(b, speed = 0.2)

        if drag is None:
            drag = DragLambda(self)
        
        # This recomputes position at Entity constructor
        super().__init__(
            parent = parent,
            click = ClickLambda(self, FonLeftClick = self.onClick, FOnMouseDown = self.onMouseDown),
            tick = TickLambda(self, FonTickStart = self.onTick),
            drag = drag,
            hover = HoverLambda(self),
            drawOrder = DrawOrder.COMMANND_BLOCK,
            recomputeWhenInvisible = True
        )

        # whenever a global expansion flag is changed, recompute each individual command expansion
        self.commandExpansion = commandExpansion

        self.elementsContainer = None
        self.mouseHoveringCommand = False

        self.elementsVisible = True

        self.headerEntity = CommandBlockHeader(self, pathAdapter, hasTrashCan)

        """
        Right now, this means that the command block is hardcoded to
        store only the elements for the current command definition,
        and switching command definitions will not change the elements.
        This will be changed in the future.
        """
        self.elementsContainer = createElementsContainer(self, self.getDefinition(), pathAdapter)

        # For turn commands: if turn is enabled/disabled, command is shown/hidden
        if self.pathAdapter.type == CommandType.TURN:
            self.pathAdapter.subscribe(self, id = NotifyType.TURN_ENABLE_TOGGLED, onNotify = self.onTurnEnableToggled)

        self.onTurnEnableToggled()

    # called when a different name is selected in the dropdown
    def onFunctionChange(self):

        # First, get the definition for the new function
        functionName = self.headerEntity.functionName.getFunctionName()
        self.definitionIndex = self.database.getDefinitionIndexByName(self.type, functionName)

        # Delete old elements container and assign new one
        self.entities.removeEntity(self.elementsContainer)
        self.elementsContainer = createElementsContainer(self, self.getDefinition(), self.pathAdapter)

        # switch to the new definition color (animated)
        r,g,b = self.getDefinition().color
        self.colorR.setEndValue(r)
        self.colorG.setEndValue(g)
        self.colorB.setEndValue(b)

        # set initial visibility for new elements container
        if self.isFullyCollapsed():
            self.elementsContainer.setInvisible()
            self.elementsVisible = False
        else:
            self.elementsContainer.setVisible()
            self.elementsVisible = True

        self.propagateChange()

    # Update animation every tick
    def onTick(self):
        # handle elements visibility
        if self.elementsVisible and self.isFullyCollapsed():
            self.elementsContainer.setInvisible()
            self.elementsVisible = False
        elif not self.elementsVisible and not self.isFullyCollapsed():
            self.elementsContainer.setVisible()
            self.elementsVisible = True

        self.mouseHoveringCommand = self.isSelfOrChildrenHovering()

        self.colorR.tick()
        self.colorG.tick()
        self.colorB.tick()
        # handle color animation
        if self.colorR.wasChange() or self.colorG.wasChange() or self.colorB.wasChange():
            self.headerEntity.functionName.updateColor()

        # handle expansion animation
        if not self.animatedExpansion.isDone():
            #self.animatedPosition.tick()
            self.animatedExpansion.tick()

            self.propagateChange()

    def getDefinition(self) -> CommandDefinition:
        return self.database.getDefinition(self.type, self.definitionIndex)
    
    def getFunctionName(self) -> str:
        return self.getDefinition().name
    
    # how much the widgets stretch the command by. return the largest one
    def getElementStretch(self) -> int:
        if self.elementsContainer is None:
            return 0
        return self.elementsContainer.defineHeight()
    
    def isActuallyExpanded(self) -> bool:
        if self.commandExpansion.getForceCollapse():
            return False
        elif self.commandExpansion.getForceExpand():
            return True
        return self.localExpansion


    def defineWidth(self) -> float:
        return self._pwidth(1)
    
    def defineHeight(self) -> float:

        if not self.isVisible():
            return 0
        
        # calculate target height
        expanded = self.isActuallyExpanded()
        
        self.ACTUAL_COLLAPSED_HEIGHT = self._aheight(self.COLLAPSED_HEIGHT)
        self.ACTUAL_EXPANDED_HEIGHT = self._aheight(self.EXPANDED_HEIGHT) + self.getElementStretch()
        self.ACTUAL_HEIGHT = self.ACTUAL_EXPANDED_HEIGHT if expanded else self.ACTUAL_COLLAPSED_HEIGHT

        self.animatedExpansion.setEndValue(1 if expanded else 0)
        
        # current animated height
        ratio = self.animatedExpansion.get()
        height = self.ACTUAL_COLLAPSED_HEIGHT + (self.ACTUAL_EXPANDED_HEIGHT - self.ACTUAL_COLLAPSED_HEIGHT) * ratio
        return height
    
    def getPercentExpanded(self) -> float:
        return self.animatedExpansion.get()
        
    def isFullyCollapsed(self) -> bool:
        return self.animatedExpansion.get() == 0
    
    def isFullyExpanded(self) -> bool:
        return self.animatedExpansion.get() == 1
    
    def getCommandType(self) -> CommandType:
        return self.type
    
    # Set the local expansion of the command without modifying global expansion flags
    def setLocalExpansion(self, isExpanded):
        self.localExpansion = isExpanded

    # Toggle command expansion. Modify global expansion flags if needed
    def onClick(self, mouse: tuple):

        if self.localExpansion:
            # If all are being forced to contract right now, disable forceContract, but 
            # all other commands should retain being contracted except this one
            if self.commandExpansion.getForceCollapse():
                self.handler.setAllLocalExpansion(False)
                self.commandExpansion.setForceCollapse(False)
        else:
            if self.commandExpansion.getForceExpand():
                self.handler.setAllLocalExpansion(True)
                self.commandExpansion.setForceExpand(False)

        self.localExpansion = not self.localExpansion
        self.propagateChange()

    def onTurnEnableToggled(self):
        if self.pathAdapter.type == CommandType.TURN:
            turnAdapter: TurnAdapter = self.pathAdapter
            if turnAdapter.isTurnEnabled():
                self.setVisible()
            else:
                self.setInvisible()

            self.propagateChange()

    def getOpacity(self) -> float:
        if self.isDragging():
            return 0.7 # drag opacity
        else:
            return 1
    
    # return 0 if minimized, 1 if maximized, and in between
    def getAddonsOpacity(self) -> float:
        if self.isDragging():
            return self.getOpacity()
        else:
            ratio = self.getPercentExpanded()
            return ratio ** 2 # square for steeper opacity animation
    
    # return 1 if not dragging, and dragged opacity if dragging
    # not applicable for regular command blocks
    def isDragging(self):
        return self.drag.isDragging
    
    def isHighlighted(self) -> bool:
        return CommandBlockEntity.HIGHLIGHTED == self
    
    # Highlight the command block visually
    # Also, contract all commands except this one
    def highlight(self):

        if self.isHighlighted():
            CommandBlockEntity.HIGHLIGHTED = None
            self.localExpansion = False
            self.propagateChange()
            return

        # highlight and expand this command, disabling global flag if need be
        CommandBlockEntity.HIGHLIGHTED = self
        self.handler.setAllLocalExpansion(False)
        self.commandExpansion.setForceCollapse(False)
        self.localExpansion = True
        self.propagateChange()

        self.handler.scrollToCommand(self)

    # Called when the highlight button in the command block is clicked.
    # Should highlight the corresponding node or segment in the path
    def onHighlightPath(self, mouse: tuple):
        self.handler.highlightPathFromCommand(self)

    # if mouse down on different command, clear highlight
    def onMouseDown(self, mouse: tuple):
        if CommandBlockEntity.HIGHLIGHTED is not None and CommandBlockEntity.HIGHLIGHTED is not self:
            CommandBlockEntity.HIGHLIGHTED = None

    def getColor(self) -> tuple:
        r = self.colorR.get()
        g = self.colorG.get()
        b = self.colorB.get()
        return (r, g, b)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        isHighlighted = (CommandBlockEntity.HIGHLIGHTED is self)

        # draw rounded rect
        color = self.getColor()
        if isHighlighted:
            color = shade(color, 1.4)
        elif isActive and isHovered and self.interactor.leftDragging:
            color = shade(color, 1.3)
        elif self.mouseHoveringCommand and not self.interactor.disableUntilMouseUp:
            color = shade(color, 1.2)
        else:
            color = shade(color, 1.1)

        if self.isDragging():
            drawTransparentRect(screen, *self.RECT, color, alpha = self.DRAG_OPACITY*255, radius = Constants.CORNER_RADIUS)
        else:
            pygame.draw.rect(screen, color, self.RECT, border_radius = Constants.CORNER_RADIUS)

        if isHighlighted:
            pygame.draw.rect(screen, (0,0,0), self.RECT, border_radius = Constants.CORNER_RADIUS, width = 2)

        # draw function name
        text = self.getDefinition().name + "()"
        x = self.dimensions.FIELD_WIDTH + 40

    def toString(self) -> str:
        return "Command Block Entity"
    
    def getNextInserter(self) -> CommandBlockEntity:
        return self.handler.getNext(self)
    
    def getPreviousInserter(self) -> CommandBlockEntity:
        return self.handler.getPrevious(self)
    
    def getNextCommand(self) -> CommandBlockEntity:
        inserter = self.getNextInserter()
        if inserter is None:
            return None
        else:
            return self.handler.getNext(inserter)
    
    def getPreviousCommand(self) -> CommandBlockEntity:
        inserter = self.getPreviousInserter()
        if inserter is None:
            return None
        else:
            return self.handler.getPrevious(inserter)