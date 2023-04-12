from __future__ import annotations
from typing import TYPE_CHECKING
from adapter.turn_adapter import TurnAdapter
from entity_base.listeners.hover_listener import HoverLambda
from entity_ui.scrollbar.scrolling_content_container import ScrollingContentContainer
from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer
if TYPE_CHECKING:
    from root_container.path import Path
    from command_creation.command_definition_database import CommandDefinitionDatabase

from entity_base.entity import Entity
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.tick_listener import TickLambda
from entity_base.listeners.drag_listener import DragListener
from entity_base.listeners.select_listener import SelectLambda, SelectorType

from adapter.path_adapter import PathAdapter

from command_creation.command_type import CommandType
from command_creation.command_definition import CommandDefinition

from root_container.panel_container.command_block.command_block_header import CommandBlockHeader
from root_container.panel_container.command_expansion.command_expansion_container import CommandExpansionContainer
from root_container.panel_container.command_block.command_or_inserter import CommandOrInserter

from root_container.panel_container.element.overall.elements_container_factory import createElementsContainer

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

class CommandBlockEntity(Entity, CommandOrInserter, Observer):

    HIGHLIGHTED = None


    def __init__(self, container: BlockTabContentsContainer, parent: CommandOrInserter, path: Path, pathAdapter: PathAdapter, database: CommandDefinitionDatabase, commandExpansion: CommandExpansionContainer, drag: DragListener = None, defaultExpand: bool = False, hasTrashCan: bool = False):
        
        self.path = path
        self.container = container

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

        
        
        # This recomputes position at Entity constructor
        super().__init__(
            parent = parent,
            click = ClickLambda(self, FonLeftClick = self.onClick, FOnMouseDown = self.onMouseDown),
            tick = TickLambda(self, FonTick = self.onTick),
            drag = drag,
            hover = HoverLambda(self),
            #select = SelectLambda(self, "command", type = SelectorType.SOLO),
            drawOrder = DrawOrder.COMMANND_BLOCK,
            recomputeWhenInvisible = True
        )

        CommandOrInserter.__init__(self, True)

        # whenever a global expansion flag is changed, recompute each individual command expansion
        self.commandExpansion = commandExpansion
        self.commandExpansion.subscribe(self, onNotify = self.path.recalculateTargets)

        self.elementsContainer = None
        self.mouseHoveringCommand = False

        self.elementsVisible = True

        self.updateTargetHeight(True)
        self.recomputePosition()
        self.headerEntity = CommandBlockHeader(self, pathAdapter, hasTrashCan)

        """
        Right now, this means that the command block is hardcoded to
        store only the elements for the current command definition,
        and switching command definitions will not change the elements.
        This will be changed in the future.
        """
        self.elementsContainer = createElementsContainer(self, self.getDefinition(), pathAdapter)
        
        # on element container resize, recompute target height
        self.elementsContainer.subscribe(self, onNotify = self.onElementsResize)

        # For turn commands: if turn is enabled/disabled, command is shown/hidden
        if self.pathAdapter.type == CommandType.TURN:
            self.pathAdapter.subscribe(self, id = NotifyType.TURN_ENABLE_TOGGLED, onNotify = self.onTurnEnableToggled)

        self.updateTargetHeight(True)
        self.recomputePosition()

        self.onTurnEnableToggled()

    def recomputePosition(self):
        # If entire command block is hidden, only recompute position of next inserter/command
        if not self.isVisible():
            super().recomputePosition(excludeChildIf = 
                lambda child: child is not self.getNext()           
            )
        # Otherwise, compute everything that is visible
        # (note that elements container won't be computed anyways if invisibel)
        else:
            super().recomputePosition()

    # normally should never override this. but because of the bad design decision
    # for inserters/commands to be parent/children of each other, prevent parent
    # inserter being invisible from making self invisible
    def isVisible(self) -> bool:

        return self._LOCAL_VISIBLE and self.container.isVisible()

    # called when a different name is selected in the dropdown
    def onFunctionChange(self):

        # First, get the definition for the new function
        functionName = self.headerEntity.functionName.getFunctionName()
        self.definitionIndex = self.database.getDefinitionIndexByName(self.type, functionName)

        # Delete old elements container and assign new one
        self.entities.removeEntity(self.elementsContainer)
        self.elementsContainer = createElementsContainer(self, self.getDefinition(), self.pathAdapter)

        # resize based on new elements container rect
        self.onElementsResize()

    # Update animation every tick
    def onTick(self):

        if self.elementsVisible and self.isFullyCollapsed():
            self.elementsContainer.setInvisible()
            self.elementsVisible = False
        elif not self.elementsVisible and not self.isFullyCollapsed():
            self.elementsContainer.setVisible()
            self.elementsVisible = True

        if self.getNext() is not None and self.getNext().isSelfOrChildrenHovering():
            self.mouseHoveringCommand = False
        else:
            self.mouseHoveringCommand = self.isSelfOrChildrenHovering()


        if not self.animatedExpansion.isDone():
            #self.animatedPosition.tick()
            self.animatedExpansion.tick()

            self.path.onChangeInCommandPositionOrHeight()

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

    def onElementsResize(self):
        self.updateTargetHeight()
        self.path.onChangeInCommandPositionOrHeight()
    
    # Call this whenever there might be a change to target height
    def updateTargetHeight(self, isFirst: bool = False):
        #print(self, "update target height")

        expanded = self.isActuallyExpanded()
        
        self.ACTUAL_COLLAPSED_HEIGHT = self._aheight(self.COLLAPSED_HEIGHT)
        self.ACTUAL_EXPANDED_HEIGHT = self._aheight(self.EXPANDED_HEIGHT) + self.getElementStretch()
        self.ACTUAL_HEIGHT = self.ACTUAL_EXPANDED_HEIGHT if expanded else self.ACTUAL_COLLAPSED_HEIGHT

        self.animatedExpansion.setEndValue(1 if expanded else 0)
           
        if isFirst:
            self.animatedExpansion.forceToEndValue()

    def updateTargetY(self, force: bool = False):
        pass
        #self.targetY = self._py(1) - self._parent.dragOffset + self.dragOffset
        #self.animatedPosition.setEndValue(self.targetY)
        #if force:
        #    self.animatedPosition.forceToEndValue()

    def defineBefore(self):
        pass
        #self.updateTargetHeight()
        #self.updateTargetY()

    def defineTopLeft(self) -> tuple:

        #if self.path.forceAnimationToEnd:
        #        self.animatedPosition.forceToEndValue()

        # right below the previous CommandOrInserter
        self.normalY = self._py(1)
        self.draggingY = self._py(1) if self.dragPosition is None else self.dragPosition
        return self._px(0), self.draggingY
    

    def defineWidth(self) -> float:
        return self._pwidth(1)
    
    def defineHeight(self) -> float:

        if not self.isVisible():
            return 0

        if self.path.forceAnimationToEnd:
                self.animatedExpansion.forceToEndValue()
        
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

    # commands are sandwiched by CommandInserters
    def getPreviousCommand(self) -> 'CommandBlockEntity':
        return self.getPrevious().getPrevious()
    
    def getNextCommand(self) -> 'CommandBlockEntity':
        return self.getNext().getNext()
    
    # Set the local expansion of the command without modifying global expansion flags
    def setLocalExpansion(self, isExpanded):
        self.localExpansion = isExpanded

    # Toggle command expansion. Modify global expansion flags if needed
    def onClick(self, mouse: tuple):

        if self.localExpansion:
            # If all are being forced to contract right now, disable forceContract, but 
            # all other commands should retain being contracted except this one
            if self.commandExpansion.getForceCollapse():
                self.path.setAllLocalExpansion(False)
                self.commandExpansion.setForceCollapse(False)
        else:
            if self.commandExpansion.getForceExpand():
                self.path.setAllLocalExpansion(True)
                self.commandExpansion.setForceExpand(False)

        self.localExpansion = not self.localExpansion
        self.path.recalculateTargets()

    def onTurnEnableToggled(self):
        if self.pathAdapter.type == CommandType.TURN:
            turnAdapter: TurnAdapter = self.pathAdapter
            if turnAdapter.isTurnEnabled():
                self.setVisible()
            else:
                self.setInvisible()

            self.path.onChangeInCommandPositionOrHeight()

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
        return False
    
    def isHighlighted(self) -> bool:
        return CommandBlockEntity.HIGHLIGHTED == self
    
    # Highlight the command block visually
    # Also, contract all commands except this one
    def highlight(self):

        if self.isHighlighted():
            CommandBlockEntity.HIGHLIGHTED = None
            self.localExpansion = False
            self.path.recalculateTargets()
            return

        # highlight and expand this command, disabling global flag if need be
        CommandBlockEntity.HIGHLIGHTED = self
        self.path.setAllLocalExpansion(False)
        self.commandExpansion.setForceCollapse(False)
        self.localExpansion = True
        self.path.recalculateTargets()

        # scroll to this command
        tail = self.path.commandList.tail
        contentHeight = 0 if tail is None else tail._getTargetHeight()
        self.path.scrollHandler.setContentHeight(contentHeight)
        # cursed number to make scrollbar go down a little more
        self.path.scrollHandler.setManualScrollbarPosition(self._getTargetHeight() - self.ACTUAL_COLLAPSED_HEIGHT*5)

    # Called when the highlight button in the command block is clicked.
    # Should highlight the corresponding node or segment in the path
    def onHighlightPath(self, mouse: tuple):
        pathEntity = self.path.getPathEntityFromCommand(self)
        self.interactor.removeAllEntities()
        self.interactor.addEntity(pathEntity)

    # if mouse down on different command, clear highlight
    def onMouseDown(self, mouse: tuple):
        if CommandBlockEntity.HIGHLIGHTED is not None and CommandBlockEntity.HIGHLIGHTED is not self:
            CommandBlockEntity.HIGHLIGHTED = None

    def getColor(self) -> tuple:
        return self.getDefinition().color

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
            drawTransparentRect(screen, *self.RECT, color, alpha = self.DRAG_OPACITY*255, radius = self.CORNER_RADIUS)
        else:
            pygame.draw.rect(screen, color, self.RECT, border_radius = self.CORNER_RADIUS)

        if isHighlighted:
            pygame.draw.rect(screen, (0,0,0), self.RECT, border_radius = self.CORNER_RADIUS, width = 2)

        # draw function name
        text = self.getDefinition().name + "()"
        x = self.dimensions.FIELD_WIDTH + 40

    def toString(self) -> str:
        return "Command Block Entity"

     # Try to find variable name in self.adapter and self.widgets and replace with value
    def _replaceWithValue(self, token: str) -> str:
        if token.startswith("$") and token.endswith("$"):
            variableName = token[1:-1]

            value = self.pathAdapter.get(variableName)
            if value is not None:
                return value
            
            for widgetEntity in self.widgetEntities:
                if variableName == widgetEntity.getName():
                    return widgetEntity.getValue()
                
        # No variable found. return string as-is
        return token

    # recalculate final text from template
    # Given pathAdapter and widgetAdapter specific to the command block
    def getCodeText(self):

        result = ""

        # Split each $variable$ into tokens
        tokens = re.split(r'(\$[^\$]+\$)', self.getDefinition().templateText)

        # replace each $variable$ with value
        for token in tokens:
            result += self._replaceWithValue(token)

        return result