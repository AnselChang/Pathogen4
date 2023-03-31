from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.select_listener import SelectLambda
from BaseEntity.EntityListeners.tick_listener import TickLambda

from Adapters.path_adapter import PathAdapter

from CommandCreation.command_type import COMMAND_INFO, CommandTypeInfo
from CommandCreation.command_definition_database import CommandDefinitionDatabase
from CommandCreation.command_definition import CommandDefinition

from Commands.command_block_position import CommandBlockPosition

from Widgets.widget_entity import WidgetEntity
from Widgets.readout_entity import ReadoutEntity

from EntityHandler.entity_manager import EntityManager
from EntityHandler.interactor import Interactor

from linked_list import LinkedListNode

from image_manager import ImageManager, ImageID
from draw_order import DrawOrder
from dimensions import Dimensions
from reference_frame import PointRef, Ref
from pygame_functions import shade, drawText, FONT20, drawSurface
from math_functions import isInsideBox2
import pygame, re



class CommandBlockEntity(Entity, LinkedListNode['CommandBlockEntity']):

    expandedEntity: 'CommandBlockEntity' = None

    def __init__(self, pathAdapter: PathAdapter, database: CommandDefinitionDatabase, entities: EntityManager, interactor: Interactor, images: ImageManager, dimensions: Dimensions):
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
        self.definitionIndex: int = 0

        self.pathAdapter = pathAdapter
        
        self.type = self.pathAdapter.type
        self.database = database
        self.entities = entities
        self.interactor = interactor
        self.images = images
        self.dimensions = dimensions

        self.widgetEntities = self.manifestWidgets()
        self.readoutEntities = self.manifestReadouts()

    # MUST call this after being added to the linked list
    def initPosition(self):
        self.position = CommandBlockPosition(self, self.dimensions)

    def getDefinition(self) -> CommandDefinition:
        return self.database.getDefinition(self.type, self.definitionIndex)
    
    # Given the command widgets, create the WidgetEntities and add to entity manager
    def manifestWidgets(self) -> list[WidgetEntity]:
        entities = []
        for widget in self.getDefinition().widgets:
            entity = WidgetEntity(self, widget)
            self.entities.addEntity(entity)
            entities.append(entity)
        return entities
    
    # Given the command widgets, create the ReadoutEntities and add to entity manager
    def manifestReadouts(self) -> list[ReadoutEntity]:
        readouts = []
        for readout in self.getDefinition().readouts:
            readout = ReadoutEntity(self, readout, self.pathAdapter)
            self.entities.addEntity(readout)
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
    def onSelect(self):

        # only expand if it's the only thing selected
        if self.interactor.selected.hasOnly(self):
            self.position.setExpanded()
            CommandBlockEntity.expandedEntity = self
        else:
            if CommandBlockEntity.expandedEntity is not None:
                CommandBlockEntity.expandedEntity.position.setContracted()
                CommandBlockEntity.expandedEntity = None

    # minimize command when not selected
    def onDeselect(self):
        self.position.setContracted()
        CommandBlockEntity.expandedEntity = None

    def isVisible(self) -> bool:
        return True
    
    def getX(self) -> float:
        return self.position.getX()
    
    def getY(self) -> float:
        return self.position.getY()
    
    def getRect(self) -> tuple:
        return self.position.getRect()

    def isTouching(self, position: PointRef) -> bool:
        return isInsideBox2(*position.screenRef, *self.getRect())

    def getPosition(self) -> PointRef:
        return PointRef(Ref.SCREEN, self.position.getCenterPosition())
    
    # whether some widget of command block is hovering
    def isWidgetHovering(self) -> bool:
        for widget in self.widgetEntities:
            if widget.hover.isHovering:
                return True
        return False

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        CORNER_RADIUS = 3

        x, y, width, height = self.position.getRect()

        # draw rounded rect
        color = COMMAND_INFO[self.state.type].color
        if isHovered or self.isWidgetHovering():
            color = shade(color, 1.2)
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius = CORNER_RADIUS)

        # draw selected border
        if isActive:
            pygame.draw.rect(screen, (0,0,0), (x, y, width, height), border_radius = CORNER_RADIUS, width = 2)

        # draw icon
        iconImage = self.images.get(self.pathAdapter.getIcon())
        x = self.dimensions.FIELD_WIDTH + 20
        y = self.position.getCenterPosition()[1]
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