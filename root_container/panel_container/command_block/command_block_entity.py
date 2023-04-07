from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.path import Path

from entity_base.entity import Entity
from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.tick_listener import TickLambda
from entity_base.listeners.drag_listener import DragListener
from entity_base.listeners.select_listener import SelectLambda, SelectorType

from adapter.path_adapter import PathAdapter

from command_creation.command_type import COMMAND_INFO
from command_creation.command_definition import CommandDefinition

from root_container.panel_container.command_block.command_block_header import CommandBlockHeader
from root_container.panel_container.command_expansion.command_expansion_handler import CommandExpansionHandler
from root_container.panel_container.command_block.command_or_inserter import CommandOrInserter

from root_container.panel_container.element.widget.widget_entity import WidgetEntity
from root_container.panel_container.element.readout.readout_entity import ReadoutEntity

from common.font_manager import FontID
from common.draw_order import DrawOrder
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

class CommandBlockEntity(Entity, CommandOrInserter):


    def __init__(self, parent: CommandOrInserter, path: Path, pathAdapter: PathAdapter, database, commandExpansion: CommandExpansionHandler, drag: DragListener = None, defaultExpand: bool = False, hasTrashCan: bool = False):
        
        self.definitionIndex: int = 0
        self.database = database
        self.pathAdapter = pathAdapter
        self.type = self.pathAdapter.type

        self.animatedHeight = MotionProfile(self.getDefinition().fullHeight, speed = 0.4)
        self.animatedPosition = MotionProfile(0, speed = 0.3)

        self.localExpansion = False
        
        # This recomputes position at Entity constructor
        super().__init__(
            parent = parent,
            click = ClickLambda(self, FonLeftClick = self.onClick),
            tick = TickLambda(self, FonTick = self.onTick),
            drag = drag,
            select = SelectLambda(self, "command", type = SelectorType.SOLO),
            drawOrder = DrawOrder.COMMANND_BLOCK
        )

        CommandOrInserter.__init__(self)

        # whenever a global expansion flag is changed, recompute each individual command expansion
        self.commandExpansion = commandExpansion
        self.commandExpansion.subscribe(onNotify = self.updateTargetHeight)

        self.widgetEntities = []
        self.readoutEntities = []
        self.updateTargetHeight()
        self.recomputePosition()
        self.headerEntity = CommandBlockHeader(self, pathAdapter, hasTrashCan)

        self.path = path

        self.dragOffset = 0

        self.widgetEntities = self.manifestWidgets()
        self.readoutEntities = self.manifestReadouts()

        self.titleFont = self.fontManager.getDynamicFont(FontID.FONT_NORMAL, 15)

    # Update animation every tick
    def onTick(self):
        if not self.animatedPosition.isDone() or not self.animatedHeight.isDone():
            self.animatedPosition.tick()
            self.animatedHeight.tick()
            self.path.onChangeInCommandPositionOrHeight()

    def getDefinition(self) -> CommandDefinition:
        return self.database.getDefinition(self.type, self.definitionIndex)
    
    # how much the widgets stretch the command by. return the largest one
    def getWidgetStretch(self) -> int:
        stretch = 0
        for widget in self.widgetEntities:
            stretch = max(stretch, widget.getCommandStretch())
        return stretch
    
    def isActuallyExpanded(self) -> bool:
        if self.commandExpansion.getForceCollapse():
            return False
        elif self.commandExpansion.getForceExpand():
            return True
        return self.localExpansion
    
    # Call this whenever there might be a change to target height
    def updateTargetHeight(self):

        self.EXPANDED_HEIGHT = self._pheight(self.getDefinition().fullHeight) + self.getWidgetStretch()
        self.COLLAPSED_HEIGHT = self._pheight(0.0375)
        
        height = self.EXPANDED_HEIGHT if self.isActuallyExpanded() else self.COLLAPSED_HEIGHT        
        self.animatedHeight.setEndValue(height)

    def defineTopLeft(self) -> tuple:
        # right below the previous CommandOrInserter
        return self._px(0), self._py(1)

    def defineWidth(self) -> float:
        # 95% of the panel
        return self._pwidth(1)
    
    def defineHeight(self) -> float:
        # current animated height
        return self._pheight(self.animatedHeight.get())
    
    def getPercentExpanded(self) -> float:
        return (self.HEIGHT - self.COLLAPSED_HEIGHT) / (self.EXPANDED_HEIGHT - self.COLLAPSED_HEIGHT)
        
    def isFullyCollapsed(self) -> bool:
        return self.HEIGHT == self.COLLAPSED_HEIGHT
    
    def isFullyExpanded(self) -> bool:
        return self.HEIGHT == self.EXPANDED_HEIGHT

    # Given the command widgets, create the WidgetEntities and add to entity manager
    def manifestWidgets(self) -> list[WidgetEntity]:

        widgets: list[WidgetEntity] = []
        for widget in self.getDefinition().widgets:
            widgetEntity = widget.make(self)
            widgetEntity.subscribe(onNotify = self.updateTargetHeight)
            widgets.append(widgetEntity)
        return widgets
    
    # Given the command widgets, create the ReadoutEntities and add to entity manager
    def manifestReadouts(self) -> list[ReadoutEntity]:
        readouts: list[ReadoutEntity] = []
        for readout in self.getDefinition().readouts:
            readout = readout.make(self, self.pathAdapter)
            readouts.append(readout)
        return readouts
    

    # commands are sandwiched by CommandInserters
    def getPreviousCommand(self) -> 'CommandBlockEntity':
        return self.getPrevious().getPrevious()
    
    def getNextCommand(self) -> 'CommandBlockEntity':
        return self.getNext().getNext()
    
    # Set the local expansion of the command without modifying global expansion flags
    def setLocalExpansion(self, isExpanded):
        self.localExpansion = isExpanded
        self.updateTargetHeight()

    # Toggle command expansion. Modify global expansion flags if needed
    def onClick(self):

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
        self.updateTargetHeight()

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
            return ratio * ratio # square for steeper opacity animation
    
    # return 1 if not dragging, and dragged opacity if dragging
    # not applicable for regular command blocks
    def isDragging(self):
        return False
    
    # whether some widget of command block is hovering
    def isWidgetHovering(self) -> bool:
        for widget in self.widgetEntities:
            if widget.hover is not None and widget.hover.isHovering:
                return True
        return False

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        CORNER_RADIUS = 3

        # draw rounded rect
        color = COMMAND_INFO[self.type].color
        if isActive and isHovered and self.interactor.leftDragging:
            color = shade(color, 1.15)
        elif isHovered or self.isWidgetHovering():
            color = shade(color, 1.2)
        else:
            color = shade(color, 1.1)

        if self.isDragging():
            drawTransparentRect(screen, *self.RECT, color, alpha = self.DRAG_OPACITY*255, radius = CORNER_RADIUS)
        else:
            pygame.draw.rect(screen, color, self.RECT, border_radius = CORNER_RADIUS)

        # draw function name
        text = self.getDefinition().name + "()"
        x = self.dimensions.FIELD_WIDTH + 40
        drawText(screen, self.titleFont.get(), text, (0,0,0), x, y, alignX = 0)

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