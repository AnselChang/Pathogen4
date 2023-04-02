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

from Widgets.widget_entity import WidgetEntity
from Widgets.readout_entity import ReadoutEntity

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from Observers.observer import Observer

from linked_list import LinkedListNode
from image_manager import ImageManager
from draw_order import DrawOrder
from dimensions import Dimensions
from reference_frame import PointRef, Ref
from pygame_functions import shade, drawText, FONT20, drawSurface
from math_functions import isInsideBox2
import pygame, re

"""
A CommandBlockEntity object describes a single instance of a command block
displayed on the right panel.
It references some CommandDefinition at any given point, which specfies the template of the
command. Note the same CommandDefinition may be shared by multiple CommandBlockEntities
The WidgetEntities and pathAdapters hold the informatino for this specific instance.
Position calculation is offloaded to CommandBlockPosition
"""

class CommandBlockEntity(Entity, LinkedListNode['CommandBlockEntity']):


    def __init__(self, path, pathAdapter: PathAdapter, database, entities: EntityManager, interactor: Interactor, commandExpansion: CommandExpansion, images: ImageManager, dimensions: Dimensions, drag: DragListener = None):
        super().__init__(
            click = ClickLambda(self, FonLeftClick = self.onClick),
            tick = TickLambda(self, FonTick = self.onTick),
            drag = drag,
            select = SelectLambda(self, "command", type = SelectorType.SOLO),
            drawOrder = DrawOrder.COMMANND_BLOCK
        )

        LinkedListNode.__init__(self)
        self.definitionIndex: int = 0

        self.path = path

        self.pathAdapter = pathAdapter
        
        self.type = self.pathAdapter.type
        self.database = database
        self.entities = entities
        self.interactor = interactor
        self.images = images
        self.dimensions = dimensions

        self.position = CommandBlockPosition(self, commandExpansion, self.dimensions)

        self.widgetEntities = self.manifestWidgets()
        self.readoutEntities = self.manifestReadouts()

        self.position.recomputeExpansion()

    def getDefinition(self) -> CommandDefinition:
        return self.database.getDefinition(self.type, self.definitionIndex)
    
    # Given the command widgets, create the WidgetEntities and add to entity manager
    def manifestWidgets(self) -> list[WidgetEntity]:

        commandStretchObserver = Observer(onNotify = self.position.recomputeExpansion)

        entities = []
        for widget in self.getDefinition().widgets:
            entity = widget.make(self)
            entity.addObserver(commandStretchObserver)
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

    # based on this command's height, find next command's y
    def updateNextY(self):
        self.position.updateNextY()      

    # Update animation every tick
    def onTick(self):
        self.position.onTick()

    # try to expand command when selected, but only when it's the only thing selected
    def onClick(self):

        if self.isExpanded():
            self.position.setCollapsed()
        else:
            self.position.setExpanded()

    def onExpand(self):
        for widget in self.widgetEntities:
            widget.onCommandExpand()

    def onCollapse(self):
        for widget in self.widgetEntities:
            widget.onCommandCollapse()

    def isVisible(self) -> bool:
        return True
    
    def getX(self) -> float:
        return self.position.getX()
    
    def getY(self) -> float:
        return self.position.getY()
    
    def getScrollbarOffset(self) -> int:
        return self.path.getScrollbarOffset()
    
    def setY(self, y: float):
        self.position.setY(y)

    def getWidth(self) -> float:
        return self.position.getWidth()
    
    def getHeight(self) -> float:
        return self.position.getHeight()
    
    # the dimensions of the command rectangle, calculated on-the-fly
    def getRect(self) -> tuple:
        return self.getX(), self.getY(), self.getWidth(), self.getHeight()
    
    # return 0 if minimized, 1 if maximized, and in between
    def getAddonsOpacity(self) -> float:
        ratio = self.position.getExpandedRatio()
        return ratio * ratio
    
    def getAddonPosition(self, px: float, py: float) -> tuple:
        return self.position.getAddonPosition(px, py)

    def isTouching(self, position: PointRef) -> bool:
        return isInsideBox2(*position.screenRef, *self.getRect())

    def getPosition(self) -> PointRef:
        return PointRef(Ref.SCREEN, self.position.getCenterPosition())
    
    def isExpanded(self) -> bool:
        return self.position.isExpanded()
    
    def isFullyCollapsed(self) -> bool:
        return self.position.isFullyCollapsed()
    
    # how much the widgets stretch the command by. return the largest one
    def getStretchFromWidgets(self) -> int:
        stretch = 0
        for widget in self.widgetEntities:
            stretch = max(stretch, widget.getCommandStretch())
        return stretch
    
    # whether some widget of command block is hovering
    def isWidgetHovering(self) -> bool:
        for widget in self.widgetEntities:
            if widget.hover is not None and widget.hover.isHovering:
                return True
        return False
    
    def isOtherHovering(self) -> bool:
        return False

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        CORNER_RADIUS = 3

        x, y, width, height = self.getRect()

        # draw rounded rect
        color = COMMAND_INFO[self.type].color
        if isActive and isHovered and self.interactor.leftDragging:
            color = shade(color, 1.15)
        elif isHovered or self.isWidgetHovering() or self.isOtherHovering():
            color = shade(color, 1.2)
        else:
            color = shade(color, 1.1)
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius = CORNER_RADIUS)

        # draw icon
        iconImage = self.images.get(self.pathAdapter.getIcon())
        x = self.dimensions.FIELD_WIDTH + 20
        y = self.position.getCenterHeadingY()
        drawSurface(screen, iconImage, x, y)

        # draw function name
        text = self.getDefinition().name + "()"
        x = self.dimensions.FIELD_WIDTH + 40
        drawText(screen, FONT20, text, (0,0,0), x, y, alignX = 0)

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