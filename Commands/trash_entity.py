from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.click_listener import ClickLambda
from BaseEntity.EntityListeners.hover_listener import HoverLambda

from image_manager import ImageManager, ImageID
from dimensions import Dimensions

from draw_order import DrawOrder
from reference_frame import PointRef, Ref
from pygame_functions import drawSurface
import pygame

# trash button for custom commands
class TrashEntity(Entity):

    def __init__(self, parentCommand: Entity, images: ImageManager, dimensions: Dimensions, onDelete = lambda: None):
        
        super().__init__(
            click = ClickLambda(self, FonLeftClick = onDelete),
            hover = HoverLambda(self),
            drawOrder = DrawOrder.WIDGET
        )
        
        self.parentCommand = parentCommand
        self.images = images
        self.dimensions = dimensions

    
    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        return (position - self.getPosition()).magnitude(Ref.SCREEN) < 12

    def getPosition(self) -> PointRef:
        x = self.dimensions.FIELD_WIDTH + self.dimensions.PANEL_WIDTH - 30
        y = self.parentCommand.getY() + self.parentCommand.position.Y_BETWEEN_COMMANDS_MIN / 2
        return PointRef(Ref.SCREEN, (x,y))

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        x,y = self.getPosition().screenRef
        image = self.images.get(ImageID.TRASH_ON if isHovered else ImageID.TRASH_OFF)
        drawSurface(screen, image, x, y)

    def toString(self) -> str:
        return "trash"