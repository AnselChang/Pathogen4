from BaseEntity.entity import Entity

from draw_order import DrawOrder
from Adapters.path_adapter import PathAdapter
from pygame_functions import drawSurface
import pygame

class CommandBlockIcon(Entity):

    def __init__(self, pathAdapter: PathAdapter):
        super().__init__(drawOrder = DrawOrder.WIDGET)
        self.pathAdapter = pathAdapter

    def getCenter(self) -> tuple:
        return self._ax(20), self._py(0.5)

    # must impl both of these if want to contain other entity
    def getWidth(self) -> float:
        return 0
    def getHeight(self) -> float:
        return 0

    # override
    def isTouching(self, position: tuple) -> bool:
        return False

    # override
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        # draw icon
        iconImage = self.images.get(self.pathAdapter.getIcon())
        drawSurface(screen, iconImage, self.CENTER_X, self.CENTER_Y)