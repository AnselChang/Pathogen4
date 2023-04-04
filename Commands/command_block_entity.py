from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.click_listener import ClickLambda
from BaseEntity.EntityListeners.tick_listener import TickLambda
from BaseEntity.EntityListeners.drag_listener import DragListener
from BaseEntity.EntityListeners.select_listener import SelectLambda, SelectorType

from Adapters.path_adapter import PathAdapter

from CommandCreation.command_type import COMMAND_INFO
from CommandCreation.command_definition import CommandDefinition

from Commands.command_block_position import CommandBlockPosition
from Commands.command_expansion import CommandExpansion
from Commands.command_or_inserter import CommandOrInserter
from Commands.command_expansion import CommandExpansion

from Widgets.widget_entity import WidgetEntity
from Widgets.readout_entity import ReadoutEntity

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from Observers.observer import Observer

from font_manager import FontManager, FontID
from linked_list import LinkedListNode
from image_manager import ImageManager
from draw_order import DrawOrder
from dimensions import Dimensions
from reference_frame import PointRef, Ref
from pygame_functions import shade, drawText, drawSurface, drawTransparentRect
from math_functions import isInsideBox2
from Animation.motion_profile import MotionProfile
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


    def __init__(self, path, pathAdapter: PathAdapter, database, entities: EntityManager, interactor: Interactor, commandExpansion: CommandExpansion, images: ImageManager, fontManager: FontManager, dimensions: Dimensions, drag: DragListener = None,
                 defaultExpand: bool = False
                 ):
        
        self.animatedHeight = MotionProfile(self.HEIGHT, speed = 0.4)
        self.animatedPosition = MotionProfile(0, speed = 0.3)

        self.localExpansion = False
        
        # This recomputes position at Entity constructor
        super().__init__(
            click = ClickLambda(self, FonLeftClick = self.onClick),
            tick = TickLambda(self, FonTick = self.onTick),
            drag = drag,
            select = SelectLambda(self, "command", type = SelectorType.SOLO),
            drawOrder = DrawOrder.COMMANND_BLOCK
        )

        CommandOrInserter.__init__(self)
        self.definitionIndex: int = 0

        self.path = path

        self.pathAdapter = pathAdapter
        
        self.type = self.pathAdapter.type
        self.database = database
        self.entities = entities
        self.interactor = interactor
        self.images = images
        self.fontManager = fontManager
        self.dimensions = dimensions

        self.dragOffset = 0

        self.widgetEntities = self.manifestWidgets()
        self.readoutEntities = self.manifestReadouts()

        # whenever a global expansion flag is changed, recompute each individual command expansion
        self.commandExpansion = commandExpansion
        self.commandExpansion.subscribe(Observer(onNotify = self.updateTargetHeight))

        self.titleFont = self.fontManager.getDynamicFont(FontID.FONT_NORMAL, 15)

    # Update animation every tick
    def onTick(self):
        if not self.animatedPosition.isDone() or not self.animatedHeight.isDone():
            self.animatedPosition.tick()
            self.animatedHeight.tick()
            self.recomputePosition()

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
    
    def updateTargetHeight(self):

        self.EXPANDED_HEIGHT = self._pheight(self.getDefinition().fullHeight + self.getWidgetStretch())
        self.COLLAPSED_HEIGHT = self._pheight(0.0375)
        
        height = self.EXPANDED_HEIGHT if self.isActuallyExpanded() else self.COLLAPSED_HEIGHT        
        self.animatedHeight.setEndValue(height)

    def getTopLeft(self) -> tuple:
        # right below the previous CommandOrInserter
        return self._px(0), self._py(1)

    def getWidth(self) -> float:
        # 95% of the panel
        return self._pwidth(self.WIDTH_PERCENT_OF_PANEL)
    
    def getHeight(self) -> float:
        # current animated height
        return self._pheight(self.animatedHeight.get())
    
    def getPercentExpanded(self) -> float:
        return (self.HEIGHT - self.COLLAPSED_HEIGHT) / (self.EXPANDED_HEIGHT - self.COLLAPSED_HEIGHT)
        
    def isFullyCollapsed(self) -> bool:
        return self.HEIGHT == self.COLLAPSED_HEIGHT

    # Given the command widgets, create the WidgetEntities and add to entity manager
    def manifestWidgets(self) -> list[WidgetEntity]:

        widgetResizeObserver = Observer(onNotify = self.recomputePosition())

        entities = []
        for widget in self.getDefinition().widgets:
            entity = widget.make(self)
            entity.subscribe(widgetResizeObserver)
            self.entities.addEntity(entity, self)
            entities.append(entity)
        return entities
    
    # Given the command widgets, create the ReadoutEntities and add to entity manager
    def manifestReadouts(self) -> list[ReadoutEntity]:
        readouts = []
        for readout in self.getDefinition().readouts:
            readout = readout.make(self, self.pathAdapter)
            self.entities.addEntity(readout, self)
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
    
    # return 0 if minimized, 1 if maximized, and in between
    def getAddonsOpacity(self) -> float:
        DRAG_OPACITY = 0.7
        if self.isDragging():
            return DRAG_OPACITY

        ratio = self.getPercentExpanded()
        return ratio * ratio # square for steeper opacity animation
    
    # return 1 if not dragging, and dragged opacity if dragging
    # not applicable for regular command blocks
    def isDragging(self):
        return False

    def isTouching(self, position: tuple) -> bool:
        return isInsideBox2(*position, *self.RECT)
    
    # whether some widget of command block is hovering
    def isWidgetHovering(self) -> bool:
        for widget in self.widgetEntities:
            if widget.hover is not None and widget.hover.isHovering:
                return True
        return False

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        CORNER_RADIUS = 3

        x, y, width, height = self.getRect()

        # draw rounded rect
        color = COMMAND_INFO[self.type].color
        if isActive and isHovered and self.interactor.leftDragging:
            color = shade(color, 1.15)
        elif isHovered or self.isWidgetHovering():
            color = shade(color, 1.2)
        else:
            color = shade(color, 1.1)

        if self.isDragging():
            drawTransparentRect(screen, x, y, x+width, y+height, color, alpha = self.DRAG_OPACITY*255, radius = CORNER_RADIUS)
        else:
            pygame.draw.rect(screen, color, (x, y, width, height), border_radius = CORNER_RADIUS)

        # draw icon
        iconImage = self.images.get(self.pathAdapter.getIcon())
        x = self.dimensions.FIELD_WIDTH + 20
        y = self.position.getCenterHeadingY()
        drawSurface(screen, iconImage, x, y)

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