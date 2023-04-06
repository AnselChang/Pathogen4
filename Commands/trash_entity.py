from BaseEntity.entity import Entity
from BaseEntity.EntityListeners.click_listener import ClickLambda
from BaseEntity.EntityListeners.hover_listener import HoverLambda

from image_manager import ImageManager, ImageID
from dimensions import Dimensions

from draw_order import DrawOrder
from reference_frame import PointRef, Ref
from pygame_functions import drawSurface
from math_functions import distance
import pygame

# trash button for custom commands
class TrashEntity(Entity):

    def __init__(self, parentCommand: Entity, onDelete = lambda: None):
        
        super().__init__(
            click = ClickLambda(self, FonLeftClick = onDelete),
            hover = HoverLambda(self),
            drawOrder = DrawOrder.WIDGET
        )
        
        self.parentCommand = parentCommand
        self.recomputePosition()

    def isTouching(self, position: PointRef) -> bool:
        return self.distanceTo(position) < 12
    
    def defineCenter(self) -> tuple:
        return self._px(1) - self._ax(60), self._py(0.5)


    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        image = self.images.get(ImageID.TRASH_ON if isHovered else ImageID.TRASH_OFF)
        drawSurface(screen, image, self.CENTER_X, self.CENTER_Y)